import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils import *
from aoc_utils.data import *

digits = set(str(i) for i in range(10))

def tokenize(line):
    line = iter(line)
    while True:
        try:
            c = next(line)
        except StopIteration:
            break
        if not c:
            break
        if c == ' ':
            continue
        if c in digits:
            val = ''
            while c is not None and c in digits:
                val += c
                try:
                    c = next(line)
                except StopIteration:
                    break
            yield int(val)
        if c in ('*', '+', '(', ')'):
            yield c

def to_lists(token_iter):
    result = []
    while True:
        try:
            token = next(token_iter)
            if token == '(':
                result.append(to_lists(token_iter))
            elif token == ')':
                return result
            else:
                result.append(token)
        except StopIteration:
            return result

def part1(vals):
    if len(vals) == 1:
        return vals[0]
    else:
        vals, op, right = vals[:-2], vals[-2], vals[-1]
        if op == '+':
            return part1(vals) + right
        elif op == '*':
            return part1(vals) * right
        else:
            assert(False)

def part2(vals):
    try:
        i = vals.index('*')
        return part2(vals[:i]) * part2(vals[i+1:])
    except ValueError:
        pass

    try:
        i = vals.index('+')
        return part2(vals[:i]) + part2(vals[i+1:])
    except ValueError:
        pass

    assert(len(vals) == 1)
    return vals[0]

def evaluate(tree, do_math):
    flattened = []
    for node in tree:
        if type(node) is list:
            flattened.append(evaluate(node, do_math))
        else:
            flattened.append(node)
    return do_math(flattened)

def eval_expr(line, do_math):
    return evaluate(to_lists(iter(tokenize(line))), do_math)

def main():
    total = sum(eval_expr(line, do_math=part1) for line in read_lines())
    print('part 1 =', total)

    total = sum(eval_expr(line, do_math=part2) for line in read_lines())
    print('part 2 =', total)

if __name__ == '__main__':
    main()
