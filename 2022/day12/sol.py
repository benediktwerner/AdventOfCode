#!/usr/bin/env python3

from os import path
from collections import deque


def shortest_path(grid, start, target):
    visited = set([start])
    todo = deque([(start, 0)])
    while todo:
        (cx, cy), d = todo.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < len(grid[0])
                and 0 <= ny < len(grid)
                and (nx, ny) not in visited
                and grid[ny][nx] <= grid[cy][cx] + 1
            ):
                if (nx, ny) == target:
                    return d + 1
                todo.append(((nx, ny), d + 1))
                visited.add((nx, ny))
    return float("inf")


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = [list(line) for line in f.read().splitlines()]
    starts = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                starts.append((x, y))
                start = (x, y)
                grid[y][x] = ord("a")
            elif c == "E":
                target = (x, y)
                grid[y][x] = ord("z")
            else:
                if c == "a":
                    starts.append((x, y))
                grid[y][x] = ord(c)

    print("Part 1:", shortest_path(grid, start, target))
    print("Part 2:", min([shortest_path(grid, s, target) for s in starts]))
