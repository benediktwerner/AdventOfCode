#!/usr/bin/env python3

from os import path
import math
from z3 import Optimize, Int, If, sat


def solve(parts):
    part = sum(nums) // parts
    opt = Optimize()
    vars = [(Int(str(x)), x) for x in nums]

    for v, _ in vars:
        opt.add(v >= 0)
        opt.add(v < parts)

    for i in range(parts - 1):
        opt.add(sum(If(v == i, n, 0) for v, n in vars) == part)

    count = sum(If(v == 0, 1, 0) for v, _ in vars)
    quantum = math.prod(If(v == 0, n, 1) for v, n in vars)

    opt.minimize(count)
    opt.minimize(quantum)

    assert opt.check() == sat
    return opt.model().eval(quantum).as_long()


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    nums = list(map(int, f.read().splitlines()))


print("Part 1:", solve(3))
print("Part 2:", solve(4))
