import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils.data import *

def game(inputs, target):
    mem = dict((n, (i, )) for i, n in enumerate(inputs))
    last_n = inputs[-1]
    for i in range(len(inputs), target):
        last_pos = mem[last_n]
        if len(last_pos) == 1:
            n = 0
        else:
            n = last_pos[1] - last_pos[0]
        last_n = n

        x = mem.get(n)
        mem[n] = (x[-1], i) if x else (i, )
    return n

def main():
    inputs = [0,1,4,13,15,12,16]

    print('example =', game([0,3,6], 2020))
    print('part 1 =', game(inputs, 2020))
    print('part 2 =', game(inputs, 30_000_000))

if __name__ == '__main__':
    main()
