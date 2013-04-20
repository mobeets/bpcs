from act_on_image import Params, act_on_image
from array_bit_plane import pbc_to_cgc, cgc_to_pbc, conjugate, BitPlane
from bpcs_steg import arr_bpcs_complexity
from array_message import list_to_grids, grids_to_list

from test_utils import show_html_diff
import numpy as np

def test_bin_arr_to_grids_invertibility():
    # note: only true when they perfectly divide into grids of dim
    arr = [0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,0]
    assert grids_to_list(list_to_grids(arr, [2,3])) == arr
    assert grids_to_list(list_to_grids(arr, [6,1])) == arr
    assert grids_to_list(list_to_grids(arr, [3,4])) == arr

def test_bpcs_complexity():
    arr = np.array([[1,0,0,1], [0,1,1,0], [1,1,1,1]])
    ans = 10/17.0
    assert arr_bpcs_complexity(arr) == ans

def test_pbc_to_cgc_invertibility(arr):
    f = pbc_to_cgc
    finv = cgc_to_pbc
    assert f(finv(arr)) == arr
    assert finv(f(arr)) == arr

def test_bitplane_invertibility(arr):
    b1 = BitPlane(arr, True)
    assert b1.stack(b1.slice(8)) == arr
    b1 = BitPlane(arr, True)
    assert b1.stack(b1.slice(5)) == arr
    b3 = BitPlane(arr, False)
    assert b3.stack(b3.slice(8)) == arr

def test_conjugate_invertibility(arr):
    assert conjugate(conjugate(arr)) == arr

def dummy_action_fcn(grid, params):
    # iterate through grids, do whatever...
    # print grid.block_view((0,0,0))
    # print grid.block_view((61,0,0))
    #
    pass

def get_dummy_params():
    # ['nbits_per_layer', 'grid_size', 'as_rgb', 'gray', 'modifier', 'custom']
    return Params(8, (8,8), True, True, dummy_action_fcn, {})

def test_null_action(infile):
    """ makes sure that dummy_fcns won't change image by gridding and/or bitplaning """
    action = 'dummy'
    outfile = infile.replace('.', '_' + action + '.')
    act_on_image(infile, outfile, get_dummy_params())
    f1 = open(infile).read()
    f2 = open(outfile).read()
    assert f1 == f2, show_html_diff((f1, 'OG'), (f2, 'NEW'))

def test_all():
    test_bpcs_complexity()
    test_bin_arr_to_grids_invertibility()
    infile = 'docs/vessel.png'
    # test_null_action(infile)

if __name__ == '__main__':
    test_all()

