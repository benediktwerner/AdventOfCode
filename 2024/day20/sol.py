#!/usr/bin/env python3

from collections import deque
from os import path


def distances_from(x, y):
    todo = deque([(0, x, y)])
    distances = {(x, y): 0}
    while todo:
        d, x, y = todo.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if (
                nx not in range(width)
                or ny not in range(height)
                or (nx, ny) in distances
                or grid[ny][nx] == "#"
            ):
                continue
            distances[nx, ny] = d + 1
            todo.append((d + 1, nx, ny))
    return distances


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    width, height = len(grid[0]), len(grid)

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "E":
                end = x, y
            elif c == "S":
                start = x, y

    dists_from_start = distances_from(*start)
    dists_from_end = distances_from(*end)
    target_to_beat = dists_from_end[start] - 100

    part1 = part2 = 0

    for (sx, sy), sd in dists_from_start.items():
        for (ex, ey), ed in dists_from_end.items():
            cheat_length = abs(sx - ex) + abs(sy - ey)
            if cheat_length <= 20 and sd + cheat_length + ed <= target_to_beat:
                part2 += 1
                part1 += cheat_length <= 2

    print("Part 1:", part1)
    print("Part 2:", part2)
