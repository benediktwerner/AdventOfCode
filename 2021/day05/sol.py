#!/usr/bin/env python3

from os import path
import re
from collections import defaultdict


def ints(string):
    return map(int, re.findall(r"-?[0-9]+", string))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid1 = defaultdict(int)
    grid2 = defaultdict(int)
    for line in f.read().splitlines():
        x1, y1, x2, y2 = ints(line)
        if x1 != x2 and y1 != y2:
            xx = range(x1, x2 + 1) if x2 > x1 else range(x1, x2 - 1, -1)
            yy = range(y1, y2 + 1) if y2 > y1 else range(y1, y2 - 1, -1)
            for x, y in zip(xx, yy):
                grid2[(x, y)] += 1
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid1[(x, y)] += 1
                    grid2[(x, y)] += 1

    print("Part 1:", sum(c > 1 for c in grid1.values()))
    print("Part 2:", sum(c > 1 for c in grid2.values()))
