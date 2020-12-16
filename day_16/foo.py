import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils.data import *

def valid(n, a, b):
    return (a[0] <= n <= a[1]) or (b[0] <= n <= b[1])

def is_valid(n, fields):
    for a, b in fields.values():
        if valid(n, a, b):
            return True

def read_data():
    fields = collections.OrderedDict()

    lines = iter(read_lines())
    line = next(lines)
    while line:
        field, a0, a1, b0, b1 = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)$', line).groups()
        fields[field] = (int(a0), int(a1)), (int(b0), int(b1))
        line = next(lines)

    line = next(lines) # burn it: your ticket
    line = next(lines)
    my_ticket = [int(x) for x in line.split(',')]

    line = next(lines) # burn it: nearby tickets
    line = next(lines)

    other_tickets = []
    while True:
        try:
            other_tickets.append([int(x) for x in next(lines).split(',')])
        except StopIteration:
            break
    return fields, my_ticket, other_tickets

def main():
    fields, my_ticket, other_tickets = read_data()

    total = 0
    valid_tickets = []
    for ticket in other_tickets:
        invalid_fields = [n for n in ticket if not is_valid(n, fields)]
        if invalid_fields:
            total += sum(invalid_fields)
        else:
            valid_tickets.append(ticket)

    assert(total == 18227)
    print('part 1 =', total)

    possible_fields = [set(fields.keys()) for _ in my_ticket]

    for ticket in valid_tickets:
        for col, val in enumerate(ticket):
            for field, (a, b) in fields.items():
                if not valid(val, a, b):
                    possible_fields[col].remove(field)

    possible_fields = collections.deque(sorted([(col, choices) for col, choices in enumerate(possible_fields)], key=lambda x: len(x[1])))

    finals = []

    while possible_fields:
        col, choices =  possible_fields.popleft()
        assert(len(choices) == 1)
        field = choices.pop()

        finals.append((col, field))

        for _, choices in possible_fields:
            choices.discard(field)

    cols = [col for col, field in finals if field.startswith('departure')]
    assert(len(cols) == 6)
    total = functools.reduce(lambda x, y: x*y, [val for col, val in enumerate(my_ticket) if col in cols])
    assert(total == 2355350878831)
    print('part 2 =', total)

if __name__ == '__main__':
    main()
