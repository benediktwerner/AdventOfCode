#!/usr/bin/env python3

from collections import deque
from os import path


WIDTH = HEIGHT = 71


def solve(grid: list[list[bool]]) -> int | None:
    todo = deque([(0, 0, 0)])
    seen = set()
    while todo:
        x, y, d = todo.popleft()
        if x == WIDTH - 1 and y == HEIGHT - 1:
            return d
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if nx in range(WIDTH) and ny in range(HEIGHT) and not grid[nx][ny]:
                todo.append((nx, ny, d + 1))

    return None


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for i, line in enumerate(file.read().splitlines()):
        x, y = map(int, line.split(","))
        grid[y][x] = True

        if i == 1023:
            print("Part 1:", solve(grid))
        elif i > 1023 and solve(grid) is None:
            print("Part 2:", line)
            break
