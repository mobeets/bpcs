import numpy as np
from PIL import Image # source: http://www.pythonware.com/library/pil/handbook/image.htm

from .logger import log
from .array_bit_plane import BitPlane

def load_image(infile, as_rgb):
    get_im_mode = lambda is_rgb: 'RGB' if is_rgb else 'L'
    return Image.open(infile).convert(get_im_mode(as_rgb))

def write_image(outfile, im):
    im.save(outfile, outfile.split('.')[-1])

def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

class ActOnImage(object):
    def __init__(self, infile, as_rgb, bitplane, gray, nbits_per_layer):
        self.infile = infile
        self.as_rgb = as_rgb
        self.bitplane  = bitplane
        self.gray = gray
        self.nbits_per_layer = nbits_per_layer
        self.arr = self.read(infile)
        log.critical('Loaded image as array with shape {0}'.format(self.arr.shape))

    def read(self, infile):
        im = load_image(infile, self.as_rgb)
        arr = image_to_array(im)
        if self.bitplane:
            arr = BitPlane(arr, self.gray).slice(self.nbits_per_layer)
        return arr

    def modify(self):
        raise NotImplementedError()

    def write(self, outfile, arr):
        if self.bitplane:
            arr = BitPlane(arr, self.gray).stack()
        im = array_to_image(arr)
        log.critical('Loaded new array as image')
        write_image(outfile, im)
