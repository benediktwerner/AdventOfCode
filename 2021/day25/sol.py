#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = []
    for line in f.read().splitlines():
        grid.append(list(line))

    changed = True
    steps = 0

    while changed:
        steps += 1
        new = [["." for _ in row] for row in grid]
        changed = False
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == ">" and row[(x + 1) % len(row)] == ".":
                    new[y][(x + 1) % len(row)] = ">"
                    changed = True
                elif c != ".":
                    new[y][x] = c
        grid = new
        new = [["." for _ in row] for row in grid]
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "v" and grid[(y + 1) % len(grid)][x] == ".":
                    new[(y + 1) % len(grid)][x] = "v"
                    changed = True
                elif c != ".":
                    new[y][x] = c
        grid = new

    print("Part 1:", steps)
