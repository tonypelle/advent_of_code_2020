import collections
import os
import re
import sys

from aoc_utils.data import *

def can_contain(containing_bags, color):
	all_bags = set()
	stack_o_bags = [color]

	while stack_o_bags:
		inner_bag, stack_o_bags = stack_o_bags[0], stack_o_bags[1:]
		c = containing_bags[inner_bag]
		all_bags.update(c)
		stack_o_bags.extend(c)
	return all_bags

def count_bags(bags, color):
	total = 0
	for inner_bag, num_bags in bags[color]:
		total += num_bags + num_bags * count_bags(bags, inner_bag)
	return total

def main():
	outer_bag_re = re.compile(r'^(.+) bags contain (.*)\.$')
	contains_re = re.compile(r'^(\d+) (.*?) bags?$')
	bags = collections.defaultdict(set)
	containing_bags = collections.defaultdict(set)
	for line in read_lines():
		m = outer_bag_re.match(line)
		assert(m)
		outer_bag, contains = m.groups()

		if contains == 'no other bags':
			continue

		for c in contains.split(', '):
			count, color = contains_re.match(c).groups()
			containing_bags[color].add(outer_bag)
			bags[outer_bag].add((color, int(count)))

	print('part 1 =', len(can_contain(containing_bags, 'shiny gold')))
	print('part 2 =', count_bags(bags, 'shiny gold'))


if __name__ == '__main__':
	main()
