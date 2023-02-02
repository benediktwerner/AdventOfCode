#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1, part2 = 0, 0
    for line in f.read().splitlines():
        (a1, a2), (b1, b2) = map(lambda e: map(int, e.split("-")), line.split(","))
        if a1 <= b1 and b2 <= a2 or b1 <= a1 and a2 <= b2:
            part1 += 1
        if a1 <= b1 <= a2 or b1 <= a1 <= b2:
            part2 += 1

    print("Part 1:", part1)
    print("Part 2:", part2)
