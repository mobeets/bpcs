from math import ceil
import numpy as np
from logger import log
from bpcs_steg import conjugate, arr_bpcs_complexity, max_bpcs_complexity, checkerboard

def get_conj_grid_prefix(dims, alpha):
    """
    dims is list specifying grid shape
    alpha is float

    returns a list of trash bits to prefix each conjugation map
        to ensure that the resulting grid will have complexity >= alpha
    """
    n = reduce(lambda x,y: x*y, dims, 1)
    checkered = checkerboard(*dims).reshape(-1).tolist()
    nprefix = int(ceil(alpha*n))
    prefix = checkered[:nprefix]
    assert len(prefix) == nprefix
    return prefix

def get_next_message_grid_sized(arr, dims, min_alpha=None):
    """
    returns a sub-array of arr with shape of dims
    if min_alpha is float, fill the first min_alpha percent of the grid
        with a checkerboard, so that the grid has complexity of at least min_alpha
    """
    if arr.size == 0:
        raise Exception("cannot get a grid from empty array")
    n = reduce(lambda x,y: x*y, dims, 1)
    arr = arr.reshape(-1).tolist()
    if min_alpha:
        prefix = get_conj_grid_prefix(dims, min_alpha)
        assert len(prefix) < n
        arr = prefix + arr
    if len(arr) < n:
        arr += [0]*(len(arr) - n)
    cur_arr, arr = np.array(arr[:n]), np.array(arr[n:])
    cur_arr.resize(dims)
    if min_alpha:
        assert arr_bpcs_complexity(cur_arr) >= min_alpha, '{0} < {1}'.format(arr_bpcs_complexity(cur_arr), min_alpha)
    return cur_arr, arr

def list_to_grids(arr, dims):
    """
    arr is list of bits
    dims is list, len(dims) == 2
    converts each to bits of length dims[0]
        then stacks each char in blocks, where each block.shape == dims
    returns sequence of bits
    """
    area = dims[0]*dims[1]
    rem = (len(arr) % area)
    length_missing = area - rem if rem else 0
    arr += [0]*length_missing
    arr = np.array(arr)
    ngrids = len(arr) / area
    assert len(arr) % area == 0
    return np.resize(arr, [ngrids, dims[0], dims[1]])

def str_to_grids(message, grid_size):
    """
    message is str
    turns message into list of bits, high bits first
    then returns list of bits as grid,
        where each grid is a numpy array with shape == grid_size
    """
    def bits(out):
        """ reads the bits from a str, high bits first """
        bytes = (ord(b) for b in out)
        for b in bytes:
            for i in reversed(xrange(8)):
                yield (b >> i) & 1
    bits_list = list(bits(message))
    # return bits_list
    return list_to_grids(bits_list, grid_size)

def read_message_grids(messagefile, grid_size):
    """
    reads messagefile as bits and returns as list of grids
    where each grid is a numpy array with shape == grid_size
    """
    with open(messagefile, 'r') as f:
        return str_to_grids(f.read(), grid_size)

def grids_to_list(grids):
    """
    grids is list of 2d numpy arrays
    returns list
        inverse of list_to_grids
    """
    grids = [np.array(grid).reshape(-1) for grid in grids]
    return np.hstack(grids).flatten().tolist()

def grids_to_str(grids):
    """
    grids is list of numpy arrays, all of same shape
    combines grids into one long list
        turns into bytes

    source: http://stackoverflow.com/questions/5205487/how-to-write-individual-bits-to-a-text-file-in-python
    """
    bits = grids_to_list(grids)
    nspare = len(bits) % 8
    # bits += [0]*nspare
    # since the message was initially read by the byte
    # any spares must have been added to create a grid
    bits = bits[:len(bits)-nspare]
    nbytes = len(bits) / 8
    bytes = np.resize(np.array(bits), [nbytes, 8])
    byte_to_str = lambda byte: int('0b' + ''.join(str(x) for x in byte.tolist()), 2)
    byte_to_char = lambda byte: chr(byte_to_str(byte))
    return ''.join([byte_to_char(byte) for byte in bytes])

