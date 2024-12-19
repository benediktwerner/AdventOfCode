#!/usr/bin/env python3

from functools import cache
from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    towels, designs = file.read().split("\n\n")
    towels = towels.split(", ")

    @cache
    def ways_to_make(d: str) -> int:
        count = 0
        for t in towels:
            if d.startswith(t):
                if len(d) == len(t):
                    count += 1
                else:
                    count += ways_to_make(d[len(t) :])
        return count

    part1 = part2 = 0

    for d in designs.splitlines():
        ways = ways_to_make(d)
        part1 += ways > 0
        part2 += ways

    print("Part 1:", part1)
    print("Part 2:", part2)
