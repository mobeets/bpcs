import numpy as np
from logger import log
from array_grid import get_next_grid_dims
from act_on_image import ActOnImage
from array_message import write_conjugated_message_grids

def remove_message_from_vessel(arr, alpha, grid_size):
    messages = []
    for dims in get_next_grid_dims(arr, grid_size):
        grid = arr[dims]
        if arr_bpcs_complexity(grid) < alpha:
            continue
        messages.append(grid)
    return messages

class BPCSDecodeImage(ActOnImage):
    def modify(self, alpha):
        return remove_message_from_vessel(self.arr, alpha, (8,8))

def bpcs_steg_decode(infile, outfile, alpha):
    BPCSDecodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    grids = x.modify(alpha)
    write_conjugated_message_grids(outfile, grids)

if __name__ == '__main__':
    infile = 'docs/vessel_small_encoded.png'
    outfile = infile.replace('_encoded.png', '_message.txt')
    alpha 0.45
    bpcs_steg_decode(infile, outfile, alpha)
