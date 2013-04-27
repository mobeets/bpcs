
def alpha_batch(infile, name, action, alphas):
    params = get_params(action)
    nflippeds = {}
    for alpha in alphas:
        params.custom['alpha'] = alpha
        outfile = infile.replace('.', '_{2}_{1}_p{0}.'.format(int(alpha*100), 'cgc' if params.gray else 'pbc', name))
        # print alpha
        log.critical('---------------------\n' + outfile + '\n---------------------')
        nflipped = act_on_image(infile, outfile, params)
        nflippeds[(name, alpha)] = nflipped
    return nflippeds

def write_stats(outfile, stats):
    out = ''
    for (name, alpha), n in stats.iteritems():
        out += '{0},{1},{2}\n'.format(name, alpha, n)
    with open(outfile, 'w') as f:
        f.write(out)
    
def batch(infile):
    alphas = [0.3 + (a/100.0) for a in range(20)]
    stats = {}
    for action in actions:
        name = 'complexified' if 'simpl' in action else 'simplified'
        cur_stats = alpha_batch(infile, name, action, alphas)
        stats.update(cur_stats)
    write_stats(infile.replace('.png', '_stats_pbc.txt'), stats)
