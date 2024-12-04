#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    width, height = len(grid[0]), len(grid)

    part1 = 0
    for dx, dy in ((0, 1), (1, 0), (1, 1), (1, -1)):
        for x in range(width):
            for y in range(height):
                if x + 3 * dx not in range(width) or y + 3 * dy not in range(height):
                    continue
                if all(grid[y + i * dy][x + i * dx] == c for i, c in enumerate("XMAS")):
                    part1 += 1
                if all(grid[y + i * dy][x + i * dx] == c for i, c in enumerate("SAMX")):
                    part1 += 1
    print("Part 1:", part1)

    part2 = 0
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if (
                grid[y][x] == "A"
                and grid[y - 1][x - 1] in "MS"
                and grid[y + 1][x + 1] in "MS"
                and grid[y - 1][x - 1] != grid[y + 1][x + 1]
                and grid[y - 1][x + 1] in "MS"
                and grid[y + 1][x - 1] in "MS"
                and grid[y - 1][x + 1] != grid[y + 1][x - 1]
            ):
                part2 += 1
    print("Part 2:", part2)
