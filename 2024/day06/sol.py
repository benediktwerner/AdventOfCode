#!/usr/bin/env python3

from os import path


RIGHT, DOWN, LEFT, UP = range(4)
DIRS = {RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0), UP: (0, -1)}


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "^":
                return x, y
    assert False, "no guard (^) in grid"


def simulate(grid: list[list[str]], x: int, y: int) -> set[tuple[int, int]] | None:
    width, height = len(grid[0]), len(grid)
    dir = UP
    visited = set([(x, y, dir)])
    while True:
        dx, dy = DIRS[dir]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height):
            return {(x, y) for x, y, _ in visited}
        if grid[ny][nx] == "#":
            dir = (dir + 1) % 4
        else:
            x, y = nx, ny
            if (x, y, dir) in visited:
                return None
            visited.add((x, y, dir))


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = list(map(list, file.read().splitlines()))
    x, y = find_start(grid)
    visited = simulate(grid, x, y)

    assert visited is not None
    print("Part 1:", len(visited))

    part2 = 0
    for bx, by in visited:
        if grid[by][bx] == "^":
            continue
        grid[by][bx] = "#"
        if simulate(grid, x, y) is None:
            part2 += 1
        grid[by][bx] = "."
    print("Part 2:", part2)
