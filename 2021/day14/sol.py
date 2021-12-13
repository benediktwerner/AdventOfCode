#!/usr/bin/env python3

from os import path
from collections import Counter
from functools import lru_cache


@lru_cache(maxsize=None)
def count(poly, n):
    if n == 0:
        return Counter(poly)

    if len(poly) > 2:
        return sum(
            (count(poly[i : i + 2], n) for i in range(len(poly) - 1)), Counter()
        ) - Counter(poly[1:-1])

    new = rules[poly]
    return count(poly[0] + new, n - 1) + count(new + poly[1], n - 1) - Counter(new)


def solve(n):
    c = count(poly, n)
    most_common = c.most_common()
    return most_common[0][1] - most_common[-1][1]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    poly = lines[0]
    rules = dict(rule.split(" -> ") for rule in lines[2:])

    print("Part 1:", solve(10))
    print("Part 2:", solve(40))
