#!/usr/bin/env python3

from os import path

OUTSIDE, INSIDE, INSIDE_UP, INSIDE_DOWN = range(4)
MOVEMENT = {
    "-": {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0),
    },
    "|": {
        (0, 1): (0, 1),
        (0, -1): (0, -1),
    },
    "F": {
        (-1, 0): (0, 1),
        (0, -1): (1, 0),
    },
    "7": {
        (1, 0): (0, 1),
        (0, -1): (-1, 0),
    },
    "J": {
        (1, 0): (0, -1),
        (0, 1): (-1, 0),
    },
    "L": {
        (-1, 0): (0, -1),
        (0, 1): (1, 0),
    },
}
PIECE_FROM_CONNECTIONS = {
    ((0, -1), (0, 1)): "|",
    ((-1, 0), (1, 0)): "-",
    ((0, 1), (1, 0)): "F",
    ((-1, 0), (0, 1)): "7",
    ((-1, 0), (0, -1)): "J",
    ((0, -1), (1, 0)): "L",
}


def find_loop(x, y, dx, dy):
    loop = set()
    while True:
        x += dx
        y += dy
        loop.add((x, y))
        match grid[y][x]:
            case ".":
                return None
            case "S":
                return loop
            case c:
                if (dx, dy) not in MOVEMENT[c]:
                    return None
                dx, dy = MOVEMENT[c][dx, dy]


def find_start():
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "S":
                return x, y
    assert False


def part1(x, y):
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        if loop := find_loop(x, y, dx, dy):
            return loop
    assert False


def find_connections(x, y):
    for dx, dy in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        xx, yy = x + dx, y + dy
        if (xx, yy) in loop and (dx, dy) in MOVEMENT[grid[yy][xx]]:
            yield dx, dy


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = list(map(list, file.read().splitlines()))
    x, y = find_start()
    loop = part1(x, y)
    print("Part 1:", len(loop) // 2)

    grid[y][x] = PIECE_FROM_CONNECTIONS[tuple(find_connections(x, y))]

    enclosed_count = 0
    for y, row in enumerate(grid):
        state = OUTSIDE
        for x, c in enumerate(row):
            if (x, y) not in loop:
                enclosed_count += state == INSIDE
            elif c == "|":
                state = {
                    OUTSIDE: INSIDE,
                    INSIDE: OUTSIDE,
                }[state]
            elif c == "-":
                pass
            elif c == "F":
                state = {
                    OUTSIDE: INSIDE_DOWN,
                    INSIDE: INSIDE_UP,
                }[state]
            elif c == "L":
                state = {
                    OUTSIDE: INSIDE_UP,
                    INSIDE: INSIDE_DOWN,
                }[state]
            elif c == "7":
                state = {
                    INSIDE_DOWN: OUTSIDE,
                    INSIDE_UP: INSIDE,
                }[state]
            elif c == "J":
                state = {
                    INSIDE_DOWN: INSIDE,
                    INSIDE_UP: OUTSIDE,
                }[state]
            else:
                assert False

    print("Part 2:", enclosed_count)
