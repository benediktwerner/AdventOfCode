#!/usr/bin/env python3

from os import path


def move_horizontal(grid, dx):
    start_x = 0 if dx < 0 else len(grid[0]) - 1
    end_x = len(grid[0]) if dx < 0 else -1
    for y in range(len(grid)):
        last_free = start_x
        for x in range(start_x, end_x, -dx):
            if grid[y][x] == "#":
                last_free = x - dx
            elif grid[y][x] == "O":
                grid[y][x] = "."
                grid[y][last_free] = "O"
                last_free -= dx


def move_vertical(grid, dy):
    start_y = 0 if dy < 0 else len(grid) - 1
    end_y = len(grid) if dy < 0 else -1
    for x in range(len(grid[0])):
        last_free = start_y
        for y in range(start_y, end_y, -dy):
            if grid[y][x] == "#":
                last_free = y - dy
            elif grid[y][x] == "O":
                grid[y][x] = "."
                grid[last_free][x] = "O"
                last_free -= dy


def load(grid):
    return sum(load * line.count("O") for load, line in enumerate(reversed(grid), 1))


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = list(map(list, file.read().splitlines()))
    move_vertical(grid, -1)
    print("Part 1:", load(grid))

    move_horizontal(grid, -1)
    move_vertical(grid, 1)
    move_horizontal(grid, 1)

    seen = {}
    i = 1
    looped = False
    while i < 1000000000:
        if not looped:
            key = tuple(tuple(line) for line in grid)
            if key in seen:
                cycle = i - seen[key]
                i += cycle * ((1000000000 - i) // cycle)
                looped = True
            else:
                seen[key] = i
        move_vertical(grid, -1)
        move_horizontal(grid, -1)
        move_vertical(grid, 1)
        move_horizontal(grid, 1)
        i += 1

    print("Part 2:", load(grid))
