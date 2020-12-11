import collections
import itertools
import os
import re
import sys

from aoc_utils.data import *

def num_adjacent(grid, start_x, start_y):
    count = 0
    for y in range(max(0, start_y - 1), min(len(grid), start_y + 2)):
        row = grid[y]
        for x in range(max(0, start_x - 1), min(len(row), start_x + 2)):
            if x == start_x and y == start_y:
                continue
            if row[x] == '#':
                count += 1
    return count

def search_(grid, start_x, start_y, dx, dy):
    x = start_x + dx
    y = start_y + dy
    while True:
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            return 0
        if grid[y][x] == 'L':
            return 0
        if grid[y][x] == '#':
            return 1
        x += dx
        y += dy

def search(grid, x, y):
    num_occupied = 0
    for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        num_occupied += search_(grid, x, y, dx, dy)
    return num_occupied

def solve(grid, search_func, threshold):
    changed = True
    while changed:
        changed = False
        new_grid = []
        for y, row in enumerate(grid):
            new_row = row[:]
            for x, seat in enumerate(row):
                if seat == 'L' and search_func(grid, x, y) == 0:
                    new_row[x] = '#'
                    changed = True
                elif seat == '#' and search_func(grid, x, y) >= threshold:
                    new_row[x] = 'L'
                    changed = True
            new_grid.append(new_row)
        grid = new_grid
    return grid

def main():
    grid = [list(row) for row in read_lines()]

    grid1 = solve(grid, num_adjacent, 4)
    num_occupied1 = sum(row.count('#') for row in grid1)
    print('part 1 =', num_occupied1)

    grid2 = solve(grid, search, 5)
    num_occupied2 = sum(row.count('#') for row in grid2)
    print('part 2 =', num_occupied2)

if __name__ == '__main__':
    main()
