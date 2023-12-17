#!/usr/bin/env python3

from os import path
from queue import PriorityQueue

RIGHT, DOWN, LEFT, UP = range(4)
DIRS = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}


def solve(grid, min_straight: int, max_straight: int):
    width, height = len(grid[0]), len(grid)
    todo = PriorityQueue()
    todo.put((grid[0][1], 1, 0, RIGHT, 1))
    todo.put((grid[1][0], 0, 1, DOWN, 1))
    seen = set()
    while todo:
        heat, x, y, d, steps = todo.get()
        if x == width - 1 and y == height - 1 and steps >= min_straight:
            return heat
        if (x, y, d, steps) in seen:
            continue
        seen.add((x, y, d, steps))
        for dd in (-1, 0, 1):
            if (dd == 0 and steps == max_straight) or (
                dd != 0 and steps < min_straight
            ):
                continue
            nd = (d + dd) % 4
            nx, ny = x + DIRS[nd][0], y + DIRS[nd][1]
            new_steps = steps + 1 if d == nd else 1
            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny, nd, new_steps) not in seen
            ):
                todo.put((heat + grid[ny][nx], nx, ny, nd, new_steps))
    assert False


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = [list(map(int, line)) for line in file.read().splitlines()]
    print("Part 1:", solve(grid, min_straight=0, max_straight=3))
    print("Part 2:", solve(grid, min_straight=4, max_straight=10))
