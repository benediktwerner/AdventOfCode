#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()

    empty_rows = []
    for y, row in enumerate(grid):
        if all(c == "." for c in row):
            empty_rows.append(y)

    empty_columns = []
    for x in range(len(grid[0])):
        if all(grid[y][x] == "." for y in range(len(grid))):
            empty_columns.append(x)

    galaxies = []
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "#":
                galaxies.append((x, y))

    part1, part2 = 0, 0
    for i, (ax, ay) in enumerate(galaxies):
        for bx, by in galaxies[i + 1 :]:
            part1 += abs(ax - bx) + abs(ay - by)
            part2 += abs(ax - bx) + abs(ay - by)
            for y in empty_rows:
                if ay < y < by or by < y < ay:
                    part1 += 1
                    part2 += 999999
            for x in empty_columns:
                if ax < x < bx or bx < x < ax:
                    part1 += 1
                    part2 += 999999

    print("Part 1:", part1)
    print("Part 2:", part2)
