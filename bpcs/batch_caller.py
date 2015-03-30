from logger import log
from bpcs_steg_capacity import complexify, simplify

GRAYED = True

def alpha_batch(infile, name, action, alphas, grayed):
    nflippeds = {}
    for alpha in alphas:
        outfile = infile.replace('.', '_{2}_{1}_p{0}.'.format(int(alpha*10), 'cgc' if grayed else 'pbc', name))
        # print alpha
        log.critical('---------------------\n' + outfile + '\n---------------------')
        nflipped = action(infile, outfile, alpha)
        nflippeds[(name, alpha)] = nflipped
    return nflippeds

def write_stats(outfile, stats):
    out = ''
    for (name, alpha), n in stats.iteritems():
        out += '{0},{1},{2}\n'.format(name, alpha, n)
    with open(outfile, 'w') as f:
        f.write(out)

def batch(infile):
    actions = {'rand_complex_size': complexify, 'rand_simp_side': simplify}
    alphas = [a/10.0 for a in range(10)]
    stats = {}
    for gray in [True, False]:
        for name, fcn in actions.iteritems():
            cur_stats = alpha_batch(infile, name, fcn, alphas, gray)
            stats.update(cur_stats)
    write_stats(infile.replace('.png', '_stats_pbc.txt'), stats)

if __name__ == '__main__':
    infile = '/Users/mobeets/bpcs-steg/docs/vessel_small.png'
    batch(infile)
