import numpy as np
import Image # source: http://www.pythonware.com/library/pil/handbook/image.htm

from array_grid import Grid
from array_bit_plane import BitPlane

from collections import namedtuple
Params = namedtuple('ImageParams', ['nbits_per_layer', 'grid_size', 'as_rgb'])
ActionParams = namedtuple('ActionParams', ['bitplane', 'grid', 'gray', 'modifier', 'custom'])
get_im_mode = lambda is_rgb: 'RGB' if is_rgb else 'L'

DEFAULT_PARAMS = Params(8, (8,8), True)

def load_image(infile, as_rgb):
    return Image.open(infile).convert(get_im_mode(as_rgb))

def write_image(outfile, im):
    im.save(outfile, outfile.split('.')[-1])

def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

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
        cur = BitPlane(cur, action_params.gray).slice(params.nbits_per_layer)
    if action_params.grid:
        cur = Grid(cur, params.grid_size)

    action_params.modifier(cur, params)

    if action_params.bitplane:
        if action_params.grid:
            cur = cur.arr
        cur = BitPlane(cur, action_params.gray).stack()
    elif action_params.grid:
        cur = cur.arr
    new_im = array_to_image(cur)
    return new_im

def act_on_image(infile, outfile, action_params, params=DEFAULT_PARAMS):
    im = load_image(infile, params.as_rgb)
    new_im = act_on_gridded_bitplane(im, action_params, params)
    write_image(outfile, new_im)

if __name__ == '__main__':
    infile = 'docs/vessel.png'
    act_on_image(infile, infile.replace('.', '_old.'))
