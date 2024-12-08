#!/usr/bin/env python3

from os import path
from collections import defaultdict
import itertools

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    lines = file.read().splitlines()
    width, height = len(lines[0]), len(lines)
    antennas = defaultdict(list)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != ".":
                antennas[c].append((x, y))

    part1, part2 = set(), set()

    for points in antennas.values():
        for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
            dx, dy = x1 - x2, y1 - y2

            for i in (1, -2):
                nx, ny = x1 + i * dx, y1 + i * dy
                if 0 <= nx < width and 0 <= ny < height:
                    part1.add((nx, ny))

            for d in (1, -1):
                for i in itertools.count(step=d):
                    nx, ny = x1 + i * dx, y1 + i * dy
                    if 0 <= nx < width and 0 <= ny < height:
                        part2.add((nx, ny))
                    else:
                        break

    print("Part 1:", len(part1))
    print("Part 2:", len(part2))