def write_message_grids(outfile, grids):
    """
    grids is list of numpy arrays, all of same shape
    """
    with open(outfile, 'w') as f:
        f.write(grids_to_str(grids))

def get_message_grid_from_grids(mgrids, conj_map):
    """
    mgrids is a list of numpy arrays, each a message grid of bits
    cgrids is a list of numpy array, each a conj_map grid of bits
    conjugates the ith mgrid if cgrids[i] == 1
    and returns altered mgrids
    """
    
    assert len(conj_map) >= len(mgrids), '{0} < {1}'.format(len(conj_map), len(mgrids))
    for i, mgrid in enumerate(mgrids):
        if conj_map[i]:
            mgrids[i] = conjugate(mgrid)
    return mgrids

def get_n_message_grids(nbits_per_map, ngrids):
    """
    nbits_per_map is list, specifying the number of non-trash bits in each grid if it were a conj_map (given its shape)
    ngrids is the total number of grids, be they message or conj_map

    want to find x, the number of message grids, and y, the number of conj_map grids
        s.t. ngrids=x+y and sum(nbits_per_map[-(y-1)]) < x <= sum(nbits_per_map[-y:])
    e.g. if x=34, and nbits_per_map=64 for each conj_map, then ngrids=35, x=34, and y=1 because 0 < 34 < 64
    e.g. if x=160, and nbits_per_map=60 for each conj_map, then ngrids=163, x=160, and y=3 because 2*60 < 160 < 3*60
    """
    x, y = ngrids-1, 1
    is_valid = lambda x, y, ngrids, nbits_per_map: ngrids==x+y and sum(nbits_per_map[-(y-1):]) < x <= sum(nbits_per_map[-y:])
    while not is_valid(x, y, ngrids, nbits_per_map):
        x, y = x-1, y+1
    assert x > 0
    assert y > 0
    return x

def separate_conj_map_from_message(grids, alpha):
    """
    grids is a list of numpy arrays, all of the same size
    returns two lists, representing the message grids and the conj_map grids

    n.b. some percent of each conj_map grid will be junk bits added to keep complexity above alpha
    """
    if not grids:
        return [], []

    get_nignored = lambda grid: len(get_conj_grid_prefix((grid.shape[0], grid.shape[1]), alpha))
    get_nbits_per_map = lambda grid: grid.shape[0]*grid.shape[1] - get_nignored(grid)
    nbits_per_map = [get_nbits_per_map(grid) for grid in grids]

    ngrids = len(grids)
    x = get_n_message_grids(nbits_per_map, ngrids)
    log.critical('Found {0} message grids and {1} conjugation maps'.format(x, ngrids-x))
    return grids[:x], grids[x:], nbits_per_map[x:]

def get_conj_map(cgrids, nbits_per_map):
    """
    cgrids is list of np.arrays, each of them a conjugation map
    nbits_per_map is a list where the ith element stores the number of bits in the ith conj_map to keep
        since some percent of each conj_map grid will be junk bits added to keep complexity above alpha
    """
    cgrids = [grid.reshape(-1).tolist()[-nbits_per_map[i]:] for i, grid in enumerate(cgrids)]
    conj_map = np.hstack(cgrids).reshape(-1).tolist()
    assert len(conj_map) == sum(nbits_per_map), '{0} != {1}'.format(len(conj_map), sum(nbits_per_map))
    return conj_map

def write_conjugated_message_grids(outfile, grids, alpha):
    messages, conj_map_grids, nbits_per_map = separate_conj_map_from_message(grids, alpha)
    conj_map = get_conj_map(conj_map_grids, nbits_per_map)
    message_grids = get_message_grid_from_grids(messages, conj_map)
    write_message_grids(outfile, message_grids)
