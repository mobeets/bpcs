import numpy as np

class BitPlane:
    """
    slices or stacks values in a numpy array's last dimension
    """
    def __init__(self, arr):
        self.arr = arr

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
        new_arr = self.arr
        return new_arr

    def stack(self):
        """
        the reverse of slicing
        """
        new_arr = self.arr
        return new_arr
