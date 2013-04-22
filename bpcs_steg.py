from act_on_image import act_on_image, Params
from array_message import read_message_grids, get_next_message_grid_sized
from array_grid import get_next_grid_dims
import numpy as np

def arr_bpcs_complexity(arr):
    """
    arr is a 2-d numpy array
    returns the fraction of maximum bpcs_complexity in arr
        where bpcs_complexity is total sum of bit changes
        moving along each row and each column
    """
    nrows, ncols = arr.shape
    max_complexity = ((nrows-1)*ncols) + ((ncols-1)*nrows)
    nbit_changes = lambda items, length: sum([items[i] ^ items[i-1] for i in range(1, length)])
    k = 0
    for row in arr:
        k += nbit_changes(row, ncols)
    for col in arr.transpose():
        k += nbit_changes(col, nrows)
    return (k*1.0)/max_complexity

def checkerboard(h, w):
    """
    h, w are int
    returns a checkerboard array of shape == [h,w]
    """
    re = np.r_[ (w/2)*[0,1] + ([0] if w%2 else [])]
    ro = 1-re
    return np.row_stack(h/2*(re,ro) + ((re,) if h%2 else ()))

def conjugate(arr):
    """
    arr is a numpy array

    conjugates arr so that its complexity, s, is 1-s
    assert conjugate(conjugate(arr)) == arr
    """
    wc = checkerboard(arr.shape[0], arr.shape[1]) # white pixel at origin
    bc = 1-wc # black pixel at origin
    return np.array([[wc[i,j] if arr[i,j] else bc[i,j] for j, cell in enumerate(row)] for i, row in enumerate(arr)])

def eliminate_image_complexity(arr, params):
    alpha = params.custom['alpha']
    for dims in get_next_grid_dims(arr, params.grid_size):
        grid = arr[dims]
        if arr_bpcs_complexity(grid) < alpha:
            grid = conjugate(grid)
    return arr

def embed_message_in_vessel(arr, params):
    alpha = params.custom['alpha']
    get_next_message_grid = lambda x,y: get_next_message_grid_sized(params.custom['message_grids'], (x, y))
    conjugated = []
    i = 0
    for dims in get_next_grid_dims(arr):
        grid = arr[dims]
        if not arr_bpcs_complexity(grid) < alpha:
            # not sure if we're supposed to remove all complexities in o.g. image
            # i.e. stop placing messages and just conjugate grids under alpha...
            continue
        # get next message_grid
        cur_message = get_next_message_grid(nrows, ncols)
        # conjugate if necessary, keep track of message_grids conjugated
        if arr_bpcs_complexity(cur_message) < alpha:
            cur_message = conjugate(cur_message)
            conjugated.append(i)
        i += 1
        # replace grid with message_grid
        grid = cur_message
    return arr

def get_params(action):
    # ['nbits_per_layer', 'grid_size', 'as_rgb', 'gray', 'modifier', 'custom']
    if action == 'eliminate_image_complexity':
        params = Params(8, (8,8), True, True, eliminate_image_complexity, {'alpha': 0.3})
    elif action == 'bpcs':
        params = Params(8, (8,8), True, True, embed_message_in_vessel, {'alpha': 0.3, 'message_grids': ''})
    return params

def remove_complexity(infile, outfile):
    params = get_params('eliminate_image_complexity')
    act_on_image(infile, outfile, params)

def bpcs_steg(infile, messagefile, outfile):
    params = get_params('bpcs')
    message_grids = read_message_grids(messagefile, params)
    params.custom['message_grids'] = message_grids
    act_on_image(infile, outfile, params)

if __name__ == '__main__':
    infile = 'docs/vessel.png'
    remove_complexity(infile, infile.replace('.', '_old.'))
