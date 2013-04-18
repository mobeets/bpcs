from act_on_image import ActionParams, act_on_image
from test_utils import show_html_diff

def dummy_action_fcn(grid, params):
    # iterate through grids, do whatever...
    # print grid.block_view((0,0,0))
    # print grid.block_view((61,0,0))
    #
    pass

def get_dummy_action_params(action):
    if action == 'dummy_all':
        action_params = ActionParams(True, True, True, dummy_action_fcn, {})
    elif action == 'dummy_none':
        action_params = ActionParams(False, False, None, dummy_action_fcn, {})
    elif action == 'dummy_grid':
        action_params = ActionParams(False, True, True, dummy_action_fcn, {})
    elif action == 'dummy_no_cgc':
        action_params = ActionParams(False, True, False, dummy_action_fcn, {})
    elif action == 'dummy_plane':
        action_params = ActionParams(True, False, None, dummy_action_fcn, {})

def test_null_action(infile):
    """ makes sure that dummy_fcns won't change image by gridding and/or bitplaning """
    for action in ['dummy_none', 'dummy_plane', 'dummy_grid', 'dummy_all']:
        outfile = infile.replace('.', action + '.')
        act_on_image(infile, outfile, action)
        f1 = open(infile).read()
        f2 = open(outfile).read()
        assert f1 == f2, show_html_diff((f1, 'OG'), (f2, 'NEW'))

if __name__ == '__main__':
    infile = 'docs/vessel.png'
    test_null_action(infile)
