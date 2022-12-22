#!/usr/bin/env python3

from os import path
import re

# right, down, left, up
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def solve(grid, path, part1):
    my = 0
    mx = min(x for x, y in grid if y == 0)
    d = 0

    for p in path:
        if p == "L":
            d = (d - 1) % 4
            continue
        if p == "R":
            d = (d + 1) % 4
            continue

        for _ in range(int(p)):
            dx, dy = DIRS[d]
            n = nx, ny = mx + dx, my + dy
            nd = d
            if n not in grid:
                if dx < 0:
                    if part1:
                        nx = max(x for x, y in grid if y == my)
                    elif my < 50:
                        nx = 0
                        ny = 149 - my
                        nd = 0
                    elif my < 100:
                        nx = my - 50
                        ny = 100
                        nd = 1
                    elif my < 150:
                        nx = 50
                        ny = 49 - (my - 100)
                        nd = 0
                    else:
                        nx = 50 + my - 150
                        ny = 0
                        nd = 1
                if dx > 0:
                    if part1:
                        nx = min(x for x, y in grid if y == my)
                    elif my < 50:
                        nx = 99
                        ny = 149 - my
                        nd = 2
                    elif my < 100:
                        nx = 100 + my - 50
                        ny = 49
                        nd = 3
                    elif my < 150:
                        nx = 149
                        ny = 49 - (my - 100)
                        nd = 2
                    else:
                        nx = 50 + my - 150
                        ny = 149
                        nd = 3
                if dy < 0:
                    if part1:
                        ny = max(y for x, y in grid if x == mx)
                    elif my == 0:
                        if 50 <= mx < 100:
                            nx = 0
                            ny = 150 + mx - 50
                            nd = 0
                        elif 100 <= mx:
                            nx = mx - 100
                            ny = 199
                        else:
                            assert False
                    else:
                        assert my == 100
                        ny = mx + 50
                        nx = 50
                        nd = 0
                if dy > 0:
                    if part1:
                        ny = min(y for x, y in grid if x == mx)
                    elif my == 199:
                        nx = mx + 100
                        ny = 0
                        nd = 1
                    elif my == 149:
                        nx = 49
                        ny = mx - 50 + 150
                        nd = 2
                    else:
                        assert my == 49
                        nx = 99
                        ny = mx - 100 + 50
                        nd = 2
                n = nx, ny
            if grid[n] == "#":
                break
            mx = nx
            my = ny
            d = nd

    return (my + 1) * 1000 + 4 * (mx + 1) + d


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    path = re.findall(r"(\d+|L|R)", lines[-1])
    grid = {}
    for y, line in enumerate(lines[:-2]):
        for x, c in enumerate(line):
            if c != " ":
                grid[(x, y)] = c

    print("Part 1:", solve(grid, path, True))
    print("Part 2:", solve(grid, path, False))
