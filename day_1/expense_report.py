#!/bin/env python3

if __name__ == '__main__':
	with open('input.txt', 'r') as fp:
		vals = [int(line.strip()) for line in fp.readlines()]
		for i, a in enumerate(vals[:-1]):
			for b in vals[i+1:]:
				if a + b == 2020:
					print(a, b, a+b, a*b)
