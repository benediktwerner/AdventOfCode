#!/usr/bin/env python3

from os import path
import string

prio = string.ascii_lowercase + string.ascii_uppercase

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()

    part1 = 0
    for line in lines:
        half = len(line) // 2
        a, b = line[:half], line[half:]
        part1 += sum(prio.index(c) + 1 for c in set(a) & set(b))
    print("Part 1:", part1)

    part2 = 0
    for a, b, c in zip(lines[::3], lines[1::3], lines[2::3]):
        part2 += sum(prio.index(c) + 1 for c in set(a) & set(b) & set(c))
    print("Part 2:", part2)
