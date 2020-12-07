import os
import sys

def get_input_filename(input_file='input.txt'):
	return os.path.join(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)), input_file)

def read_lines(input_file=None):
	if input_file is None:
		input_file = get_input_filename()
	with open(input_file, 'r') as fp:
		for line in fp.readlines():
			yield line.strip()


def read_groups(input_file=None):
	if input_file is None:
		input_file = get_input_filename()
	group = []
	for line in read_lines(input_file):
		if not line.strip():
			yield group
			group = []
		else:
			group.append(line.strip())
	if group:
		yield group
