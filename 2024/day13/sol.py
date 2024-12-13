#!/usr/bin/env python3

import re
from os import path
from z3 import Optimize, Int, sat


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(a: list[int], b: list[int], p: list[int]) -> int | None:
    a_count, b_count = Int("a"), Int("b")
    opt = Optimize()
    for aa, bb, pp in zip(a, b, p):
        opt.add(pp == aa * a_count + bb * b_count)
    opt.minimize(a_count * 3 + b_count)
    if opt.check() == sat:
        m = opt.model()
        return m[a_count].as_long() * 3 + m[b_count].as_long()


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    for game in file.read().split("\n\n"):
        a, b, p = map(ints, game.splitlines())
        part1 += solve(a, b, p) or 0
        part2 += solve(a, b, [x + 10_000_000_000_000 for x in p]) or 0

    print("Part 1:", part1)
    print("Part 2:", part2)
