import numpy as np

from .logger import log
from .array_grid import get_next_grid_dims
from .act_on_image import ActOnImage
from .array_message import write_conjugated_message_grids
from .bpcs_steg import arr_bpcs_complexity

def remove_message_from_vessel(arr, alpha, grid_size):
    messages = []
    nfound, nkept, nleft = 0, 0, 0
    complexities = []
    for dims in get_next_grid_dims(arr, grid_size):
        nfound += 1
        grid = arr[tuple(dims)]
        cmplx = arr_bpcs_complexity(grid)
        if cmplx < alpha:
            nleft += 1
            continue
        complexities.append(cmplx)
        nkept += 1
        messages.append(grid)
    assert nfound == nkept + nleft
    log.critical('Found {0} out of {1} grids with complexity above {2}'.format(nkept, nfound, alpha))
    return messages

class BPCSDecodeImage(ActOnImage):
    def modify(self, alpha):
        return remove_message_from_vessel(self.arr, alpha, (8,8))

def decode(infile, outfile, alpha=0.45):
    x = BPCSDecodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    grids = x.modify(alpha)
    write_conjugated_message_grids(outfile, grids, alpha)
