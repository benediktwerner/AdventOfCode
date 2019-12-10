#!/usr/bin/env python3

from os import path


DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    first_wire = [(c[0], int(c[1:])) for c in f.readline().strip().split(",")]
    second_wire = [(c[0], int(c[1:])) for c in f.readline().strip().split(",")]

    first_cords = set()
    first_steps = {}
    x, y, s = 0, 0, 0

    for (d, a) in first_wire:
        xd, yd = DIRS[d]
        for _ in range(a):
            x += xd
            y += yd
            s += 1
            first_steps[(x, y)] = s
            first_cords.add((x, y))

    intersections = set()
    x, y, s = 0, 0, 0

    for (d, a) in second_wire:
        xd, yd = DIRS[d]
        for _ in range(a):
            x += xd
            y += yd
            s += 1
            if (x, y) in first_cords:
                intersections.add((x, y, s + first_steps[(x, y)]))

    min_dist = min(map(lambda x: abs(x[0]) + abs(x[1]), intersections))
    print("Part 1:", min_dist)

    min_steps = min(map(lambda x: x[2], intersections))
    print("Part 2:", min_steps)
