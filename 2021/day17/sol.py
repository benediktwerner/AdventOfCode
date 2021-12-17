#!/usr/bin/env python3

from os import path
from collections import defaultdict
import itertools
import re


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    x1, x2, y1, y2 = ints(f.read().strip())
    yd_max = -y1 - 1
    print("Part 1:", yd_max * (yd_max + 1) // 2)

    yds = defaultdict(list)
    for init in range(y1, -y1):
        y, yd = 0, init
        for i in itertools.count(1):
            y += yd
            yd -= 1
            if y1 <= y <= y2:
                yds[init].append(i)
            elif y < y1:
                break

    xds = defaultdict(set)
    for init in range(1, x2 + 1):
        x, xd = 0, init
        for i in itertools.count(1):
            x += xd
            if xd > 0:
                xd -= 1
            if xd == 0:
                if x1 <= x <= x2:
                    xds[init] = min(xds[init], default=i)
                break
            if x1 <= x <= x2:
                xds[init].add(i)
            elif x > x2:
                break

    count = 0
    for yd_is in yds.values():
        for xd_is in xds.values():
            if isinstance(xd_is, int):
                if any(i >= xd_is for i in yd_is):
                    count += 1
            elif any(i in xd_is for i in yd_is):
                count += 1

    print("Part 2:", count)
