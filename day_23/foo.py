import collections
import functools
import itertools
import os
import math
import re
import sys
import time

from aoc_utils import *
from aoc_utils.data import *

class Node(object):
    def __init__(self, value):
        self.value_ = value
        self.next_ = None

    def __eq__(self, other_node):
        return self.value_ == other_node.value_

    def __neq__(self, other_node):
        return self.value_ != other_node.value_

    def __str__(self):
        return str(self.value_)

def loop(start_node):
    node = start_node
    yield node
    while node.next_ != start_node:
        yield node.next_
        node = node.next_

def remove_next(node):
    n = node.next_
    node.next_ = n.next_
    n.next_ = None
    return n

def insert_next(node, next_node):
    next_node.next_ = node.next_
    node.next_ = next_node
    return node



def crab_walk(start_node, nodes_map, num_iterations, max_value):
    current = start_node
    for move in range(num_iterations):
        ccup = current.value_

        a = remove_next(current)
        b = remove_next(current)
        c = remove_next(current)
        abc = [a, b, c]

        abc_values = {a.value_, b.value_, c.value_}
        dest = ccup - 1
        while dest > 0 and dest in abc_values:
            dest -= 1
        if dest == 0:
            dest = max_value
            while dest in abc_values:
                dest -= 1

        dest_node = nodes_map[dest]

        insert_next(dest_node, c)
        insert_next(dest_node, b)
        insert_next(dest_node, a)

        current = current.next_

    return nodes_map[1]

def gen_nodes(data, extend_to=None):
    nums = [int(x) for x in data]
    highest = max(nums)

    if extend_to is not None:
        nums.extend(range(highest + 1, extend_to+1))
        highest = extend_to

    all_nodes = [Node(x) for x in nums]
    nodes_map = {}
    for i, node in enumerate(all_nodes):
        nodes_map[node.value_] = node
        node.next_ = all_nodes[ (i+1) % len(all_nodes) ]

    return all_nodes[0], nodes_map, highest

def main():
    data = list('739862541')

    t1 = time.perf_counter()
    current, nodes_map, highest = gen_nodes(data)
    node_1 = crab_walk(current, nodes_map, 100, highest)
    t2 = time.perf_counter()

    part1 = ''.join([str(n) for n in loop(node_1)][1:])
    print('part 1=', part1, " ms: {:6.2f}".format((t2 - t1)*1000))

    t3 = time.perf_counter()
    current, nodes_map, highest = gen_nodes(data, extend_to=1_000_000)
    node_1 = crab_walk(current, nodes_map, 10_000_000, highest)
    t4 = time.perf_counter()

    a = node_1.next_.value_
    b = node_1.next_.next_.value_
    part2 = a * b
    print('part 2=', part2, " ms: {:6.2f}".format((t4 - t3)*1000))

if __name__ == '__main__':
    main()
