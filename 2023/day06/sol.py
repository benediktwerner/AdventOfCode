#!/usr/bin/env python3

from os import path
import math
import re


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp: str):
    result = 1
    times, dists = map(ints, inp.splitlines())
    for t, d in zip(times, dists):
        # brute-force solution
        # result *= sum((t - hold_t) * hold_t > d for hold_t in range(t))

        # mathematical solution. calculate the roots of the quadratic equation. the solution is the range they span.
        # d == (t - hold_t) * hold_t
        # 0 == (t - hold_t) * hold_t - d
        # 0 == t * hold_t - hold_t^2 - d
        # 0 == -hold_t^2 + t * hold_t - d
        # hold_t = (-t +- sqrt(t^2 - 4 * (-1) * (-d))) / -2
        sqrt = math.sqrt(t * t - 4 * d)
        a = (-t - sqrt) / -2
        b = (-t + sqrt) / -2
        a, b = math.floor(min(a, b) + 1), math.ceil(max(a, b) - 1)
        result *= b - a + 1

    return result


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    input = f.read()
    print("Part 1:", solve(input))
    print("Part 2:", solve(input.replace(" ", "")))
