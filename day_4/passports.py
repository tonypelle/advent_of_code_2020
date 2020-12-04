import os
import re

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
valid_eye_colours = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

year_re = re.compile(r'^\d{4}$')
height_re = re.compile(r'^(\d+)(in|cm)$')
colour_re = re.compile(r'^#[a-f0-9]{6}$')
pid_re = re.compile(r'^[0-9]{9}$')

def check_year(value, min_val, max_val):
	return year_re.match(value) and int(value) >= min_val and int(value) <= max_val

def check_height(value):
	m = height_re.match(value)
	if not m:
		return False

	h, units = m.groups([1, 2])
	h = int(h)
	return (units == 'cm' and h >= 150 and h <= 193) or (units == 'in' and h >= 59 and h <= 76)

def check_validity(passport):
	if required_fields - set(passport.keys()):
		return False

	if not check_year(passport['byr'], 1920, 2002):
		return False
	if not check_year(passport['iyr'], 2010, 2020):
		return False
	if not check_year(passport['eyr'], 2020, 2030):
		return False
	if not check_height(passport['hgt']):
		return False
	if not colour_re.match(passport['hcl']):
		return False
	if not pid_re.match(passport['pid']):
		return False
	if passport['ecl'] not in valid_eye_colours:
		return False

	return True

def read_passports(input_file):
	passport = {}
	with file(input_file, 'r') as fp:
		for line in fp.readlines():
			if not line.strip():
				yield passport
				passport = {}
			else:
				parts = line.split()
				for part in parts:
					k, v = part.split(':')
					passport[k] = v
	if passport:
		yield passport
	
if __name__ == '__main__':
	invalid = 0
	valid = 0
	for passport in read_passports('input.txt'):
		if check_validity(passport):
			valid += 1
		else:
			invalid += 1
	print("Invalid", invalid)
	print("Valid", valid)
