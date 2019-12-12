#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import re


def calc(a, b):
    x1, y1, z1, *_ = a
    x2, y2, z2, *_ = b
    if x1 > x2:
        vx1 = -1
        vx2 = 1
    elif x1 < x2:
        vx1 = 1
        vx2 = -1
    else:
        vx1 = 0
        vx2 = 0
    if y1 > y2:
        vy1 = -1
        vy2 = 1
    elif y1 < y2:
        vy1 = 1
        vy2 = -1
    else:
        vy1 = 0
        vy2 = 0
    if z1 > z2:
        vz1 = -1
        vz2 = 1
    elif z1 < z2:
        vz1 = 1
        vz2 = -1
    else:
        vz1 = 0
        vz2 = 0
    return vx1, vy1, vz1, vx2, vy2, vz2


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    moons = []

    for line in f:
        m = list(map(int, re.findall(r"(-?\d+)", line.strip())))
        m += [0, 0, 0]
        moons.append(m)

    for _ in range(1000):
        for i, m1 in enumerate(moons):
            for j, m2 in enumerate(moons[i + 1 :], i+1):
                a, b, c, d, e, f = calc(m1, m2)
                moons[i][3] += a
                moons[i][4] += b
                moons[i][5] += c
                moons[j][3] += d
                moons[j][4] += e
                moons[j][5] += f
        for m in moons:
            m[0] += m[3]
            m[1] += m[4]
            m[2] += m[5]
    total = 0
    for m in moons:
        a = abs(m[0]) + abs(m[1]) + abs(m[2])
        b = abs(m[3]) + abs(m[4]) + abs(m[5])
        total += a * b
    print(total)
