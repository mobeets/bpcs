import numpy as np
import matplotlib.pyplot as plt

from logger import log

from act_on_image import ActOnImage
from bpcs_steg import arr_bpcs_complexity, conjugate, max_bpcs_complexity
from array_message import get_n_message_grids
from array_grid import get_next_grid_dims

def histogram_of_complexity(arr, grid_size, alpha, comp_fcn):
    log.critical('Creating histograms of image complexity...')
    max_complexity = max_bpcs_complexity(*grid_size)
    vals = [arr_bpcs_complexity(arr[dims]) for dims in get_next_grid_dims(arr, grid_size)]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ns, bins, patches = ax.hist(vals, 200, facecolor='red', alpha=0.75)

    navail = sum([n for n, bin in zip(ns, bins) if comp_fcn(bin, alpha)])
    return fig, navail, sum(ns)

def flip_image_complexity(arr, alpha, comp_fcn, grid_size):
    n = 0
    for dims in get_next_grid_dims(arr, grid_size):
        grid = arr[dims]
        if comp_fcn(arr_bpcs_complexity(grid), alpha): # < or >
            n += 1
            init_grid = np.copy(grid)
            arr[dims] = conjugate(grid)
            assert abs((1 - arr_bpcs_complexity(init_grid)) - arr_bpcs_complexity(grid)) < 0.01
            assert not(arr[dims].tolist() == init_grid.tolist() and alpha != 0.5)
    log.critical('Conjugated {0} grids'.format(n))
    # histogram_of_complexity(arr, params)
    return arr, n

class HistogramComplexityImage(ActOnImage):
    def modify(self, alpha, comp_fcn, grid_size=(8,8)):
        hist, navail, ntotal = histogram_of_complexity(self.arr, grid_size, alpha, comp_fcn)
        print '{0} of {1} grids available with alpha of {2}'.format(navail, ntotal, alpha)
        nbits_per_grid = grid_size[0]*grid_size[1]
        nbytes = (get_n_message_grids(nbits_per_grid, navail)*nbits_per_grid)/8.0
        print '{0} bytes of storage space can fit in this vessel image'.format(nbytes)
        return hist

class ComplexifyImage(ActOnImage):
    def modify(self, alpha, grid_size=(8,8)):
        new_arr = np.array(self.arr, copy=True)
        return flip_image_complexity(new_arr, alpha, lambda x,thresh: x>=thresh, grid_size)

class SimplifyImage(ActOnImage):
    def modify(self, alpha, grid_size=(8,8)):
        new_arr = np.array(self.arr, copy=True)
        return flip_image_complexity(new_arr, alpha, lambda x,thresh: x<thresh, grid_size)

def histogram(infile, outfile, alpha, comp_fcn):
    x = HistogramComplexityImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    hist = x.modify(alpha, comp_fcn)
    hist.savefig(outfile)
    plt.show()

def complexify(infile, outfile, alpha):
    x = ComplexifyImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr, stats = x.modify(alpha)
    x.write(outfile, arr)
    return stats

def simplify(infile, outfile, alpha):
    x = SimplifyImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr, stats = x.modify(alpha)
    x.write(outfile, arr)
    return stats

if __name__ == '__main__':
    infile = 'docs/vessel_mini.png'
    outfile = infile.replace('.png', '_complexity_hist.png')
    alpha = 0.45
    greater = lambda x,thresh: x>=thresh
    lesser = lambda x,thresh: x<thresh
    histogram(infile, outfile, alpha, greater)
