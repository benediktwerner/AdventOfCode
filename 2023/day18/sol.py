#!/usr/bin/env python3

from os import path


DIRS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def solve(instructions):
    edges = []
    x, y = 0, 0
    for d, length in instructions:
        dx, dy = DIRS[d]
        x = x + dx * length
        y = y + dy * length
        edges.append((x, y))

    # https://en.wikipedia.org/wiki/Shoelace_formula
    # https://de.wikipedia.org/wiki/Gau%C3%9Fsche_Trapezformel
    area, circumference = 0, 2
    for i in range(len(edges)):
        area += edges[i][0] * (edges[(i + 1) % len(edges)][1] - edges[i - 1][1])
        circumference += abs(edges[i][0] - edges[i - 1][0])
        circumference += abs(edges[i][1] - edges[i - 1][1])
    return (area + circumference) // 2


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1, part2 = [], []
    for line in file.read().splitlines():
        d, length, hx = line.split()
        part1.append((d, int(length)))
        hx = hx[2:-1]
        part2.append(("RDLU"[int(hx[-1])], int(hx[:-1], 16)))
    print("Part 1:", solve(part1))
    print("Part 2:", solve(part2))
