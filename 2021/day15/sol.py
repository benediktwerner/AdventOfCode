#!/usr/bin/env python3

from os import path
import heapq


def solve(grid):
    goalx = max(x for x, _ in grid)
    goaly = max(y for _, y in grid)

    todo = [(0, 0, 0)]
    visited = set()
    while todo:
        r, x, y = heapq.heappop(todo)
        if x == goalx and y == goaly:
            return r
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nc = x + xd, y + yd
            if nc in grid and nc not in visited:
                heapq.heappush(todo, (r + grid[nc], *nc))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = {}
    for y, line in enumerate(f.read().splitlines()):
        for x, r in enumerate(line):
            grid[x, y] = int(r)

    w, h = x + 1, y + 1

    print("Part 1:", solve(grid))

    grid2 = {}
    for (x, y), r in grid.items():
        for dx in range(5):
            for dy in range(5):
                grid2[x + dx * w, y + dy * h] = (r + dx + dy - 1) % 9 + 1

    print("Part 2:", solve(grid2))
