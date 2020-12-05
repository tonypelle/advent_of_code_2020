import collections
import os
import re
import sys

def read_lines(input_file):
	with open(input_file, 'r') as fp:
		for line in fp.readlines():
			yield line.strip()

def partition(start, end, lower):
	half = (end - start) // 2
	if lower:
		return start, start + half
	else:
		return start + half + 1, end

def find(vals, start, end, f):
	for i in vals:
		start, end = partition(start, end, f(i))
	return start

def main():
	highest_seat_id = 0
	max_seat_id = 127 * 8 + 7

	seats = set(range(max_seat_id + 1))
	for line in read_lines("input.txt"):
		rows, cols = line[:7], line[7:]
		row = find(rows, 0, 127, lambda i: i == 'F')
		col = find(cols, 0, 7, lambda i: i == 'L')
		seat = row * 8 + col
		highest_seat_id = max(highest_seat_id, seat)
		seats.discard(seat)

	print('highest seat id:', highest_seat_id)
	for seat in seats:
		if seat > 0 and seat <= max_seat_id and (seat - 1) not in seats and (seat + 1) not in seats:
			print('my seat:', seat)

if __name__ == '__main__':
	main()
