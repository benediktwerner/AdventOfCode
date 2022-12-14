#!/usr/bin/env python3

from os import path
from itertools import count


def simulate(grid):
    max_y = max(y for _, y in grid)
    for i in count():
        x, y = 500, 0
        while True:
            if y == max_y:
                return i
            elif (x, y + 1) not in grid:
                y += 1
            elif (x - 1, y + 1) not in grid:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in grid:
                x += 1
                y += 1
            elif y == 0:
                return i + 1
            else:
                grid.add((x, y))
                break


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = set()
    for line in f.read().splitlines():
        points = [list(map(int, p.split(","))) for p in line.split(" -> ")]
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid.add((x, y))

    print("Part 1:", simulate(grid.copy()))

    max_y = max(y for _, y in grid)
    for x in range(-100000, 100000):
        grid.add((x, max_y + 2))

    print("Part 2:", simulate(grid))
