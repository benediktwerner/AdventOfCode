#!/usr/bin/env python3

from os import kill, path
import itertools
import math
import re


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    ingredients = [ints(line) for line in f.read().splitlines()]
    best1, best2 = 0, 0
    for a in range(101):
        for b in range(101 - a):
            for c in range(101 - a - b):
                d = 100 - a - b - c
                attrs = [0] * 5
                for ing, amnt in zip(ingredients, (a, b, c, d)):
                    for i, x in enumerate(ing):
                        attrs[i] += x * amnt
                score = math.prod(max(0, x) for x in attrs[:-1])
                best1 = max(best1, score)
                if attrs[-1] == 500:
                    best2 = max(best2, score)
    print("Part 1:", best1)
    print("Part 2:", best2)
