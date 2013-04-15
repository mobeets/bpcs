import numpy as np

class BitPlane:
    """
    slices or stacks values in a numpy array's last dimension
    """
    def __init__(self, arr):
        self.arr = arr

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
