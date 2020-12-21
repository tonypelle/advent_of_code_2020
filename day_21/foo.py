import collections
import functools
import itertools
import os
import math
import re
import sys
import time

from aoc_utils import *
from aoc_utils.data import *

def main():
    possible_ingredients = collections.defaultdict(list)
    all_ingredients = set()
    all_alergens = set()
    ingredient_counts = collections.defaultdict(int)

    regex = re.compile(r'(.+) \(contains (.+)\)$')

    for line in read_lines():
        ingredients, alergens = regex.match(line).group(1, 2)
        ingredients = ingredients.split()
        alergens = [a.strip() for a in alergens.split(',')]
        for i in ingredients:
            all_ingredients.add(i)
            ingredient_counts[i] += 1
        for a in alergens:
            possible_ingredients[a].append(set(ingredients))
            all_alergens.add(a)

    t1 = time.perf_counter()
    alergen_to_ingredient_map = dict()

    ingredients_with_alergens = set()
    for a in all_alergens:
        ingredient_sets = functools.reduce(lambda a, b: a.intersection(b), possible_ingredients[a])
        ingredients_with_alergens.update(ingredient_sets)
        alergen_to_ingredient_map[a] = ingredient_sets

    ingredients_without_alergens = all_ingredients - ingredients_with_alergens
    part1 = sum(ingredient_counts[i] for i in ingredients_without_alergens)
    t2 = time.perf_counter()

    final_alergen_to_ingredient_map = {}
    while alergen_to_ingredient_map:
        for a, ingredients in alergen_to_ingredient_map.items():
            if len(ingredients) == 1:
                ingredient = ingredients.pop()
                final_alergen_to_ingredient_map[a] = ingredient
                del alergen_to_ingredient_map[a]
                for i_s in alergen_to_ingredient_map.values():
                    i_s.discard(ingredient)
                break

    part2 = ','.join(i for _, i in sorted(list(final_alergen_to_ingredient_map.items()), key=lambda v: v[0]))

    t3 = time.perf_counter()
    print('part 1=', part1, " ms: {:6.2f}".format((t2 - t1)*1000))
    print('part 2=', part2, " ms: {:6.2f}".format((t3 - t2)*1000))

if __name__ == '__main__':
    main()
