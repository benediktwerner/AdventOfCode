#!/usr/bin/env python3

from os import path
import re
from z3 import *


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def Abs(x):
    return If(x >= 0, x, -x)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    impossible_x = set()
    beacons_in_row = set()
    x, y = Ints("x y")
    s = Solver()
    s.add(x >= 0)
    s.add(x <= 4000000)
    s.add(y >= 0)
    s.add(y <= 4000000)
    for line in f.read().splitlines():
        sx, sy, bx, by = ints(line)
        d = abs(sx - bx) + abs(sy - by)
        s.add(Abs(x - sx) + Abs(y - sy) > d)
        extent = d - abs(sy - 2000000)
        for xx in range(sx - extent, sx + extent + 1):
            impossible_x.add(xx)
        if by == 2000000:
            beacons_in_row.add(bx)

    print("Part 1:", len(impossible_x - beacons_in_row))

    assert s.check() == sat, "unsat"
    m = s.model()
    print("Part 2:", m[x].as_long() * 4000000 + m[y].as_long())
