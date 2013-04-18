from math import ceil
from numpy.lib.stride_tricks import as_strided as ast

def error(base, msg, is_fatal=False):
    error_msg = 'ERROR (' + base + '): ' + msg
    if is_fatal:
        raise Exception(error_msg)
    else:
        print error_msg

"""
TO DO:
    * fix adjust_grid_inds
    * write iterator over grids
    * write test cases
    * make sure I am even accessing the correct dims of self.arr?
"""

class Grid:
    """ for gridding the first 2-dims of an array """
    def __init__(self, arr, grid_size):
        self.arr = arr
        self.grid_size = grid_size
        self.dims = self.get_grid_dims()

    def get_grid_dims(self):
        """
        calculates the max indices for accessing the grids of self.arr
        """
        assert len(self.grid_size) == 2
        ngrids = lambda x, ngrids: int(ceil(x*1.0/ngrids))
        grid_counts = [ngrids(self.arr.shape[i], self.grid_size[i]) for i in range(2)]
        shape_dims = [self.arr.shape[i] for i in range(2, len(self.arr.shape))]
        return grid_counts + shape_dims

    def grid_view(self, inds):
        """
        inds is list, the indices of the grid desired
            e.g. if inds == [i,j,k] it gets the ith block down, the jth block right, the kth block deep
            note: len(inds) == len(self.arr.shape)
            (blocks are 0-indexed)
        corrects the indices accessing self.arr where they would access outside the dims
        and returns the grid accessed using those indices
        """
        if len(inds) != len(self.dims):
            error("Grid", "Invalid inds sized " + str(len(inds)) + " should be length " + str(len(self.dims)))
        if not all([a < b for a, b in zip(inds, self.dims)]):
            error("Grid", "Invalid grid inds: " + str(inds))
        block = self.adjust_grid_inds((self.dims[0], self.dims[1]), (inds[0], inds[1]))
        shape = (self.arr.shape[0] / block[0], self.arr.shape[1] / block[1]) + block
        strides = (block[0] * self.arr.strides[0], block[1] * self.arr.strides[1]) + self.arr.strides
        error("Grid", "need to use inds[2:] to access currect slice of self.arr")
        cur_arr = self.arr # FIXME
        return ast(cur_arr, shape=shape, strides=strides)

    def adjust_grid_inds((bx, by), (i,j)):
        """
        (bx, by) is the desired block shape
        (i, j) is the location of the block in the image
        verifies the the (i,j)th block would not cross the image bounds,
            and if it would, returns an altered block size

        e.g. image is 7-by-9 => (self.i, self.j) is (3, 3)
            (bx, by) is (3, 3)
            (i, j) is (2, 2)
            => (1, 3)
        """
        bx2, by2 = bx, by
        if i == self.i-1:
            bx2 = bx - ((self.i * bx) - self.nrows)
        if j == self.j-1:
            by2 = by - ((self.j * by) - self.ncols)
        return bx2, by2
