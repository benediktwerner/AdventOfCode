#!/usr/bin/env python3

from os import path


DIRECTIONS = {d: i for i, d in enumerate(["N", "E", "S", "W"])}
MOVE = [(0, -1), (1, 0), (0, 1), (-1, 0)]
ROTX = [(1, 0), (0, -1), (-1, 0), (0, 1)]
ROTY = [(0, 1), (1, 0), (0, -1), (-1, 0)]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    x, y, x2, y2, d = 0, 0, 0, 0, DIRECTIONS["E"]
    wpx, wpy = 10, -1

    for line in f:
        op, arg = line[0], int(line[1:])

        # Part 1
        if op == "R":
            d = (d + arg // 90) % 4
        elif op == "L":
            d = (d - arg // 90) % 4
        else:
            dx, dy = MOVE[DIRECTIONS.get(op, d)]
            x += dx * arg
            y += dy * arg

        # Part 2
        if op in DIRECTIONS:
            dx, dy = MOVE[DIRECTIONS[op]]
            wpx += dx * arg
            wpy += dy * arg
        elif op == "F":
            x2 += wpx * arg
            y2 += wpy * arg
        else:
            rot = arg // 90 if op == "R" else ((-arg) % 360) // 90
            rotx, roty = ROTX[rot], ROTY[rot]
            wpx, wpy = wpx * rotx[0] + wpy * rotx[1], wpx * roty[0] + wpy * roty[1]

    print("Part 1:", abs(x) + abs(y))
    print("Part 2:", abs(x2) + abs(y2))
