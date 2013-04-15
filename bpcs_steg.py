import numpy as np
import Image # source: http://www.pythonware.com/library/pil/handbook/image.htm

from array_grid import Grid
from array_bit_plane import BitPlane

from collections import namedtuple
Params = namedtuple('ImageParams', ['nbits_per_layer', 'grid_size', 'as_rgb'])
ActionParams = namedtuple('ActionParams', ['bitplane', 'grid', 'modifier'])
DEFAULT_PARAMS = Params(8, 8, True)
DEFAULT_ACTION = 'dummy'
get_im_mode = lambda is_rgb: 'RGB' if is_rgb else 'L'

def load_image(infile, as_rgb):
    return Image.open(infile).convert(get_im_mode(as_rgb))

def write_image(outfile, im, as_rgb):
    im.save(outfile, get_im_mode(as_rgb))

def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

def eliminate_image_complexity(grid, params):
    pass

def dummy_action_fcn(grid, params):
    # iterate through grids, do whatever...
    # print grid.block_view((0,0,0))
    # print grid.block_view((61,0,0))
    #

def act_on_gridded_bitplane(im, action_params, params):
    """
    im is an image
    converts im to a gridded, bit-planed numpy array
        (gridded and bit-planed only if specified in action_params)
    then applies action_params.modifier to that array
        and returns the resulting new image
    """
    cur = image_to_array(im)
    if action_params.bitplane:
        cur = BitPlane(cur).slice(params.nbits_per_layer)
    if action_params.grid:
        cur = Grid(cur, params.grid_size)

    action_fcn(cur, params)

    if action_params.bitplane:
        if action_params.grid:
            cur = cur.arr
        cur = BitPlane(cur).stack()
    new_im = array_to_image(cur)
    return new_im

def get_action_params(action):
    if action == 'dummy_all':
        action_params = ActionParams(True, True, dummy_action_fcn)
    elif action == 'dummy_none':
        action_params = ActionParams(False, False, dummy_action_fcn)
    elif action == 'dummy_grid':
        action_params = ActionParams(False, True, dummy_action_fcn)
    elif action == 'dummy_plane':
        action_params = ActionParams(True, False, dummy_action_fcn)
    elif action == 'eliminate_image_complexity':
        action_params = ActionParams(True, True, eliminate_image_complexity)
    return action_params

def test(infile):
    for action in ['dummy_none', 'dummy_plane', 'dummy_grid', 'dummy_all']:
        outfile = infile.replace('.', action + '.')
        main(infile, outfile, action)

def main(infile, outfile, action=DEFAULT_ACTION, params=DEFAULT_PARAMS):
    im = load_image(infile, params.as_rgb)
    action_params = get_action_params(action)
    new_im = act_on_gridded_bitplane(im, action_params, params)
    write_image(outfile, new_im, params.as_rgb)

if __name__ == '__main__':
    infile = 'vessel.png'
    test(infile)
