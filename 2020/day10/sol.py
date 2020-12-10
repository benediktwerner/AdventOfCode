#!/usr/bin/env python3

from os import path
from functools import lru_cache


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    jolts = [int(line) for line in f]
    jolts.sort()
    jolts = [0] + jolts + [jolts[-1] + 3]

    ones = threes = 0

    for a, b in zip(jolts, jolts[1:]):
        if b - a == 1:
            ones += 1
        if b - a == 3:
            threes += 1

    print("Part 1:", ones * threes)


@lru_cache
def arrangements(i):
    if i >= len(jolts):
        return 1

    x = jolts[i]
    result = arrangements(i + 1)

    if i + 2 < len(jolts) and jolts[i + 2] - x <= 3:
        result += arrangements(i + 2)

        if i + 3 < len(jolts) and jolts[i + 3] - x <= 3:
            result += arrangements(i + 3)

    return result


print("Part 2:", arrangements(0))
