import collections
import itertools
import os
import math
import re
import sys

from aoc_utils.data import *

def move(x, y, direction, distance):
    if direction == 'N':
        return x, y + distance
    elif direction == 'E':
       return x + distance, y
    elif direction == 'S':
        return x, y - distance
    elif direction == 'W':
        return x - distance, y
    assert(False)

def pivot_left(degrees, x, y):
    if degrees == 90:
        return -y, x
    elif degrees == 180:
        return -x, -y
    elif degrees == 270:
        return y, -x
    elif degrees == 360:
        return x, y
    assert(False)

def pivot_right(degrees, x, y):
    if degrees == 90:
        return y, -x
    elif degrees == 180:
        return -x, -y
    elif degrees == 270:
        return -y, x
    elif degrees == 360:
        return x, y
    assert(False)

def main():
    dirs = [(row[0], int(row[1:])) for row in read_lines()]
    left = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
    right = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

    ship_x, ship_y = 0, 0
    facing = 'E'
    for instr, param in dirs:
        if instr in ('N', 'E', 'S', 'W'):
            ship_x, ship_y = move(ship_x, ship_y, instr, param)
        elif instr == 'R':
            for _ in range(param // 90):
                facing = right[facing]
        elif instr == 'L':
            for _ in range(param // 90):
                facing = left[facing]
        elif instr == 'F':
            ship_x, ship_y = move(ship_x, ship_y, facing, param)
        else:
            assert(False)

    print('part 1 =', int(math.fabs(ship_x) + math.fabs(ship_y)))

    w_x, w_y = 10, 1
    ship_x, ship_y = 0, 0
    facing = 'E'
    for instr, param in dirs:
        if instr in ('N', 'E', 'S', 'W'):
            w_x, w_y = move(w_x, w_y, instr, param)
        elif instr == 'R':
            w_x, w_y = pivot_right(param, w_x, w_y)
        elif instr == 'L':
            w_x, w_y = pivot_left(param, w_x, w_y)
        elif instr == 'F':
            ship_x += param * w_x
            ship_y += param * w_y
        else:
            assert(False)

    print('part 2 =', int(math.fabs(ship_x) + math.fabs(ship_y)))

if __name__ == '__main__':
    main()
