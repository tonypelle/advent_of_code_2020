import collections
import os
import re
import sys

from aoc_utils.data import *

def find_pair(data, total):
    for i, a in enumerate(data):
        for j, b in enumerate(data):
            if i == j:
                continue
            if a + b == total:
                return True

def main():
    data = [int(i) for i in read_lines()]

    for i, value in enumerate(data[25:]):
        preamble = data[i:i+25]
        assert(len(preamble) == 25)
        if find_pair(preamble, value):
            continue
        else:
            target = value
            break

    print('part 1 =', target)

    for i in range(len(data)-1):
        s = data[i]
        for j in range(i+1, len(data)):
            s += data[j]
            if s == target:
                small, large = min(data[i:j+1]), max(data[i:j+1])
                print('part 2 =', small + large)
                return

if __name__ == '__main__':
    main()
