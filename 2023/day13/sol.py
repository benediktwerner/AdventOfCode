#!/usr/bin/env python3

from os import path


def is_horizontally_symmetric(grid, y, smudges):
    for i in range(min(y + 1, len(grid) - y - 1)):
        for x in range(len(grid[y])):
            if grid[y - i][x] != grid[y + 1 + i][x]:
                if smudges > 0:
                    smudges -= 1
                else:
                    return False
    return smudges == 0


def is_vertically_symmetric(grid, x, smudges):
    for i in range(min(x + 1, len(grid[0]) - x - 1)):
        for y in range(len(grid)):
            if grid[y][x - i] != grid[y][x + 1 + i]:
                if smudges > 0:
                    smudges -= 1
                else:
                    return False
    return smudges == 0


def solve(grids, smudges):
    result = 0
    for grid in grids:
        for y in range(len(grid) - 1):
            if is_horizontally_symmetric(grid, y, smudges):
                result += (y + 1) * 100
                break
        else:
            for x in range(len(grid[0]) - 1):
                if is_vertically_symmetric(grid, x, smudges):
                    result += x + 1
                    break
    return result


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grids = [grid.splitlines() for grid in file.read().split("\n\n")]
    print("Part 1:", solve(grids, 0))
    print("Part 2:", solve(grids, 1))
