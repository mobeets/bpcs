"""
source: http://web.eece.maine.edu/~eason/steg/SPIE98.pdf

A.
    * read image as n-bit plane
    * show n-bit plane as image

B.
    * get n-bit image as n bit planes
        - e.g. n-by-m 8-bit image has pixels each as 0-255 => 8 n-by-m images with pixels as 0-1
    * combine n bit planes as one n-bit plane

C.
    * PBC (pure binary code) to CGC (gray code)
        - see: http://www.datahide.com/BPCSe/pbc-vs-cgc-e.html
        1. 1st most significant bit plane in CGC is just the PBC one
        2. given ith most significant bit plane in PBC, bit plane i in CGC becomes bit plane i in PBC XOR bit plane i-1 in PBC
    * CGC to PBC

D. 
    * file to list of bytes
    * list of bytes to list of 8-bytes each

E. conjugate block (see source)

F. calculate image complexity of block
    * k = sum of bit flips along each row and column of block
    * max_k = maximum number of k given an n-by-m block
    * returns k/max_k

ENCODING
    * read file as n bit planes
    * PBC to CGC
    * segment each bit plane into blocks
    
    * mark each block as either simple or complex using threshold
    * conjugate each secret block if its complexity is below threshold
        - store this act in conjugation map
    
    * insert secret blocks using ordering defined
        - extra secret blocks are header (defining orderings?, and conjugation map)
    * CGC to PBC
    * write image

* set info-threshold alpha (suggested alpha = 0.3)
* define function for sorting an image's blocks given its n bit planes
* define function for ordering a secret file's blocks
* define subset indices of complex blocks of image to be replaced with secret blocks
"""

from math import ceil
import numpy as np
from numpy.lib.stride_tricks import as_strided as ast
import Image
# source: http://www.pythonware.com/library/pil/handbook/image.htm
GRIDSIZE = 8
BASE_BLOCK = (GRIDSIZE, GRIDSIZE)
NBITS_PER_LAYER = 8

class ImageGrid:
    def __init__(self, infile, as_rgb=True):
        self.arr = self.load(infile)
        self.ncols, self.nrows, self.nlayers = self.arr.shape
        self.x, self.y, self.z = self.grid_size(self.ncols, self.nrows, self.nlayers)

    def load(self, infile, as_rgb):
        self.im = Image.open(infile)
        self.im.convert('RGB' if as_rgb else 'L')
        return np.array(self.im)

    def write(self, outfile):
        assert '.' + self.im.mode in outfile.upper()
        self.im.putdata(self.arr)
        self.im.save(outfile, self.im.mode)

    def block_view(self, (i,j,k)):
        """
        gets the ith block down, the jth block right, the kth block deep
            (blocks are 0-indexed)
        correcting the block size where it goes over the image bounds
        """
        assert (i < self.x) and (j < self.y) and (k < self.z)
        block = self.adjust_block(BASE_BLOCK, (i,j))
        shape = (self.arr.shape[0]/ block[0], self.arr.shape[1]/ block[1])+ block
        strides = (block[0]* self.arr.strides[0], block[1]* self.arr.strides[1])+ self.arr.strides
        return ast(self.arr, shape=shape, strides=strides)

    def adjust_block((bx, by), (i,j)):
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

    def grid_size(self, ncols, nrows, nlayers):
        ngrids = lambda dim: int(ceil(dim*1.0/GRIDSIZE))
        nbitsdeep = NBITS_PER_LAYER*nlayers
        return ngrids(ncols), ngrids(nrows), nbitsdeep

def main(infile, outfile):
    x = ImageGrid(infile, True)
    print x.block_view((0,0,0))
    print x.block_view((61,0,0))

if __name__ == '__main__':
    infile = 'vessel.png'
    outfile = 'vessel_out.png'
    main(infile, outfile)
