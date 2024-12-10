#!/usr/bin/env python3

from os import path
from collections import defaultdict


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = [list(map(int, line)) for line in file.read().splitlines()]
    width, height = len(grid[0]), len(grid)
    starts = [(x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == 0]

    part1 = part2 = 0

    for x, y in starts:
        pos = {(x, y): 1}
        for h in range(9):
            new_pos = defaultdict(int)
            for (x, y), c in pos.items():
                for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == h + 1:
                        new_pos[(nx, ny)] += c
            pos = new_pos

        part1 += len(pos)
        part2 += sum(pos.values())

    print("Part 1:", part1)
    print("Part 2:", part2)
