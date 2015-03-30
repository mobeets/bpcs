import numpy as np

from act_on_image import ActOnImage
from array_bit_plane import pbc_to_cgc, cgc_to_pbc, BitPlane
from bpcs_steg import arr_bpcs_complexity, conjugate

from array_message import list_to_grids, grids_to_list, str_to_grids, grids_to_str, get_next_message_grid_sized
from array_grid import get_next_grid_dims

def test_get_next_message_grid_sized_1():
    arr = np.array([[1,0,0,1], [0,1,1,0], [1,1,1,1]])
    dims = [2,2]
    grids = []
    cur_grid = True
    while arr.size > 0:
        cur_grid, arr = get_next_message_grid_sized(arr, dims)
        if cur_grid.size > 0:
            grids.append(cur_grid.tolist())
    assert grids == [[[1,0], [0,1]], [[0,1], [1,0]], [[1,1], [1,1]]], grids

def test_get_next_message_grid_sized_2():
    arr = np.array([[1,0,0,1], [0,1,1,0], [1,1,1,1], [0,1,0,0]])
    dims = [3,2]
    grids = []
    cur_grid = True
    while arr.size > 0:
        cur_grid, arr = get_next_message_grid_sized(arr, dims)
        if cur_grid.size > 0:
            grids.append(cur_grid.tolist())
    assert grids == [[[1,0], [0,1], [0,1]], [[1,0], [1,1],[1,1]], [[0,1],[0,0],[0,0]]], grids

def test_get_next_grid_dims():
    arr = np.arange(96)
    arr = np.resize(arr, [4,4,3,2])
    ans = [
            [slice(0,3), slice(0,2), 0, 0],
            [slice(0,3), slice(2,4), 0, 0],
            [slice(3,4), slice(0,2), 0, 0],
            [slice(3,4), slice(2,4), 0, 0],
            [slice(0,3), slice(0,2), 0, 1],
            [slice(0,3), slice(2,4), 0, 1],
            [slice(3,4), slice(0,2), 0, 1],
            [slice(3,4), slice(2,4), 0, 1],
            [slice(0,3), slice(0,2), 1, 0],
            [slice(0,3), slice(2,4), 1, 0],
            [slice(3,4), slice(0,2), 1, 0],
            [slice(3,4), slice(2,4), 1, 0],
            [slice(0,3), slice(0,2), 1, 1],
            [slice(0,3), slice(2,4), 1, 1],
            [slice(3,4), slice(0,2), 1, 1],
            [slice(3,4), slice(2,4), 1, 1],
            [slice(0,3), slice(0,2), 2, 0],
            [slice(0,3), slice(2,4), 2, 0],
            [slice(3,4), slice(0,2), 2, 0],
            [slice(3,4), slice(2,4), 2, 0],
            [slice(0,3), slice(0,2), 2, 1],
            [slice(0,3), slice(2,4), 2, 1],
            [slice(3,4), slice(0,2), 2, 1],
            [slice(3,4), slice(2,4), 2, 1],
        ]
    for i, dims in enumerate(get_next_grid_dims(arr, [3,2])):
        assert dims == ans[i]

def test_grids_to_str_invertibility():
    message = 'hello there asfasdf asdfasdf asdfasdf asd,f asd; asdf !fdf'
    grids = str_to_grids(message, (8,8))
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

def test_bitplane_invertibility():
    arr = np.array([[14,24,9,0],[1,32,3,5],[14,5,3,2],[16,22,1,1],[1,200,180,53],[9,23,111,20]])
    arr.resize([4,3,2])

    grayed = False
    b1 = BitPlane(arr, grayed)
    b2 = b1.slice(8)
    assert BitPlane(b2, grayed).stack().tolist() == arr.tolist()

    grayed = False
    b1 = BitPlane(arr, grayed)
    b2 = b1.slice(15)
    assert BitPlane(b2, grayed).stack().tolist() == arr.tolist()

    grayed = True
    b1 = BitPlane(arr, grayed)
    b2 = b1.slice(8)
    assert BitPlane(b2, grayed).stack().tolist() == arr.tolist()

def test_conjugate_invertibility():
    arr = np.array([[0,1,0,1,1,1,0,1,0], [1,1,1,1,0,0,1,1,0], [0,0,1,1,1,0,0,1,0]])
    assert conjugate(conjugate(arr)).tolist() == arr.tolist()

def test_conjugate():
    arr = np.array([[0,1,0,1,1,1,0,1,0], [1,1,1,1,0,0,1,1,0], [0,0,1,1,1,0,0,1,0]])
    alpha = arr_bpcs_complexity(arr)
    arr_conj = conjugate(arr)
    alpha_conj = arr_bpcs_complexity(arr_conj)
    assert alpha == 1 - alpha_conj

def test_all():
    test_get_next_message_grid_sized_1()
    test_get_next_message_grid_sized_2()
    test_bitplane_invertibility()
    test_conjugate_invertibility()
    test_conjugate()
    test_list_to_grids()
    test_list_to_grids_1()
    test_grids_to_list()
    test_list_to_grids_invertibility()
    test_grids_to_str_invertibility()
    test_pbc_to_cgc()
    test_cgc_to_pbc()
    test_pbc_to_cgc_invertibility()
    test_bpcs_complexity()
    test_get_next_grid_dims()
    # test_null_action()

if __name__ == '__main__':
    test_all()

