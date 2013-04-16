from PIL import Image
import numpy as np
from math import sqrt
from test_utils import show_html_diff

def get_prod_of_shape(arr):
    return arr.shape[0] * arr.shape[1] * arr.shape[2]

def txt_to_uint8_array(txt, dims):
    colors = [ord(x) for x in txt]
    arr = np.array(colors)
    arr_shaped = np.resize(arr, dims)
    if arr.shape[0] != get_prod_of_shape(arr_shaped):
        diff = get_prod_of_shape(arr_shaped) - arr.shape[0]
        print "WARNING: txt will be replicated by {0} chars when printed to image".format(diff)
    arr_shaped = np.uint8(arr_shaped)
    return arr_shaped

def adjust_txt_and_get_dims(txt, verbose=False):
    added = 0
    # pad with 0s to make divisible by 3
    rem = 3-(len(txt)%3)
    txt += ' '*rem
    added += rem

    # pad with 0s to make square
    area = len(txt)/3
    one_side = sqrt(area)
    desired_side = (int(one_side)+1) if one_side > int(one_side) else int(one_side)

    diff = 3*(desired_side**2 - area)
    txt += ' '*diff
    added += diff
    assert len(txt) == 3*(desired_side**2), 3*(desired_side**2) - len(txt)
    if verbose:
        print 'Adding %s spaces to end of txt' % (added,)
    return txt, [desired_side, desired_side, 3]

def image_to_txt(imfile, txtfile):
    """
    converts each character to a number
        assuming the character is ascii
        and arranges all resulting colors into an array => image
    note: colors are inserted depth first, meaning
        e.g. if the first word is 'the'
            then the first pixel will be (ord('t'), ord('h'), ord('e'))
                'the' => (116, 104, 101) == #6A6865
    """
    png = Image.open(imfile).convert('RGB')
    arr = np.array(png)
    dims = get_prod_of_shape(arr)
    arr_flat = np.resize(arr, dims)
    chars = [chr(x) for x in arr_flat]
    with open(txtfile, 'w') as f:
        f.write(''.join(chars))

def txt_to_image(txtfile, imfile):
    txt = open(txtfile).read()
    txt, dims = adjust_txt_and_get_dims(txt, True)
    arr = txt_to_uint8_array(txt, dims)
    im = Image.fromarray(arr)
    im.save(imfile)

def test_adjust_txt_and_get_dims():
    vals = [5, 10, 11, 19, 24, 25, 31, 32, 269393]
    sides = [2, 2, 2, 3, 3, 3, 4, 4, 300]
    for val, side in zip(vals, sides):
        assert adjust_txt_and_get_dims(' '*val)[1] == [side, side, 3], val

def test_invertibility(txtfile):
    """
    roughly, assert txtfile == image_to_txt(txt_to_image(txtfile))
        ignoring whitespace before and after txt
    """
    pngfile = txtfile.replace('.txt', '.png')
    txt_to_image(txtfile, pngfile)
    new_txtfile = txtfile.replace('.', '_new.')
    image_to_txt(pngfile, new_txtfile)
    txt1 = open(txtfile).read().strip()
    txt2 = open(new_txtfile).read().strip()
    assert txt1 == txt2, show_html_diff((txt1, 'OG'), (txt2, 'NEW'))

if __name__ == '__main__':
    txtfile = 'tmp.txt'
    test_adjust_txt_and_get_dims()
    test_invertibility(txtfile)

    # infile = '/Users/mobeets/Desktop/tmp.txt'
    # outfile = '/Users/mobeets/Desktop/tmp.png'
    # txt_to_image(infile, outfile)

    # infile = '/Users/mobeets/Desktop/tmp2.png'
    # outfile = '/Users/mobeets/Desktop/tmp2.txt'
    # image_to_txt(infile, outfile)
