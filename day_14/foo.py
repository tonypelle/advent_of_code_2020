import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils.data import *

def floating(mask, addr, i=0):
    if i == len(mask):
        return ['']
    else:
        bit = mask[i]
        a = addr[i]
        results = floating(mask, addr, i+1)
        if bit == '0':
            return [a + addr for addr in results]
        elif bit == '1':
            return ['1' + addr for addr in results]
        else:
            return ['0' + addr for addr in results] + ['1' + addr for addr in results]

def binary_string(val, padding=36):
    bstring = bin(int(val))[2:]
    return '0' * (padding - len(bstring)) + bstring

def main():
    mem_line_re = re.compile(r'mem\[(\d+)\] = (\d+)')
    mask_re = re.compile(r'mask = ([01X]{36})$')

    mem = collections.defaultdict(int)
    for line in read_lines():
        if line.startswith('mask'):
            mask = mask_re.match(line).group(1)
            or_mask = int(''.join(['1' if b == '1' else '0' for b in mask]), base=2)
            and_mask = int(''.join(['0' if b == '0' else '1' for b in mask]), base=2)
        else:
            addr, value = [int(v) for v in mem_line_re.match(line).group(1, 2)]
            mem[addr] = (value & and_mask) | or_mask
    print('part 1 =', sum(mem.values()))

    mem = collections.defaultdict(int)
    for line in read_lines():
        if line.startswith('mask'):
            mask = mask_re.match(line).group(1)
        else:
            addr, value = mem_line_re.match(line).group(1, 2)
            addr = binary_string(addr)
            value = int(value)
            assert(len(mask) == len(addr))
            for a in floating(mask, addr):
                mem[int(a, base=2)] = value

    print('part 2 =', sum(mem.values()))

if __name__ == '__main__':
    main()
