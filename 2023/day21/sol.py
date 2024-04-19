#!/usr/bin/env python3

from collections import deque
from os import path

# Part 2 based on https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    width, height = len(grid[0]), len(grid)
    todo = deque([])
    visited = set()
    part1 = 1
    even_corners = 0
    odd_corners = 0
    even_full = 1
    odd_full = 0

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                todo.append((x, y, 0))
                visited.add((x, y))

    while todo:
        x, y, d = todo.popleft()
        d += 1
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if (
                (nx, ny) in visited
                or nx < 0
                or ny < 0
                or nx >= width
                or ny >= height
                or grid[ny][nx] != "."
            ):
                continue
            visited.add((nx, ny))
            todo.append((nx, ny, d))

            if d <= 64 and d % 2 == 0:
                part1 += 1

            if d % 2 == 0:
                even_full += 1
                if abs(nx - 65) + abs(ny - 65) > 65:
                    even_corners += 1
            else:
                odd_full += 1
                if abs(nx - 65) + abs(ny - 65) > 65:
                    odd_corners += 1

    n = 202300

    print("Part 1:", part1)
    print(
        "Part 2:",
        ((n + 1) * (n + 1)) * odd_full
        + (n * n) * even_full
        - (n + 1) * odd_corners
        + n * even_corners,
    )
