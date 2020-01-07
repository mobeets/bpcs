import numpy as np

from .logger import log
from .act_on_image import ActOnImage
from .array_message import read_message_grids, get_next_message_grid_sized
from .array_grid import get_next_grid_dims
from .bpcs_steg import arr_bpcs_complexity, conjugate

ALIVE, CONJUGATING, DEAD = 0,1,2
def get_message_and_status(message, dims, conjugated, status, alpha):
    """
    message is remaining message to be embedded
    dims is shape of next desired grid
    conjugated is list of bool, specifying whether each past message grid was conjugated or not
    status is int
        DEAD means we shouldn't be embedding any more messages
        ALIVE means we need the next grid from message
        CONJUGATING means we need the next grid from conjugated
    """
    if status == DEAD:
        return None, None, None, DEAD
    elif status == CONJUGATING and len(conjugated) == 0:
        return None, None, None, DEAD
    elif (status == ALIVE and message.size == 0) or (status == CONJUGATING):
        cur, conjugated = get_next_message_grid_sized(np.array(conjugated), dims, min_alpha=alpha)
        conjugated = conjugated.tolist()
        return cur, None, conjugated, CONJUGATING
    elif status == ALIVE:
        cur, message = get_next_message_grid_sized(message, dims)
        return cur, message, conjugated, ALIVE

def embed_message_in_vessel(arr, alpha, message, grid_size):
    """
    want all o.g. grids to have complexity < alpha
    if you find one greater than alpha
    replace it with message
    if message complexity < alpha, conjugate message
    """
    conjugated = []
    status = ALIVE
    nmessgs, nmaps, nleft, ngrids = 0, 0, 0, 0
    for dims in get_next_grid_dims(arr, grid_size):
        ngrids += 1
        grid = arr[tuple(dims)]
        if arr_bpcs_complexity(grid) < alpha:
            nleft += 1
            continue
        cur_message, message, conjugated, status = get_message_and_status(message, grid.shape, conjugated, status, alpha)
        if status == DEAD:
            # since there is no more embedding to do, flip the remaining grids you find
            # so that they are not mistaken for signal grids when decoding
            cur_message = np.zeros(grid.shape, dtype=np.uint8)
            if not arr_bpcs_complexity(cur_message) < alpha:
                a = arr_bpcs_complexity(grid)
                b = arr_bpcs_complexity(cur_message)
                raise Exception('Error fixing vessel grid to have complexity below alpha: {0} => {1}'.format(a, b))
            nleft += 1
        if status == ALIVE and arr_bpcs_complexity(cur_message) < alpha:
            cur_message = conjugate(cur_message)
            if not arr_bpcs_complexity(cur_message) >= alpha:
                a = arr_bpcs_complexity(conjugate(cur_message))
                b = arr_bpcs_complexity(cur_message)
                raise Exception('Error fixing message grid to have complexity above alpha: {0} => {1}'.format(a, b))
            nmessgs += 1
            conjugated.append(True)
        elif status == ALIVE:
            nmessgs += 1
            conjugated.append(False)
        elif status == CONJUGATING:
            nmaps += 1
        assert cur_message.shape == grid.shape
        arr[tuple(dims)] = cur_message
    if message is not None and message.size > 0:
        raise Exception("Could not fit message in arr. Still had {0} bits left".format(message.size))
    elif status != DEAD:
        raise Exception("Could not fully embed conjugation head in arr.")
    nfound = nmessgs + nmaps + nleft
    assert nmessgs + nmaps + nleft == ngrids, '{0} + {1} + {2} = {4} != {3}'.format(nmessgs, nmaps, nleft, ngrids, nfound)
    log.critical('Embedded {0} message grids and {1} conjugation maps'.format(nmessgs, nmaps))
    return arr

class BPCSEncodeImage(ActOnImage):
    def modify(self, messagefile, alpha):
        new_arr = np.array(self.arr, copy=True)
        message_grids = read_message_grids(messagefile, (8,8))
        return embed_message_in_vessel(new_arr, alpha, message_grids, (8,8))

def encode(infile, messagefile, outfile, alpha=0.45):
    x = BPCSEncodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    arr = x.modify(messagefile, alpha)
    x.write(outfile, arr)
