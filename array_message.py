import numpy as np

def get_next_message_grid_sized(arr, dims):
    """
    returns a sub-array of arr with shape of dims
    """
    if arr.size == 0:
        raise Exception("cannot get a grid from empty array")
    n = reduce(lambda x,y: x*y, dims, 1)
    arr = arr.reshape(-1).tolist()
    if len(arr) < n:
        arr += [0]*(len(arr) - n)
    cur_arr, arr = np.array(arr[:n]), np.array(arr[n:])
    cur_arr.resize(dims)
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
    return np.vstack(grids).flatten().tolist()

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

def get_message_grid_from_grids(mgrids, cgrids):
    """
    mgrids is a list of numpy arrays, each a message grid of bits
    cgrids is a list of numpy array, each a conj_map grid of bits
    conjugates the ith mgrid if cgrids[i] == 1
    and returns altered mgrids
    """
    conj_map = np.vstack(cgrids).reshape(-1).tolist()
    for i, mgrid in enumerate(mgrids):
        if conj_map(i):
            mgrids[i] = conjugate(mgrid)
    return mgrids

def separate_conj_map_from_message(grids):
    """
    grids is a list of numpy arrays, all of the same size
    want to find x, the number of message grids, and y, the number of conj_map grids
        s.t. m=x+y and n*(y-1) < x <= n*y
        e.g. if x=34, and n=64, then m=35, x=34, and y=1 because 0 < 34 < 64
        e.g. if x=160, and n=60, then m=163, x=160, and y=3 because 2*60 < 160 < 3*60
    returns two lists, representing the message grids and the conj_map grids
    """
    if not grids:
        return [], []
    n = reduce(lambda x,y: x*y, grids[0].shape, 1)
    m = len(messages)
    x, y = m-1, 1
    is_valid = lambda x,y,m,n: m==x+y and (n*(y-1) < x <= n*y)
    while not is_valid(x,y,m,n):
        x, y = x-1, y+1
    assert x > 0
    assert y > 0
    return messages[:x], messages[x:]

def write_conjugated_message_grids(outfile, grids):
    messages, conj_maps = separate_conj_map_from_message(grids)
    message_grids = get_message_grid_from_grids(messages, conj_maps)
    write_message_grids(outfile, message_grids)
