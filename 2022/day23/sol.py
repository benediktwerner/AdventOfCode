#!/usr/bin/env python3

from os import path
from collections import defaultdict
import itertools


OPTIONS = (
    ((0, -1), (1, -1), (-1, -1)),  # NORTH
    ((0, 1), (1, 1), (-1, 1)),  # SOUTH
    ((-1, 0), (-1, 1), (-1, -1)),  # WEST
    ((1, 0), (1, 1), (1, -1)),  # EAST
)


def surrounding(x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            if (x + dx, y + dy) in grid:
                return True
    return False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = set()
    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                grid.add((x, y))

    for i in itertools.count():
        proposed = defaultdict(list)
        new_grid = set()

        for x, y in grid:
            if not surrounding(x, y):
                new_grid.add((x, y))
                continue

            for j in range(4):
                opt = OPTIONS[(i + j) % 4]
                if all((x + dx, y + dy) not in grid for dx, dy in opt):
                    dx, dy = opt[0]
                    proposed[x + dx, y + dy].append((x, y))
                    break
            else:
                new_grid.add((x, y))

        for p, es in proposed.items():
            if len(es) == 1:
                new_grid.add(p)
            else:
                new_grid.update(es)

        if grid == new_grid:
            print("Part 2:", i + 1)
            break

        grid = new_grid

        if i == 9:
            minx = min(x for x, y in grid)
            maxx = max(x for x, y in grid)
            miny = min(y for x, y in grid)
            maxy = max(y for x, y in grid)
            width = maxx - minx + 1
            height = maxy - miny + 1

            print("Part 1:", width * height - len(grid))
