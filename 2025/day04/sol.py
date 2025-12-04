#!/usr/bin/env python3

from os import path

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))


def removable(x: int, y: int) -> bool:
    if grid[y][x] != "@":
        return False

    count = 0

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == "@":
            count += 1

    return count < 4


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = list(map(list, file.read().splitlines()))
    width, height = len(grid[0]), len(grid)

    print("Part 1:", sum(removable(x, y) for x in range(width) for y in range(height)))

    part2 = 0
    changed = True

    while changed:
        changed = False
        for x in range(height):
            for y in range(width):
                if removable(x, y):
                    grid[y][x] = "."
                    changed = True
                    part2 += 1

    print("Part 2:", part2)
