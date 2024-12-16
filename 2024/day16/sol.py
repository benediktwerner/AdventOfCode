#!/usr/bin/env python3

from collections import defaultdict
import heapq
from os import path


RIGHT, DOWN, LEFT, UP = range(4)
DIRS = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    width, height = len(grid[0]), len(grid)

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                start = x, y
            elif c == "E":
                end = x, y

    todo = [(0, *start, RIGHT)]
    seen = set()
    origins = defaultdict(list)
    lowest_score = None

    while todo:
        s, x, y, d = heapq.heappop(todo)

        if lowest_score is not None and s > lowest_score:
            break

        if (x, y) == end:
            lowest_score = s
            continue

        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))

        for dd in (1, -1):
            nd = (d + dd) % 4
            heapq.heappush(todo, (s + 1000, x, y, nd))
            origins[(s + 1000, x, y, nd)].append((s, x, y, d))

        dx, dy = DIRS[d]
        nx = x + dx
        ny = y + dy
        if grid[ny][nx] != "#":
            heapq.heappush(todo, (s + 1, nx, ny, d))
            origins[(s + 1, nx, ny, d)].append((s, x, y, d))

    print("Part 1:", lowest_score)

    good = set()
    todo = [(lowest_score, *end, d) for d in DIRS]
    while todo:
        s, x, y, d = todo.pop()
        good.add((x, y))
        for state in origins[(s, x, y, d)]:
            todo.append(state)

    print("Part 2:", len(good))
