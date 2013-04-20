import numpy as np

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

def grids_to_list(grids):
    """
    grids is list of 2d numpy arrays
    returns list
        inverse of list_to_grids
    """
    return np.vstack(grids).flatten().tolist()

def str_to_grids(message, params):
    """
    message is str
    turns message into list of bits, high bits first
    then returns list of bits as grid,
        where each grid is a numpy array with shape == params.grid_size
    """
    def bits(out):
        """ reads the bits from a str, high bits first """
        bytes = (ord(b) for b in out)
        for b in bytes:
            for i in reversed(xrange(8)):
                yield (b >> i) & 1
    bits_list = list(bits(message))
    return list_to_grids(bits_list, params.grid_size)

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

def read_message_grids(messagefile, params):
    """
    reads messagefile as bits and returns as list of grids
    where each grid is a numpy array with shape == params.grid_size
    """
    with open(messagefile, 'r') as f:
        return str_to_grids(f.read(), params)

def write_message_grids(outfile, grids):
    """
    grids is list of numpy arrays, all of same shape
    """
    with open(outfile, 'w') as f:
        f.write(grids_to_str(grids))
