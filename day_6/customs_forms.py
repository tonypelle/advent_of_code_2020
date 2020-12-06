import collections
import os
import re
import sys

def read_lines(input_file):
	with open(input_file, 'r') as fp:
		for line in fp.readlines():
			yield line.strip()


def read_groups(input_file):
	group = []
	for line in read_lines(input_file):
		if not line.strip():
			yield group
			group = []
		else:
			group.append(set([i for i in line.strip()]))
	yield group

def main():
	total_1 = 0
	total_2 = 0
	for group in read_groups("input.txt"):
		all_yeses = set()
		a, group = group[0], group[1:]
		all_yeses.update(a)
		for m in group:
			all_yeses.update(m)
			a.intersection_update(m)

		total_1 += len(all_yeses)
		total_2 += len(a)
	print("part 1", total_1)
	print("part 2", total_2)

if __name__ == '__main__':
	main()
