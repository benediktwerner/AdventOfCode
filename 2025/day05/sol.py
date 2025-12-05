#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    ranges, ingredients = file.read().split("\n\n")
    ranges = [list(map(int, r.split("-"))) for r in ranges.splitlines()]

    for i in map(int, ingredients.splitlines()):
        for a, b in ranges:
            if a <= i <= b:
                part1 += 1
                break

    print("Part 1:", part1)

    ranges.sort()
    end = ranges[0][0] - 1

    for a, b in sorted(ranges):
        if b > end:
            part2 += b - max(a - 1, end)
            end = b

    print("Part 2:", part2)
