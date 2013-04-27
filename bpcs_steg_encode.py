import numpy as np

from logger import log

from act_on_image import ActOnImage
from array_message import read_message_grids, get_next_message_grid_sized
from array_grid import get_next_grid_dims
from bpcs_steg import arr_bpcs_complexity, conjugate

ALIVE, CONJUGATING, DEAD = 0,1,2
def get_message_and_status(message, dims, conjugated, status):
    """
    message is remaining message to be embedded
    dims is shape of next desired grid
    conjugated is list of bool, specifying whether each past message grid was conjugated or not
    status is int
        DEAD means we shouldn't be embedding any more messages
        ALIVE means we need the next grid from message
        CONJUGATING means we need the next grid from conjugated
    """
    assert status != DEAD
    if status == CONJUGATING and len(conjugated) == 0:
        return None, None, None, DEAD
    elif (status == ALIVE and message.size == 0) or (status == CONJUGATING):
        cur, conjugated = get_next_message_grid_sized(np.array(conjugated), dims)
        conjugated = conjugated.tolist()
        return cur, None, conjugated, CONJUGATING
    elif status == ALIVE:
        cur, message = get_next_message_grid_sized(message, dims)
        return cur, message, conjugated, ALIVE

def embed_message_in_vessel(arr, alpha, message, grid_size):
    conjugated = []
    status = ALIVE
    for dims in get_next_grid_dims(arr, grid_size):
        grid = arr[dims]
        if arr_bpcs_complexity(grid) < alpha:
            continue
        cur_message, message, conjugated, status = get_message_and_status(message, grid.shape, conjugated, status)
        if status == DEAD:
            # since there is no more embedding to do, flip the remaining grids you find
            # so that they are not mistaken for signal grids when decoding
            arr[dims] = conjugate(grid)
            continue
        if arr_bpcs_complexity(cur_message) < alpha and status == ALIVE:
            cur_message = conjugate(cur_message)
            conjugated.append(True)
        elif status == ALIVE:
            conjugated.append(False)
        assert cur_message.shape == grid.shape
        arr[dims] = cur_message
    if message.size > 0:
        raise Exception("Could not fit message in arr. Still had {0} bits left".format(message.size))
    elif status != DEAD:
        raise Exception("Could not fully embed conjugation head in arr.")
    return arr, None

class BPCSEncodeImage(ActOnImage):
    def modify(self, messagefile, alpha):
        new_arr = np.array(self.arr, copy=True)
        message_grids = read_message_grids(messagefile, (8,8))
        return embed_message_in_vessel(new_arr, alpha, message_grids, (8,8))

def bpcs_steg_encode(infile, messagefile, outfile, alpha):
    BPCSEncodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr = x.modify(messagefile, alpha)
    x.write(outfile, arr)

if __name__ == '__main__':
    infile = 'docs/vessel_mini.png'
    messagefile = 'docs/message.txt'
    outfile = infile.replace('.', '_encoded.')
    alpha 0.45
    bpcs_steg_encode(infile, messagefile, outfile, alpha)
