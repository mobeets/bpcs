import numpy as np
import Image # source: http://www.pythonware.com/library/pil/handbook/image.htm

from array_bit_plane import BitPlane

from collections import namedtuple
Params = namedtuple('ImageParams', ['nbits_per_layer', 'grid_size', 'as_rgb', 'gray', 'modifier', 'custom'])
get_im_mode = lambda is_rgb: 'RGB' if is_rgb else 'L'

DEFAULT_PARAMS = Params(8, (8,8), True, True, lambda x: x, {})

def load_image(infile, as_rgb):
    return Image.open(infile).convert(get_im_mode(as_rgb))

def write_image(outfile, im):
    im.save(outfile, outfile.split('.')[-1])

def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

def bitplane_then_act(im, params):
    """
    im is an image
    converts im to a bit-planed numpy array
    then applies params.modifier to that array
        and returns the resulting new image
    """
    cur = image_to_array(im)
    cur = BitPlane(cur, params.gray).slice(params.nbits_per_layer)
    cur = params.modifier(cur, params)
    cur = BitPlane(cur, params.gray).stack()
    new_im = array_to_image(cur)
    return new_im

def act_on_image(infile, outfile, params=DEFAULT_PARAMS):
    im = load_image(infile, params.as_rgb)
    new_im = bitplane_then_act(im, params)
    write_image(outfile, new_im)

if __name__ == '__main__':
    infile = 'docs/vessel.png'
    act_on_image(infile, infile.replace('.', '_old.'))
