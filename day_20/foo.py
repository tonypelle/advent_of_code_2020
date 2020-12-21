import collections
import copy
import functools
import itertools
import os
import math
import re
import sys
import time

from aoc_utils import *
from aoc_utils.data import *

class Tile(object):
    def __init__(self, tile_id, tile_data, orientation):
        self._tile_id = tile_id
        self._top = tile_data[0]
        self._bottom = tile_data[-1]
        self._left = ''.join(x[0] for x in tile_data)
        self._right = ''.join(x[-1] for x in tile_data)
        self._orientation = orientation
        self._image_data = [tile_data[y][1:-1] for y in range(1, len(self._left)-1)]

    def __str__(self):
        return "{:4}[{}]".format(self._tile_id, self._orientation)

    def __repr__(self):
        return "Tile({}, {})".format(self._tile_id, self._orientation)

    @property
    def image_data(self):
        return self._image_data
    
    @property
    def tile_id(self):
        return self._tile_id

    @property
    def top(self):
        return self._top
    
    @property
    def bottom(self):
        return self._bottom
    
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right
    
    @property
    def orientation(self):
        return self._orientation

    def is_left_of(self, other_tile):
        return self._right == other_tile._left

    def is_right_of(self, other_tile):
        return self._left == other_tile._right
    
    def is_above(self, other_tile):
        return self._bottom == other_tile._top

    def is_below(self, other_tile):
        return self._top == other_tile._bottom

def print_grid(grid):
    for y in range(len(grid[0])):
        print(' '.join(str(grid[x][y]) for x in range(len(grid))))
    print()

def is_corner(tile, tops, bottoms, lefts, rights):
    has_above = any(True for i in bottoms[tile.top] if i.tile_id != tile.tile_id)
    has_below = any(True for i in tops[tile.bottom] if i.tile_id != tile.tile_id)
    has_left = any(True for i in rights[tile.left] if i.tile_id != tile.tile_id)
    has_right = any(True for i in lefts[tile.right] if i.tile_id != tile.tile_id)
    return not has_above and has_below and not has_left and has_right

def fill_grid(grid, i, remaining_tiles, dim):
    x, y = i // dim, i % dim

    if i == (dim * dim):
        assert(not remaining_tiles)
        yield grid
        return

    for ts, tile_set in enumerate(remaining_tiles):
        for tile in tile_set:
            if (x == 0 or tile.is_right_of(grid[x-1][y])) and (y == 0 or tile.is_below(grid[x][y-1])):
                new_grid = copy.deepcopy(grid)
                new_grid[x][y] = tile
                for ng in fill_grid(new_grid, i + 1, remaining_tiles[:ts] + remaining_tiles[ts+1:], dim):
                    yield ng

def find_grid(dim, corners, all_tile_ids, grouped_tiles):
    for corner in corners:
        remaining_tile_ids = all_tile_ids - {corner.tile_id}
        grid = [[None for _ in range(dim)] for _ in range(dim)]
        grid[0][0] = corner

        for new_grid in fill_grid(grid, 0, list(grouped_tiles.values()), dim):
            return new_grid

def rot_func(n):
    return {0: lambda x, y, dim_x, dim_y: (x, y),
            1: lambda x, y, dim_x, dim_y: (y, dim_x-x),
            2: lambda x, y, dim_x, dim_y: (dim_x-x, dim_y-y),
            3: lambda x, y, dim_x, dim_y: (dim_y-y, x)}[n]

def flip_func(do_flip, func):
    if do_flip:
        return lambda x, y, dim_x, dim_y: func(x, dim_y-y, dim_x, dim_y)
    else:
        return lambda x, y, dim_x, dim_y: func(x, y, dim_x, dim_y)

def xform_func(rots, flip):
    return flip_func(flip, rot_func(rots))

