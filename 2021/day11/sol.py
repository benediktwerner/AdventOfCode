#!/usr/bin/env python3

from os import path
import itertools


def neighbors(coord):
    x, y = coord
    for xd in (-1, 0, 1):
        for yd in (-1, 0, 1):
            if xd == 0 and yd == 0:
                continue
            c = x + xd, y + yd
            if c in grid:
                yield c


def try_flash(k):
    if grid[k] <= 9 or k in flashed:
        return

    flashed.add(k)

    for n in neighbors(k):
        grid[n] += 1
        try_flash(n)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = {}

    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = int(c)

    part1 = 0
    part2 = None

    for i in itertools.count(1):
        flashed = set()

        for k in grid:
            grid[k] += 1

        for k in grid:
            try_flash(k)

        for k, v in grid.items():
            if v > 9:
                grid[k] = 0

        if i <= 100:
            part1 += len(flashed)
        if part2 is None and len(flashed) == len(grid):
            part2 = i
        if i >= 100 and part2 is not None:
            break

    print("Part 1:", part1)
    print("Part 2:", part2)
