#!/usr/bin/env python3

from os import path


def solve(inp, count):
    last = []
    for i, c in enumerate(inp):
        last.append(c)
        if len(last) > count:
            last.pop(0)
        if len(set(last)) == count:
            return i + 1


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.read()
    print("Part 1:", solve(inp, 4))
    print("Part 2:", solve(inp, 14))
