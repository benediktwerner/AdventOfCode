#!/usr/bin/env python3

from os import path


def is_safe(levels: list[int]) -> bool:
    increasing = levels[0] < levels[1]
    for a, b in zip(levels, levels[1:]):
        if a == b or abs(a - b) > 3 or (a < b) != increasing:
            return False
    return True


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0
    for line in file.read().splitlines():
        levels = list(map(int, line.split()))
        part1 += is_safe(levels)
        part2 += any(is_safe(levels[:i] + levels[i + 1 :]) for i in range(len(levels)))

    print("Part 1:", part1)
    print("Part 2:", part2)
