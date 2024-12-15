#!/usr/bin/env python3

from copy import deepcopy
from os import path


RIGHT, DOWN, LEFT, UP = range(4)
DIRS = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "@":
                return x, y
    assert False, "no robot in grid"


def compute_gps_sum(grid: list[list[str]]) -> int:
    result = 0
    for y, line in enumerate(grid):
        for x, m in enumerate(line):
            if m in "O[":
                result += 100 * y + x
    return result


def part1(grid: list[list[str]], moves: list[int], x: int, y: int) -> int:
    for m in moves:
        dx, dy = DIRS[m]
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == ".":
            x, y = nx, ny
            continue
        while grid[ny][nx] not in "#.":
            nx += dx
            ny += dy
        if grid[ny][nx] == "#":
            continue
        grid[ny][nx] = "O"
        x += dx
        y += dy
        grid[y][x] = "."

    return compute_gps_sum(grid)


def part2(grid: list[list[str]], moves: list[int], x: int, y: int) -> int:
    for m in moves:
        dx, dy = DIRS[m]
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == ".":
            x, y = nx, ny
            continue
        if dy == 0:
            while grid[y][nx] not in "#.":
                nx += dx
            if grid[y][nx] == "#":
                continue
            for nx in range(nx, x + dx, -dx):
                grid[y][nx] = grid[y][nx - dx]
            x += dx
            grid[y][x] = "."
        else:
            ny = y
            xs = [x]
            boxes = []
            while not any(grid[ny + dy][nx] == "#" for nx in xs) and not all(
                grid[ny + dy][nx] == "." for nx in xs
            ):
                ny += dy
                new_xs = set()
                for nx in xs:
                    if grid[ny][nx] == "[":
                        new_xs.add(nx)
                        new_xs.add(nx + 1)
                        boxes.append((nx, ny, "["))
                        boxes.append((nx + 1, ny, "]"))
                    elif grid[ny][nx] == "]":
                        new_xs.add(nx - 1)
                        new_xs.add(nx)
                        boxes.append((nx - 1, ny, "["))
                        boxes.append((nx, ny, "]"))
                xs = new_xs

            if any(grid[ny + dy][nx] == "#" for nx in xs):
                continue

            for bx, by, _ in boxes:
                grid[by][bx] = "."
            for bx, by, c in boxes:
                grid[by + dy][bx] = c

            y += dy

    return compute_gps_sum(grid)


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid, moves = file.read().split("\n\n")
    grid = list(map(list, grid.splitlines()))
    moves = [">v<^".index(m) for m in moves.replace("\n", "")]
    x, y = find_start(grid)
    grid[y][x] = "."

    wide_grid = []
    for line in grid:
        row = []
        for c in line:
            if c == "O":
                row.append("[")
                row.append("]")
            else:
                row.append(c)
                row.append(c)
        wide_grid.append(row)

    print("Part 1:", part1(grid, moves, x, y))
    print("Part 2:", part2(wide_grid, moves, 2 * x, y))
