#!/usr/bin/env python3

from os import path
from collections import *
import itertools
import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    g = []
    for line in f:
        g.append(tuple(c == "#" for c in line.strip()))


seen = set()
curr = tuple(g)

while True:
    if curr in seen:
        break

    seen.add(curr)

    nxt = []
    for y in range(5):
        row = []
        for x in range(5):
            adj = (
                (x > 0 and curr[y][x - 1])
                + (y > 0 and curr[y - 1][x])
                + (x < 4 and curr[y][x + 1])
                + (y < 4 and curr[y + 1][x])
            )
            if curr[y][x]:
                row.append(adj == 1)
            else:
                row.append(adj == 1 or adj == 2)

        nxt.append(tuple(row))

    curr = tuple(nxt)


print("Part 1:", sum(curr[y][x] * 2 ** (y * 5 + x) for y in range(5) for x in range(5)))


curr = {0: g}
minlvl = -1
maxlvl = 1


def get(lvl, x, y, xd=0, yd=0):
    x += xd
    y += yd

    if x < 0:
        return get(lvl - 1, 1, 2)
    elif y < 0:
        return get(lvl - 1, 2, 1)
    elif x > 4:
        return get(lvl - 1, 3, 2)
    elif y > 4:
        return get(lvl - 1, 2, 3)

    if x == 2 and y == 2:
        if xd == 1:
            return sum(get(lvl + 1, 0, y) for y in range(5))
        elif xd == -1:
            return sum(get(lvl + 1, 4, y) for y in range(5))
        elif yd == 1:
            return sum(get(lvl + 1, x, 0) for x in range(5))
        else:
            return sum(get(lvl + 1, x, 4) for x in range(5))

    if lvl not in curr:
        return 0

    return curr[lvl][y][x]


for _ in range(200):
    nxt = {}

    for i in range(minlvl, maxlvl + 1):
        lvl = []
        for y in range(5):
            row = []
            for x in range(5):
                if x == 2 and y == 2:
                    row.append(False)
                    continue
                adj = sum(
                    get(i, x, y, xd, yd)
                    for xd, yd in ((1, 0), (-1, 0), (0, 1), (0, -1))
                )
                if i in curr and curr[i][y][x]:
                    row.append(adj == 1)
                else:
                    row.append(adj == 1 or adj == 2)
            lvl.append(row)
        nxt[i] = lvl

    curr = nxt

    if any(
        curr[minlvl][x][y]
        for x, y in (
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 4),
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
        )
    ):
        minlvl -= 1

    if any(curr[maxlvl][x][y] for x, y in ((1, 2), (2, 1), (2, 3), (3, 2))):
        maxlvl += 1

print(
    "Part 2:",
    sum(lvl[x][y] for lvl in curr.values() for x in range(5) for y in range(5)),
)
