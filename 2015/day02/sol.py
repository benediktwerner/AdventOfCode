#!/usr/bin/env python3

from os import path
import re


def ints(string):
    return map(int, re.findall(r"-?[0-9]+", string))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    p1, p2 = 0, 0
    for l, w, h in map(ints, f.read().splitlines()):
        sides = (l * w, w * h, h * l)
        p1 += 2 * sum(sides) + min(sides)
        p2 += 2 * min(l + w, w + h, h + l) + l * w * h

    print("Part 1:", p1)
    print("Part 2:", p2)
