import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils import *
from aoc_utils.data import *

def neighbours(*args, middle=True):
    c, args = args[0], args[1:]
    if args:
        for i in [-1, 0, 1]:
            for a in neighbours(*args, middle=middle and i == 0):
                yield [c + i] + a
    else:
        yield [c - 1]
        if not middle:
            yield [c]
        yield [c + 1]

def lookup(cube, *args):
    while args:
        c, args = args[0], args[1:]
        if c >= 0 and c < len(cube):
            if args:
                cube = cube[c]
            else:
                return cube[c]
        else:
            return '.'

def num_active(cube, *args):
    return sum(1 for n in neighbours(*args) if lookup(cube, *n) == '#')

def total_active(cube, depth):
    if depth > 1:
        return sum(total_active(sub, depth-1) for sub in cube)
    else:
        return sum(1 for x in cube if x == '#')

def iterate(cube, dimensions, *coords):
    dim, dimensions = dimensions[0], dimensions[1:]
    if dimensions:
        return [iterate(cube, dimensions, *coords, c) for c in range(-1, dim+1)]
    else:
        row = []
        for c in range(-1, dim+1):
            active = num_active(cube, *coords, c)
            if lookup(cube, *coords, c) == '#':
                row.append('#' if active in (2, 3) else '.')
            else:
                row.append('#' if active == 3 else '.')
        return row

def main():

    cube3 = [[list(line) for line in read_lines()]]
    for _ in range(6):
        sx = len(cube3)
        sy = len(cube3[0])
        sz = len(cube3[0][0])
        cube3 = iterate(cube3, (sx, sy, sz))
    print('part 1 =', total_active(cube3, 3))

    cube4 = [[[list(line) for line in read_lines()]]]
    for _ in range(6):
        sx = len(cube4)
        sy = len(cube4[0])
        sz = len(cube4[0][0])
        sw = len(cube4[0][0][0])
        cube4 = iterate(cube4, (sx, sy, sz, sw))
    print('part 2 =', total_active(cube4, 4))

if __name__ == '__main__':
    main()
