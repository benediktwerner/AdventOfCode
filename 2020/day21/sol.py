#!/usr/bin/env python3

from os import path
from functools import reduce
from collections import Counter

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    could_be_in = {}
    count = Counter()
    for line in f.read().splitlines():
        ingredients, allergens = line.split(" (contains ")
        ingredients = set(ingredients.split())
        allergens = allergens[:-1].split(", ")

        count.update(ingredients)

        for a in allergens:
            if a in could_be_in:
                could_be_in[a] &= ingredients
            else:
                could_be_in[a] = set(ingredients)

    could_be_alergic = reduce(set.__or__, could_be_in.values(), set())
    print("Part 1:", sum(c for i, c in count.items() if i not in could_be_alergic))

    mapping = []
    while could_be_in:
        new = []
        for a, ii in could_be_in.items():
            if len(ii) == 1:
                new.append((a, ii.pop()))

        for a, i in new:
            del could_be_in[a]
            for v in could_be_in.values():
                if i in v:
                v.remove(i)

        mapping += new

    mapping.sort()
    print("Part 2:", ",".join(i for _, i in mapping))
