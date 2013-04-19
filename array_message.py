
def list_to_grids(arr, dims):
    """
    arr is list of bits
    dims is list, len(dims) == 2
    converts each to bits of length dims[0]
        then stacks each char in blocks, where each block.shape == dims
    returns sequence of bits
    """
    length_missing = (dims[0]*dims[1]) - (len(arr) % (dims[0]*dims[1]))
    arr = np.array(arr + [0]*length_missing)
    ngrids = len(arr) / (dims[0]*dims[1])
    assert len(arr) % (dims[0]*dims[1]) == 0
    return np.resize(arr, [dims[0], dims[1], ngrids])

def get_message_grids(messagefile, params):
    """
    reads messagefile as bits and returns as list of grids
    where each grid is a numpy array with shape == params.grid_size

    source: http://stackoverflow.com/questions/5205487/how-to-write-individual-bits-to-a-text-file-in-python

    NOTE: may want to read differently? not necessarily reading as ascii...
    """
    def bits(f):
        """ reads the bits from a file, high bits first """
        bytes = (ord(b) for b in f.read())
        for b in bytes:
            for i in reversed(xrange(8)):
                yield (b >> i) & 1
    # FIXME
    message = list(bits(open(messagefile, 'r')))
    return list_to_grids(message, params.grid_size)

def grids_to_list(grids):
    return np.vstack(grids).flatten().to_list()

def grids_to_str(grids):
    """
    grids is list of numpy arrays, all of same shape
    combines grids into one long list
        turns into bytes

    source: http://stackoverflow.com/questions/5205487/how-to-write-individual-bits-to-a-text-file-in-python
    """
    # FIXME
    bits = grids_to_list(grids)

def write_message_grids(outfile, grids):
    """
    grids is list of numpy arrays, all of same shape
    """
    with open(outfile, 'w') as f:
        f.write(grids_to_str(grids))
