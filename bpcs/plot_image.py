import os
import subprocess
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from text_to_image import str_to_words, get_word_color_map_fcn

def randrange(vmin, vmax):
    return (vmax-vmin)*np.random.rand(1) + vmin

def get_word_colors(infile):
    txt = open(infile).read()
    words = str_to_words(txt, True)
    get_color = get_word_color_map_fcn(words)
    for word in words:
        yield word, get_color(word)
    # return dict((word, get_color(word)) for word in words)

def hist(infile):
    words = open(infile).read().split()
    base = sorted(list(set(words)))
    inds = [base.index(word) for word in words]

    # colors = list(get_word_colors(infile))
    # reds = [r for word, (r,g,b) in colors if word.strip()]
    # greens = [g for word, (r,g,b) in colors if word.strip()]
    # blues = [b for word, (r,g,b) in colors if word.strip()]

    # popular = [word for word, (r,g,b) in colors if g == 135]
    # print ', '.join(popular)
    # popular = [word for word, (r,g,b) in colors if b == 163]
    # print ', '.join(popular)
    # popular = [word for word, (r,g,b) in colors if r == 17]
    # print ', '.join(popular)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(inds, len(base), facecolor='red', alpha=0.75)
    # ax = fig.add_subplot(311)
    # n, bins, patches = ax.hist(reds, 256, facecolor='red', alpha=0.75)
    # ax = fig.add_subplot(312)
    # n, bins, patches = ax.hist(greens, 256, facecolor='green', alpha=0.75)
    # ax = fig.add_subplot(313)
    # n, bins, patches = ax.hist(blues, 256, facecolor='blue', alpha=0.75)
    plt.show()

def plot(infile):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')

    n = 100
    c, m = ('r', 'o')
    for word, (r,g,b) in get_word_colors(infile):
        ax.scatter(r, g, b, c=c, marker=m)
        if word.strip():
            print word.strip()
            subprocess.os.popen('say ' + word.strip())
        plt.pause(0.01)
        plt.draw()

def main(infile):
    hist(infile)
    # plot(infile)

if __name__ == '__main__':
    infile = 'docs/tmp.txt'
    main(infile)
