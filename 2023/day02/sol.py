#!/usr/bin/env python3

from os import path

import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1, part2 = 0, 0
    for i, line in enumerate(f.read().splitlines()):
        rounds = line.split(": ")[1].split(";")
        mins = {"red": 0, "green": 0, "blue": 0}
        maxs = {"red": 12, "green": 13, "blue": 14}
        wrong = False
        for r in rounds:
            for cubes in r.split(", "):
                n, c = cubes.split()
                n = int(n)
                mins[c] = max(mins[c], n)
                if n > maxs[c]:
                    wrong = True
        if not wrong:
            part1 += i + 1
        part2 += math.prod(mins.values())

    print("Part 1:", part1)
    print("Part 2:", part2)
