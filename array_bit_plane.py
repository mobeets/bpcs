import numpy as np

def xor_lists(a, b):
    assert len(a) == len(b)
    return [x ^ y for x,y in zip(a,b)]

"""
TO CODE:
    * iterate_pixels
    * conjugate
    * BitPlane.slice()
    * BitPlane.stack()

TO DO:
    * image complexity
    * test cases
"""

def iterate_pixels(arr):
    """
    arr is a numpy array
    yields successive pixels in arr
        where each pixel might be multiple dimensions
        e.g. bit-planed and/or layered
    """
    # FIXME
    yield arr

def arr_map(arr, fcn):
    """
    arr is a bit-planed numpy array

    returns arr with fcn applied to each pixel in arr
        where pixel is defined in iterate_pixels
    """
    for pixel in iterate_pixels(arr):
        pixels = fcn(pixel)
    return arr

def pbc_to_cgc(arr):
    """
    arr is a numpy array, in PBC (pure binary code)

    converts arr to CGC (canonical gray code)
    g_1 == b_1
    g_i == b_i XOR b_i-1

    assert pbc_to_cgc(cgc_to_pbc(arr)) == arr
    assert cgc_to_pbc(pbc_to_cgc(arr)) == arr
    """
    def pbc_to_cgc_mapper(planes):
        new_planes = []
        for i, plane in enumerate(planes):
            if i == 0:
                new_planes.append(planes[i])
            else:
                new_planes.append(xor_lists(planes[i], planes[i-1]))
        return np.array(new_planes)
    return arr_map(arr, pbc_to_cgc_mapper)

def cgc_to_pbc(arr):
    """
    arr is a numpy array, in CGC (canonical gray code)

    converts arr to PBC (pure binary code)
    b_1 == g_1
    b_i == g_i XOR b_i-1

    assert pbc_to_cgc(cgc_to_pbc(arr)) == arr
    assert cgc_to_pbc(pbc_to_cgc(arr)) == arr
    """
    def cgc_to_pbc_mapper(planes):
        new_planes = []
        for i, plane in enumerate(planes):
            if i == 0:
                new_planes.append(planes[i])
            else:
                new_planes.append(xor_lists(planes[i], new_planes[i-1]))
        return np.array(new_planes)
    return arr_map(arr, cgc_to_pbc_mapper)

def conjugate(arr):
    """
    arr is a numpy array

    conjugates arr so that its complexity, s, is 1-s
    assert conjugate(conjugate(arr)) == arr
    """
    # FIXME
    return arr

class BitPlane:
    """
    slices or stacks values in a numpy array's last dimension
    optionally grays the resulting bits
    """
    def __init__(self, arr, gray=False):
        self.arr = arr
        self.gray = gray

    def bin_strs_to_decimal(self, vals):
        """
        vals is list of int, each val either 0 or 1
        returns the decimal value from concatenating vals
        """
        return int(''.join([str(x) for x in vals]),2)

    def decimal_to_bin_strs(self, val, nbits):
        """
        val is int
        nbits is int
        returns val as list of int, each either 0 or 1,
            representing val in base-2 using nbits
        """
        return [int(x) for x in bin(val)[2:].zfill(nbits)]

    def slice(self, nbits):
        """
        converts the values in the last dimension of self.arr into binary
            and then splits them into new arrays for each bit
        """
        # FIXME
        if self.gray:
            self.arr = pbc_to_cgc(self.arr)
        return self.arr

    def stack(self):
        """
        the reverse of slicing
        """
        if self.gray:
            self.arr = cgc_to_pbc(self.arr)
        # FIXME
        return self.arr
