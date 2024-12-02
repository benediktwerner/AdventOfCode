#!/usr/bin/env python3

from os import path
from collections import Counter


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    lefts = []
    rights = []
    for line in file.read().splitlines():
        left, right = map(int, line.split())
        lefts.append(left)
        rights.append(right)
    lefts.sort()
    rights.sort()

    part1 = 0
    for left, right in zip(lefts, rights):
        part1 += abs(left - right)
    print("Part 1:", part1)

    part2 = 0
    right_counts = Counter(rights)
    for n in lefts:
        part2 += n * right_counts[n]
    print("Part 2:", part2)
