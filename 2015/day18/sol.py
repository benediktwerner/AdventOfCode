#!/usr/bin/env python3

from os import path

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = [list(row) for row in f.read().splitlines()]


def compute(grid, part2=False):
    def neighbors(x, y):
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                xx = x + dx
                yy = y + dy
                if 0 <= xx < 100 and 0 <= yy < 100 and grid[yy][xx] == "#":
                    count += 1
        return count

    for _ in range(100):
        new = []
        for y, row in enumerate(grid):
            new_row = []
            for x, c in enumerate(row):
                if c == "#":
                    new_row.append("#" if neighbors(x, y) in (2, 3) else ".")
                else:
                    new_row.append("#" if neighbors(x, y) == 3 else ".")
            new.append(new_row)
        grid = new
        if part2:
            for x in (0, 99):
                for y in (0, 99):
                    grid[y][x] = "#"
    
    return sum(sum(c == "#" for c in row) for row in grid)


print("Part 1:", compute(grid))

for x in (0, 99):
    for y in (0, 99):
        grid[y][x] = "#"

print("Part 2:", compute(grid, True))
