#!/usr/bin/env python3

from os import path


RIGHT, DOWN, LEFT, UP = range(4)
DIRS = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}


def solve(grid, x, y, d):
    todo = [(x, y, d)]
    seen = set(todo)
    while todo:
        x, y, d = todo.pop()
        c = grid[y][x]
        if (
            c == "."
            or (c == "-" and d in (RIGHT, LEFT))
            or (c == "|" and d in (UP, DOWN))
        ):
            new = [d]
        elif c == "-":
            new = [RIGHT, LEFT]
        elif c == "|":
            new = [UP, DOWN]
        elif c == "/":
            new = [
                {
                    RIGHT: UP,
                    DOWN: LEFT,
                    LEFT: DOWN,
                    UP: RIGHT,
                }[d]
            ]
        elif c == "\\":
            new = [
                {
                    RIGHT: DOWN,
                    DOWN: RIGHT,
                    LEFT: UP,
                    UP: LEFT,
                }[d]
            ]
        else:
            assert False
        for d in new:
            dx, dy = DIRS[d]
            x, y = x + dx, y + dy
            if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
                continue
            key = (x, y, d)
            if key not in seen:
                seen.add(key)
                todo.append(key)
    return len(set((x, y) for x, y, _ in seen))


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = [list(line) for line in file.read().splitlines()]
    print("Part 1:", solve(grid, 0, 0, RIGHT))

    width = len(grid[0])
    height = len(grid)
    best = 0
    for x in range(width):
        best = max(best, solve(grid, x, 0, DOWN))
        best = max(best, solve(grid, x, height - 1, UP))
    for y in range(height):
        best = max(best, solve(grid, 0, y, RIGHT))
        best = max(best, solve(grid, width - 1, y, LEFT))
    print("Part 2:", best)
