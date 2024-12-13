#!/usr/bin/env python3

import re
from os import path


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(a: list[int], b: list[int], p: list[int]) -> int | None:
    # px = ax * a + bx * b
    # py = ay * a + by * b
    #
    # a = (px - bx * b) / ax
    # py = ay * ((px - bx * b) / ax) + by * b
    # py = ay / ax * (px - bx * b) + by * b
    # py = ay / ax * px - ay / ax * bx * b + by * b
    # py = ay / ax * px - (ay / ax * bx - by) * b
    # b = (ay / ax * px - py) / (ay / ax * bx - by)
    ax, ay = a
    bx, by = b
    px, py = p
    bb = round((ay / ax * px - py) / (ay / ax * bx - by))
    aa = (px - bx * bb) // ax
    if ax * aa + bx * bb == px and ay * aa + by * bb == py:
        return 3 * aa + bb


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    for game in file.read().split("\n\n"):
        a, b, p = map(ints, game.splitlines())
        part1 += solve(a, b, p) or 0
        part2 += solve(a, b, [x + 10_000_000_000_000 for x in p]) or 0

    print("Part 1:", part1)
    print("Part 2:", part2)
