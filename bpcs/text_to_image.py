import re
import string
from math import sqrt

import numpy as np
from PIL import Image

from test_utils import show_html_diff

def digits_in_base_as_tuple(x, base):
    """
    x is int
    base is int

    gets the digits of x in the new base
    e.g. digits_in_base_as_tuple(20, 2) == (1,0,1,0,0)
    """
    cur = x
    digs = []
    while cur:
        digs.append(cur % base)
        cur /= base
    return tuple(reversed(digs))

def get_word_color_map_fcn(all_words):
    """
    given a set of words, returns a fcn
        returning an RGB color
        where each word is maximally spaced out from other word colors
    """
    words = set(all_words)
    words.add(' ') # add space for padding
    ncolors = 256**3
    ncolors_per_word = ncolors/len(words)
    word_order = sorted(words)
    def get_word_color(word):
        ind = word_order.index(word)
        assert ind >= 0
        colors = digits_in_base_as_tuple(ind*ncolors_per_word, 256)
        while len(colors) < 3:
            colors = (0,) + colors
        assert len(colors) == 3
        return colors
    return get_word_color

def list_to_uint8_array(colors, dims):
    arr = np.array(colors)
    arr_shaped = np.resize(arr, dims)
    if arr.size != arr_shaped.size:
        diff = arr_shaped.size - arr.size
        print "WARNING: txt will be replicated by {0} chars when printed to image".format(diff)
    arr_shaped = np.uint8(arr_shaped)
    return arr_shaped

def adjust_words_and_get_dims(words, verbose=False):
    area = len(words)
    one_side = sqrt(area)
    desired_side = (int(one_side)+1) if one_side > int(one_side) else int(one_side)
    diff = desired_side**2 - area
    words += [' ']*diff
    assert len(words) == desired_side**2, desired_side**2 - len(words)
    if verbose:
        print 'Adding %s words to end of txt' % (diff,)
    return words, [desired_side, desired_side, 3]
    
def str_to_words(txt, keep_spaces=False):
    # if keep_spaces:
    #     # want each space to be its own word
    #     space_first = txt[0] == ' '
    #     words = str_to_words(txt)
    #     space_chunks = [x for x in re.split('[^ ]', txt) if x] + [' ']
    #     final = []
    #     for word, space in zip(words, space_chunks):
    #         if space_first:
    #             for i in range(len(space)):
    #                 final.append(' ')
    #             final.append(word)
    #         else:
    #             final.append(word)
    #             for i in range(len(space)):
    #                 final.append(' ')
    #     return final
    if keep_spaces:
        words = str_to_words(txt)
        spaces = [x for x in re.split('[^ ]', txt) if x] + [' ']
        return [x for pair in zip(words, spaces) for x in pair]
    else:
        return txt.split()
        # return re.sub('['+string.punctuation+']', '', txt).split()

def txt_to_uint8_array_by_word(txt):
    words = str_to_words(txt, True)
    words, dims = adjust_words_and_get_dims(words)
    get_color = get_word_color_map_fcn(words)
    colors = [get_color(word) for word in words]
    return list_to_uint8_array(colors, dims)

def adjust_txt_and_get_dims(txt, verbose=False):
    added = 0
    # pad with 0s to make divisible by 3
    rem = len(txt) % 3
    add = 3-rem if rem else 0
    txt += ' '*add
    added += add

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

def txt_to_uint8_array_by_char(txt):
    txt, dims = adjust_txt_and_get_dims(txt, True)
    colors = [ord(x) for x in txt]
    return list_to_uint8_array(colors, dims)

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
    dims = arr.size
    arr_flat = np.resize(arr, dims)
    chars = [chr(x) for x in arr_flat]
    with open(txtfile, 'w') as f:
        f.write(''.join(chars))

def txt_to_image(txtfile, imfile, by_char=True):
    txt = open(txtfile).read()
    if by_char:
        arr = txt_to_uint8_array_by_char(txt)
    else:
        arr = txt_to_uint8_array_by_word(txt)
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

def test_all():
    txtfile = 'docs/tmp.txt'
    test_adjust_txt_and_get_dims()
    test_invertibility(txtfile)

if __name__ == '__main__':
    test_all()

    by_char = False

    base_dir = '/Users/mobeets/bpcs-steg/docs/'
    infiles = ['karenina', 'warandpeace']
    infiles = ['tmp', 'tmp1', 'tmp2']

    infiles = [base_dir + infile + '.txt' for infile in infiles]
    outfiles = [base_dir + outfile + '.txt' for outfile in outfiles]
    for infile,outfile in zip(infiles, outfiles):
        txt_to_image(infile, outfile, by_char)
    
    # infile = '/Users/mobeets/Desktop/tmp2.png'
    # outfile = '/Users/mobeets/Desktop/tmp2.txt'
    # image_to_txt(infile, outfile, by_char)
