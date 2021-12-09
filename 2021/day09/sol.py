#!/usr/bin/env python3

from os import path
from math import prod


def neighbors(coord):
    x, y = coord
    for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        c = x + xd, y + yd
        if c in grid:
            yield c, grid[c]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = {}

    for y, line in enumerate(f.read().splitlines()):
        for x, height in enumerate(line):
            grid[x, y] = int(height)

    low_points = [
        coord
        for coord, height in grid.items()
        if all(nh > height for _, nh in neighbors(coord))
    ]

    basins = []

    for lp in low_points:
        todo = [coord for coord, height in neighbors(lp) if height < 9]
        done = set(todo)
        size = 1
        while todo:
            coord = todo.pop()
            size += 1
            height = grid[coord]
            for n, nh in neighbors(coord):
                if height < nh < 9 and n not in done:
                    todo.append(n)
                    done.add(n)
        basins.append(size)

    basins.sort()

    print("Part 1:", sum(grid[lp] + 1 for lp in low_points))
    print("Part 2:", prod(basins[-3:]))
