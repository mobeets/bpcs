from act_on_image import act_on_image, DEFAULT_PARAMS
from text_to_image import txt_to_uint8_array

def arr_bpcs_complexity(arr):
    """
    arr is a 2-d numpy array
    returns the fraction of maximum bpcs_complexity in arr
        where bpcs_complexity is total sum of bit changes
        moving along each row and each column
    """
    nrows, ncols = arr.shape
    max_complexity = ((nrows-1)*ncols) + ((ncols-1)*nrows)
    nbit_changes = lambda items, length: [items[i] ^ items[i-1] for i in range(1, length)]
    k = 0
    for row in arr:
        k += nbit_changes(row, ncols)
    for col in arr.transpose():
        k += nbit_changes(col, nrows)
    return (k*1.0)/max_complexity

def eliminate_image_complexity(grids, params):
    alpha = params.custom['alpha']
    for grid in grids:
        if arr_bpcs_complexity(grid) < alpha:
            grid = conjugate(grid)

def next_grid_to_replace(grids):
    for grid in grids:
        if arr_bpcs_complexity(grid) < alpha:
            yield grid

def embed_message_in_vessel(grids, params):
    alpha = params.custom['alpha']
    message_grids = list(params.custom['message_grids'])
    conjugated = []
    i = 0
    for grid in next_grid_to_replace(grids):
        if not message_grids:
            # not sure if we're supposed to remove all complexities in o.g. image
            # i.e. stop placing messages and just conjugate grids under alpha...
            pass
        # get next message_grid
        cur_message = message_grids.pop()
        # conjugate if necessary, keep track of message_grids conjugated
        if arr_bpcs_complexity(cur_message) < alpha:
            cur_message = conjugate(cur_message)
            conjugated.append(i)
        i += 1
        # replace grid with message_grid
        grid = cur_message

def get_action_params(action):
    if action == 'eliminate_image_complexity':
        action_params = ActionParams(True, True, True, eliminate_image_complexity, {'alpha': 0.3})
    elif action == 'bpcs':
        action_params = ActionParams(True, True, True, embed_message_in_vessel, {'alpha': 0.3, 'message_grids': ''})
    return action_params

def remove_complexity(infile, outfile):
    action_params = get_action_params('eliminate_image_complexity')
    act_on_image(infile, outfile, action_params)

def set_message_grids(messagefile, action_params, params=DEFAULT_PARAMS):
    content = open(messagefile).read()
    n, m = params.grid_size
    n_grids = len(content)/(n*m)
    arr = txt_to_uint8_array(content, [n,m*n_grids])
    arr = BitPlane(arr, action_params.gray).slice(params.nbits_per_layer)
    arr = Grid(arr, params.grid_size)
    action_params.custom['message_grids'] = arr

def bpcs_steg(infile, messagefile, outfile):
    action_params = get_action_params('bpcs')
    set_message_grids(messagefile, action_params)
    act_on_image(infile, outfile, action_params)

if __name__ == '__main__':
    infile = 'docs/vessel.png'
    remove_complexity(infile, infile.replace('.', '_old.'))