def xform(src_data, rot, flip):
    dim_x = len(src_data[0])
    dim_y = len(src_data)
    xform = xform_func(rot, flip)

    xform_data = []
    for y in range(dim_y):
        row = []
        for x in range(dim_x):
            nx, ny = xform(x, y, dim_x-1, dim_y-1)
            row.append(src_data[ny][nx])
        xform_data.append(''.join(row))
    return xform_data

def all_xforms(data):
    for rot in range(4):
        for flip in range(2):
            yield rot * 2 + flip, xform(data, rot, flip)

def main():
    all_tiles = {}

    if 0:
        fn = 'day_20/example.txt'
        expected_dim = 3
        expected_p1 = 20899048083289
    else:
        fn = None
        expected_dim = 12
        expected_p1 = 84116744709593

    for group in read_groups(fn):
        tile, lines = group[0], group[1:]
        tile_id = int(tile.split()[1][:-1])
        all_tiles[tile_id] = lines

    t1 = time.perf_counter()

    tops = collections.defaultdict(set)
    bottoms = collections.defaultdict(set)
    lefts = collections.defaultdict(set)
    rights = collections.defaultdict(set)

    all_tile_ids = set()
    all_the_damned_tiles = []
    grouped_tiles = collections.defaultdict(list)
    for tile_id, tile_data in all_tiles.items():
        all_tile_ids.add(tile_id)

        for orientation, xform_data in all_xforms(tile_data):
            tile = Tile(tile_id, xform_data, orientation)
            tops[tile.top].add(tile)
            bottoms[tile.bottom].add(tile)
            lefts[tile.left].add(tile)
            rights[tile.right].add(tile)
            all_the_damned_tiles.append(tile)
            grouped_tiles[tile_id].append(tile)

    corners = [tile for tile in all_the_damned_tiles if is_corner(tile, tops, bottoms, lefts, rights)]

    dim = int(math.sqrt(len(all_tile_ids)) + 0.5)
    assert(dim == expected_dim)

    for tiles in tops.values():
        assert(1 <= len(set(t.tile_id for t in tiles)) <= 2)
    for tiles in bottoms.values():
        assert(1 <= len(set(t.tile_id for t in tiles)) <= 2)
    for tiles in lefts.values():
        assert(1 <= len(set(t.tile_id for t in tiles)) <= 2)
    for tiles in rights.values():
        assert(1 <= len(set(t.tile_id for t in tiles)) <= 2)

    if 1:
        grid = find_grid(dim, corners, all_tile_ids, grouped_tiles)
        print_grid(grid)

        part1 = grid[0][0].tile_id * grid[0][dim-1].tile_id * grid[dim-1][0].tile_id * grid[dim-1][dim-1].tile_id

        assert(part1 == expected_p1)
        t2 = time.perf_counter()

        print('part 1=', part1, " ms: {:6.2f}".format((t2 - t1)*1000))

    if 1:
        re0 = re.compile(r'..................#.')
        re1 = re.compile(r'#....##....##....###')
        re2 = re.compile(r'.#..#..#..#..#..#...')

        image = []
        num_hashes = 0
        for y in range(dim):
            images = [grid[x][y].image_data for x in range(dim)]
            for x in range(len(images[0])):
                image.append(''.join([row[x] for row in images]))
                num_hashes += sum(1 for c in image[-1] if c == '#')

        num_matches = 0
        for _, new_image in all_xforms(image):
            for y in range(len(new_image) - 2):
                pos = 0
                while pos < len(new_image[y]):
                    m0 = re0.match(new_image[y], pos)
                    m1 = re1.match(new_image[y+1], pos)
                    m2 = re2.match(new_image[y+2], pos)
                    if m0 and m1 and m2:
                        num_matches += 1
                        pos += 20
                    else:
                        pos += 1

            if num_matches:
                break

        t3 = time.perf_counter()

        print('num_matches=', num_matches)
        print('num_hashes=', num_hashes)
        part2 = num_hashes - num_matches * 15
        print('part 2=', part2, " ms: {:6.2f}".format((t3 - t2)*1000))

if __name__ == '__main__':
    main()
