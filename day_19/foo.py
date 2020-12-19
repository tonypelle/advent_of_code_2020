import collections
import functools
import itertools
import os
import math
import re
import sys

from aoc_utils import *
from aoc_utils.data import *

def match_rule_id(rule_id, line, i, non_term_rules, term_rules):
    if i >= len(line):
        return

    if rule_id in term_rules:
        if line[i] == term_rules[rule_id]:
            yield i + 1
    else:
        for frag in non_term_rules[rule_id]:
            for next_i in match_fragment(frag, line, i, non_term_rules, term_rules):
                yield next_i

def match_fragment(fragment, line, i, non_term_rules, term_rules):
    rule_id, remaining_fragment = fragment[0], fragment[1:]
    for next_i in match_rule_id(rule_id, line, i, non_term_rules, term_rules):
        if remaining_fragment:
            for next_next_i in match_fragment(remaining_fragment, line, next_i, non_term_rules, term_rules):
                yield next_next_i
        else:
            yield next_i

def match(rule_id, line, non_term_rules, term_rules):
    return any(matched_len == len(line) for matched_len in match_rule_id(rule_id, line, 0, non_term_rules, term_rules))

def main():
    do_rules = True
    rules = {}
    lines = []

    for line in read_lines():
        if not line:
            do_rules = False
            continue

        if do_rules:
            rule_id, rule = line.split(':')
            rules[rule_id] = [part.split() for part in rule.strip().split('|')]
        else:
            lines.append(line)

    term_rules = {}
    non_term_rules = {}
    for rule_id, parts in rules.items():
        if len(parts) == 1 and len(parts[0]) == 1:
            m = re.match(r'^"(.+?)"$', parts[0][0])
            if m:
                term_rules[int(rule_id)] = m.group(1)
                continue
        non_term_rules[int(rule_id)] = [[int(p) for p in part] for part in parts]

    part1 = sum(1 for line in lines if match(0, line, non_term_rules, term_rules))

    non_term_rules[8] = [[42], [42, 8]]
    non_term_rules[11] = [[42, 31], [42, 11, 31]]
    part2 = sum(1 for line in lines if match(0, line, non_term_rules, term_rules))
    print('part 1=', part1)
    print('part 2=', part2)
    assert(part1 == 224)
    assert(part2 == 436)

if __name__ == '__main__':
    main()
