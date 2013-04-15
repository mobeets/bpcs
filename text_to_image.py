from PIL import Image
import numpy as np
from math import sqrt

def text_to_uint8_array(text, dims):
    colors = [ord(x) for x in text]
    arr = np.array(colors)
    arr = np.resize(arr, dims)
    arr = np.uint8(arr)
    return arr

def image_to_text(infile, outfile):
    pass

def text_to_image(infile, outfile):
    text = open(infile).read()
    dims = [int(sqrt(len(text))), int(sqrt(len(text))), 3]
    arr = text_to_uint8_array(text, dims)
    im = Image.fromarray(arr)
    im.save(outfile)

if __name__ == '__main__':
    infile = '/Users/mobeets/Desktop/tmp.txt'
    outfile = '/Users/mobeets/Desktop/tmp.png'
    text_to_image(infile, outfile)

    infile = '/Users/mobeets/Desktop/tmp2.png'
    outfile = '/Users/mobeets/Desktop/tmp2.txt'
    image_to_text(infile, outfile)
