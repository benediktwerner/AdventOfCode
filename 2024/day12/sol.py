#!/usr/bin/env python3

import itertools
from os import path


def find_area_and_fences(x, y):
    area_id = grid[y][x]
    todo = [(x, y)]
    seen.add((x, y))
    fences = set()
    area = 1

    while todo:
        x, y = todo.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == area_id:
                if (nx, ny) not in seen:
                    area += 1
                    todo.append((nx, ny))
                    seen.add((nx, ny))
            else:
                fences.add((x, y, dx, dy))

    return area, fences


def compute_sides(fences: set[tuple[int, int, int, int]]) -> int:
    sides = 0
    while fences:
        x, y, dx, dy = fences.pop()
        sides += 1
        for d in (1, -1):
            for i in itertools.count(d, d):
                f = (x + i * dy, y + i * dx, dx, dy)
                if f in fences:
                    fences.remove(f)
                else:
                    break
    return sides


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    width, height = len(grid[0]), len(grid)
    part1 = part2 = 0
    seen = set()

    for x in range(width):
        for y in range(height):
            if (x, y) not in seen:
                area, fences = find_area_and_fences(x, y)
                part1 += area * len(fences)
                part2 += area * compute_sides(fences)

    print("Part 1:", part1)
    print("Part 2:", part2)
