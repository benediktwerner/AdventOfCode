#!/usr/bin/env python3

from os import path


def sliding_window(coll, n):
    for i in range(len(coll) - n + 1):
        yield coll[i : i + n]


def solve(depths, n):
    windows = list(map(sum, sliding_window(depths, n)))
    return sum(b > a for a, b in zip(windows, windows[1:]))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    depths = [int(x) for x in f.read().splitlines()]
    print("Part 1:", solve(depths, 1))
    print("Part 2:", solve(depths, 3))
