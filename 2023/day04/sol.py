#!/usr/bin/env python3

from os import path
import re


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    part1 = 0
    count = [1] * len(lines)
    for i, line in enumerate(lines):
        win, my = map(ints, line.split(": ")[1].split(" | "))
        win = set(win)
        c = sum(x in win for x in my)
        if c > 0:
            part1 += 2 ** (c - 1)
        for j in range(c):
            count[i + j + 1] += count[i]
    print("Part 1:", part1)
    print("Part 2:", sum(count))
