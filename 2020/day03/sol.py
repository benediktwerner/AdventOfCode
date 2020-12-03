#!/usr/bin/env python3

from os import path

PART1_SLOPE = (3, 1)
SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    trees = [line.strip() for line in f]
    width = len(trees[0])

    part2 = 1
    for dx, dy in SLOPES:
        x, y = 0, 0
        count = 0

        while y < len(trees):
            if trees[y][x] == "#":
                count += 1
            x = (x + dx) % width
            y += dy

        if (dx, dy) == PART1_SLOPE:
            print("Part 1:", count)

        part2 *= count

    print("Part 2:", part2)
