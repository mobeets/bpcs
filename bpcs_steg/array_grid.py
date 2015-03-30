import itertools
from logger import log

def get_next_grid_dims(arr, dims):
    """
    arr is a numpy array of shape [x0, x1, ..., xN]
    dims is a 2d array, the shape of the grid
        where each 'grid' is arr[dims[0], dims[1], i2, i3, ..., iN]
        for some i2, i3, ..., iN

    iterates through the grids of arr
        starting by iterating from 0..xN, then 0..xN-1, ..., 0..x2
        and in the first two dimensions, from left-to-right and then top-to-bottom
    e.g. if arr.shape == [4,4,2,2] and dims == [4,4]
        returns:
            arr[:,:,0,0]
            arr[:,:,0,1]
            arr[:,:,1,0]
            arr[:,:,1,1]
    """
    nrows, ncols = arr.shape[0], arr.shape[1]
    rows_per_grid, cols_per_grid = dims[0], dims[1]

    def get_inds(total_length, grid_length):
        lefts = range(0, total_length, grid_length)
        rights = [min(total_length, left+grid_length) for left in lefts]
        return zip(lefts, rights)
    xs = get_inds(nrows, rows_per_grid)
    ys = get_inds(ncols, cols_per_grid)

    nlayers = len(arr.shape)-2
    assert nlayers > 0
    inds = [range(arr.shape[i+2]) for i in range(nlayers)]
    zs = itertools.product(*inds)
    ngrids = reduce(lambda x,y: x*y, [len(x) for x in inds], 1)*len(xs)*len(ys)
    log.critical('Found {0} grids'.format(ngrids))
    i = 0
    for z in zs:
        for (xleft, xright) in xs:
            for (yleft, yright) in ys:
                i += 1
                if i % 10000 == 0:
                    log.critical('Grid {0} of {1}'.format(i, ngrids))
                yield [slice(xleft, xright), slice(yleft, yright)] + list(z)

if __name__ == '__main__':
    pass
