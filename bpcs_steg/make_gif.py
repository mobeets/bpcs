import os
from PIL import Image
from images2gif import writeGif

basedir = '/Users/mobeets/bpcs-steg/examples/cgc_v_pbc'
inf = 'vessel_small_{2}_{0}_p{1}.png'
outf = 'vessel_small_{1}_{0}.gif'

whats = ['simplified', 'complexified']
kinds = ['cgc', 'pbc']
ps = range(1,10)
# ps = range(30, 33) + range(35, 45) + range(46, 50)


for what in whats:
    for kind in kinds:
        outfile = os.path.join(basedir, outf.format(what, kind))
        images = [Image.open(os.path.join(basedir, inf.format(kind, p, what))) for p in ps]
        writeGif(outfile, images, duration=0.4, loops=1, dither=1)
