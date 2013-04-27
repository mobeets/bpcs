import numpy as np
import matplotlib.pyplot as plt

from logger import log

from act_on_image import ActOnImage
from bpcs_steg import arr_bpcs_complexity, conjugate
from array_grid import get_next_grid_dims

def histogram_of_complexity(arr, grid_size):
    log.critical('Creating histograms of image complexity...')
    vals = [arr_bpcs_complexity(arr[dims]) for dims in get_next_grid_dims(arr, grid_size)]
    fig = plt.figure()
    ax = fig.add_subplot(211)
    n, bins, patches = ax.hist(vals, 200, facecolor='red', alpha=0.75)
    # ax = fig.add_subplot(212)
    # n, bins, patches = ax.hist(vals2, 200, facecolor='red', alpha=0.75)
    # plt.show()
    return fig

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
    def modify(self):
        return histogram_of_complexity(self.arr, (8,8))

class ComplexifyImage(ActOnImage):
    def modify(self, alpha):
        new_arr = np.array(self.arr, copy=True)
        return flip_image_complexity(new_arr, alpha, lambda x,thresh: x>=thresh, (8,8))

class SimplifyImage(ActOnImage):
    def modify(self, alpha):
        new_arr = np.array(self.arr, copy=True)
        return flip_image_complexity(new_arr, alpha, lambda x,thresh: x<thresh, (8,8))

def histogram(infile, outfile):
    x = HistogramComplexityImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    hist = x.modify()
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
    infile = 'docs/vessel_small.png'
    outfile = infile.replace('.png', '_complexity_hist.png')
    histogram(infile, outfile)
