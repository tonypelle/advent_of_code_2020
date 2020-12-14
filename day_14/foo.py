import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils.data import *

def floating(mask_string, addr, i=0):
    if i == len(mask_string):
        yield 0x0
    else:
        bit = 0x1 << (35 - i)
        if mask_string[i] == '0':
            prefix = [addr & bit]
        elif mask_string[i] == '1':
            prefix = [bit]
        else:
            prefix = [0x0, bit]

        for floating_addrs in floating(mask_string, addr, i+1):
            for p in prefix:
                yield p | floating_addrs

def to_mask(mask_string, func):
    bitmask = 0
    bit = 0x1
    for mask_char in reversed(mask_string):
        if func(mask_char):
            bitmask |= bit
        bit <<= 1
    return bitmask

def main():
    mem_line_re = re.compile(r'mem\[(\d+)\] = (\d+)')
    mask_re = re.compile(r'mask = ([01X]{36})$')

    mem = collections.defaultdict(int)
    for line in read_lines():
        if line.startswith('mask'):
            mask_string = mask_re.match(line).group(1)
            or_mask = to_mask(mask_string, lambda b: b == '1')
            and_mask = to_mask(mask_string, lambda b: b != '0')
        else:
            addr, value = [int(v) for v in mem_line_re.match(line).group(1, 2)]
            mem[addr] = (value & and_mask) | or_mask
    print('part 1 =', sum(mem.values()))

    mem = collections.defaultdict(int)
    for line in read_lines():
        if line.startswith('mask'):
            mask_string = mask_re.match(line).group(1)
        else:
            addr, value = mem_line_re.match(line).group(1, 2)
            value = int(value)
            for a in floating(mask_string, int(addr)):
                mem[a] = value

    print('part 2 =', sum(mem.values()))

if __name__ == '__main__':
    main()
