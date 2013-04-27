from complexity_flippers import complexify, simplify
from logger import log

GRAYED = True

def alpha_batch(infile, name, action, alphas):
    nflippeds = {}
    for alpha in alphas:
        outfile = infile.replace('.', '_{2}_{1}_p{0}.'.format(int(alpha*100), 'cgc' if GRAYED else 'pbc', name))
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
    actions = {'complexified': complexify, 'simplified': simplify}
    alphas = [0.3 + (a/100.0) for a in range(2)]
    stats = {}
    for name, fcn in actions.iteritems():
        cur_stats = alpha_batch(infile, name, fcn, alphas)
        stats.update(cur_stats)
    write_stats(infile.replace('.png', '_stats_pbc.txt'), stats)

if __name__ == '__main__':
    infile = 'docs/vessel_small.png'
    batch(infile)
