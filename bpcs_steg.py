import numpy as np
import Image # source: http://www.pythonware.com/library/pil/handbook/image.htm

from array_grid import Grid

from collections import namedtuple
params = namedtuple('ImageParams', ['nbits_per_layer', 'grid_size', 'as_rgb'])
DEFAULT_PARAMS = params(8, 8, True)
get_im_mode = lambda is_rgb: 'RGB' if is_rgb else 'L'

def load_image(infile, as_rgb):
    return Image.open(infile).convert(get_im_mode(as_rgb))

def write_image(outfile, im, as_rgb):
    im.save(outfile, get_im_mode(as_rgb))

def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

def main(infile, outfile, params=DEFAULT_PARAMS):
    im = load_image(infile, params.as_rgb)
    arr = image_to_array(im)
    x = Grid(arr, True)
    print x.block_view((0,0,0))
    print x.block_view((61,0,0))

if __name__ == '__main__':
    infile = 'vessel.png'
    outfile = 'vessel_out.png'
    main(infile, outfile)
