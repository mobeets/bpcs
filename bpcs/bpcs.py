#!/usr/bin/env python
"""
BPCS Steganography: encoding/decoding messages hidden in a vessel image

Source: http://web.eece.maine.edu/~eason/steg/SPIE98.pdf

BEHAVIORS:
    encoding
        * expects a vessel image file, message file, and alpha value
        * hides the contents of a file inside a vessel image
    decoding
        * expects a vessel image file, and alpha value
        * recovers the message stored inside a vessel image
    capacity
        * expects a vessel image file and alpha value
        * assesses the maximum size of a message that could be encoded within the vessel image
    test
        * runs the unit tests

"""
from bpcs_steg_decode import decode
from bpcs_steg_encode import encode
from bpcs_steg_capacity import capacity
from bpcs_steg_test import test_all

import os.path
import optparse

__author__ = "Jay Hennig"
__license__ = "BSD"
__email__ = "mobeets@gmail.com"

parser = optparse.OptionParser()

valid_opt_behaviors = {
    'encode': ['infile', 'messagefile', 'alpha'],
    'decode': ['infile', 'outfile', 'alpha'],
    'capacity': ['infile', 'outfile', 'alpha'],
    'test': []
    }

parser.add_option('-i', '--infile', dest='infile', action='store', type='string', help='path to vessel image (.png)')
parser.add_option('-o', '--outfile', dest='outfile', action='store', type='string', help='path to write output file')
parser.add_option('-m', '--messagefile', dest='messagefile', action='store', type='string', help='path to message file')
parser.add_option('-a', '--alpha', dest='alpha', action='store', type='float', help='complexity threshold', default=0.45)
parser.add_option('-b', '--behavior', dest='behavior', action='store', type='string', help='interaction modes: {0}'.format(valid_opt_behaviors.keys()))

(opts, args) = parser.parse_args()

def check_file_exists(filename):
    if not os.path.exists(filename):
        parser.error('The file "{0}" could not be found.'.format(filename))

if not opts.behavior:
    parser.error('-h for help.')
if opts.behavior not in valid_opt_behaviors:
    parser.error('Illegal behavior: {0}. Valid behaviors are {1}'.format(opts.behavior, valid_opt_behaviors.keys()))
mandatory_opts = valid_opt_behaviors[opts.behavior]
if any([m for m in mandatory_opts if not opts.__dict__[m]]):
    parser.error('To {0}, you must specify the following: {1}'.format(opts.behavior, mandatory_opts))

if opts.behavior == 'decode':
    check_file_exists(opts.infile)
    decode(opts.infile, opts.outfile, opts.alpha)
elif opts.behavior == 'encode':
    check_file_exists(opts.infile)
    check_file_exists(opts.messagefile)
    encode(opts.infile, opts.messagefile, opts.outfile, opts.alpha)
elif opts.behavior == 'capacity':
    check_file_exists(opts.infile)
    capacity(opts.infile, opts.outfile, opts.alpha)
elif opts.behavior == 'test':
    test_all()
