#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    x, y = 0, 0
    xx, yy = [0, 0], [0, 0]
    visited1 = set([(x, y)])
    visited2 = set([(x, y)])
    for i, dir in enumerate(f.read().strip()):
        dx, dy = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}[dir]
        x += dx
        y += dy
        xx[i % 2] += dx
        yy[i % 2] += dy
        visited1.add((x, y))
        visited2.add((xx[i % 2], yy[i % 2]))

    print("Part 1:", len(visited1))
    print("Part 2:", len(visited2))
