from act_on_image import Params, act_on_image
from array_bit_plane import pbc_to_cgc, cgc_to_pbc, conjugate, BitPlane
from bpcs_steg import arr_bpcs_complexity
from array_message import list_to_grids, grids_to_list, str_to_grids, grids_to_str

from test_utils import show_html_diff
import numpy as np

def test_grids_to_str_invertibility():
    message = 'hello there asfasdf asdfasdf asdfasdf asd,f asd; asdf !fdf'
    grids = str_to_grids(message, get_dummy_params())
    message_out = grids_to_str(grids)
    assert message_out[:len(message)] == message

def test_list_to_grids():
    arr = [0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,0]
    grids_out = list_to_grids(arr, [2,3]).tolist()
    grids = [[[0,1,1],[1,1,0]], [[0,0,1],[0,1,0]], [[0,0,0],[0,1,1]], [[1,0,0],[1,1,0]]]
    assert grids_out == grids

def test_list_to_grids_1():
    arr = [0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,0,1]
    grids_out = list_to_grids(arr, [2,3]).tolist()
    grids = [[[0,1,1],[1,1,0]], [[0,0,1],[0,1,0]], [[0,0,0],[0,1,1]], [[1,0,0],[1,1,0]], [[1,0,0],[0,0,0]]]
    assert grids_out == grids

def test_grids_to_list():
    grids = [[[0,1,1],[1,1,0]], [[0,0,1],[0,1,0]], [[0,0,0],[0,1,1]], [[1,0,0],[1,1,0]]]
    arr_out = grids_to_list(grids)
    arr = [0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,0]
    assert arr_out == arr

def test_list_to_grids_invertibility():
    # note: only true when they perfectly divide into grids of dim
    arr = [0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,0]
    assert grids_to_list(list_to_grids(arr, [2,3])) == arr
    assert grids_to_list(list_to_grids(arr, [6,1])) == arr
    assert grids_to_list(list_to_grids(arr, [3,4])) == arr

def test_bpcs_complexity():
    arr = np.array([[1,0,0,1], [0,1,1,0], [1,1,1,1]])
    ans = 10/17.0
    assert arr_bpcs_complexity(arr) == ans

def test_pbc_to_cgc():
    arr = np.array([[0,1,1,0],[0,1,1,1],[1,0,1,0]])
    arr.resize([1,1,3,4])
    cgc = [[[[0,1,0,1],[0,1,0,0],[1,1,1,1]]]]
    cgc_out = pbc_to_cgc(arr).tolist()
    assert cgc == cgc_out

def test_cgc_to_pbc():
    arr = np.array([[0,1,0,1],[0,1,0,0],[1,1,1,1]])
    arr.resize([1,1,3,4])
    pbc = [[[[0,1,1,0],[0,1,1,1],[1,0,1,0]]]]
    pbc_out = cgc_to_pbc(arr).tolist()
    assert pbc == pbc_out

def test_pbc_to_cgc_invertibility():
    arr = np.array([[0,1,1,0],[0,1,1,1],[1,0,1,0]])
    arr.resize([1,1,3,4])
    f = pbc_to_cgc
    finv = cgc_to_pbc

    f_arr = f(arr)
    finv_f_arr = finv(f_arr)
    assert finv_f_arr.tolist() == arr.tolist()

    finv_arr = finv(arr)
    f_finv_arr = f(finv_arr)
    assert f_finv_arr.tolist() == arr.tolist()

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
    test_list_to_grids()
    test_list_to_grids_1()
    test_grids_to_list()
    test_list_to_grids_invertibility()
    test_grids_to_str_invertibility()
    test_pbc_to_cgc()
    test_cgc_to_pbc()
    test_pbc_to_cgc_invertibility()
    test_bpcs_complexity()
    infile = 'docs/vessel.png'
    # test_null_action(infile)

if __name__ == '__main__':
    test_all()

