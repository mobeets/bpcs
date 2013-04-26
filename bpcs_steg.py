from act_on_image import act_on_image, Params
from array_message import read_message_grids, get_next_message_grid_sized
from array_grid import get_next_grid_dims
import numpy as np
import matplotlib.pyplot as plt
from logger import log

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

def histogram_of_complexities(arr1, arr2, params):
    log.critical('Creating histograms of image complexity...')
    vals1 = [arr_bpcs_complexity(arr1[dims]) for dims in get_next_grid_dims(arr1, params.grid_size)]
    vals2 = [arr_bpcs_complexity(arr2[dims]) for dims in get_next_grid_dims(arr2, params.grid_size)]
    fig = plt.figure()
    ax = fig.add_subplot(211)
    n, bins, patches = ax.hist(vals1, 200, facecolor='red', alpha=0.75)
    ax = fig.add_subplot(212)
    n, bins, patches = ax.hist(vals2, 200, facecolor='red', alpha=0.75)
    plt.show()

def flip_image_complexity(arr, params):
    alpha = params.custom['alpha']
    comp = params.custom['comparator']
    # arr1 = np.copy(arr)
    n = 0
    for dims in get_next_grid_dims(arr, params.grid_size):
        grid = arr[dims]
        if comp(arr_bpcs_complexity(grid), alpha): # < or >
            n += 1
            init_grid = np.copy(grid)
            arr[dims] = conjugate(grid)
            assert abs((1 - arr_bpcs_complexity(init_grid)) - arr_bpcs_complexity(grid)) < 0.01
            assert not(arr[dims].tolist() == init_grid.tolist() and alpha != 0.5)
    log.critical('Conjugated {0} grids'.format(n))
    # histogram_of_complexities(arr1, arr, params)
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
    if action == 'eliminate_image_simplicity':
        params = Params(8, (8,8), True, False, flip_image_complexity, {'alpha': 0.3, 'comparator': lambda x,thresh: x<thresh})
    elif action == 'eliminate_image_complexity':
        params = Params(8, (8,8), True, False, flip_image_complexity, {'alpha': 0.7, 'comparator': lambda x,thresh: x>thresh})
    elif action == 'bpcs':
        params = Params(8, (8,8), True, True, embed_message_in_vessel, {'alpha': 0.3, 'message_grids': ''})
    return params

def remove_simplicity(infile, outfile):
    params = get_params('eliminate_image_simplicity')
    act_on_image(infile, outfile, params)

def remove_complexity(infile, outfile):
    params = get_params('eliminate_image_complexity')
    act_on_image(infile, outfile, params)

def alpha_batch(infile, name, action):
    params = get_params(action)
    for alpha in [a/10.0 for a in range(10)]:
        params.custom['alpha'] = alpha
        outfile = infile.replace('.', '_{2}_{1}_p{0}.'.format(int(alpha*10), 'cgc' if params.gray else 'pbc', name))
        log.critical('---------------------\n' + outfile + '\n---------------------')
        act_on_image(infile, outfile, params)

def batch(infile):
    actions = ['eliminate_image_simplicity', 'eliminate_image_complexity']
    for action in actions:
        name = 'complexified' if 'simpl' in action else 'simplified'
        alpha_batch(infile, name, action)

def bpcs_steg(infile, messagefile, outfile):
    params = get_params('bpcs')
    message_grids = read_message_grids(messagefile, params)
    params.custom['message_grids'] = message_grids
    act_on_image(infile, outfile, params)

if __name__ == '__main__':
    infile = 'docs/vessel_small.png'
    batch(infile)
    # remove_complexity(infile, infile.replace('.', '_simplified_cgc_p7.'))
    # remove_simplicity(infile, infile.replace('.', '_complexified.'))
