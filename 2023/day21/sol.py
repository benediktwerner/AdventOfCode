#!/usr/bin/env python3

from collections import defaultdict
from os import path


def solve(inp: str):
    grid = inp.splitlines()
    width, height = len(grid[0]), len(grid)
    pos = defaultdict(set)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                pos[x, y].add((0, 0))
    for _ in range(26501365):
        if _ % 1_000 == 0:
            print(_, len(pos))
        new_pos = defaultdict(set)
        for (x, y), areas in pos.items():
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx = (x + dx) % width
                ny = (y + dy) % height
                if grid[ny][nx] != "#":
                    new_pos[nx, ny] = areas
        pos = new_pos
    return len(pos)


example = """\

"""

if example and not example.isspace():
    print("Example:", solve(example))
else:
    print("No example provided")

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    result = solve(file.read())
    print("Output:", result)
