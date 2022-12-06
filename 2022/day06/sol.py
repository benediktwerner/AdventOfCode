#!/usr/bin/env python3

from os import path


def solve(inp, count):
    for i in range(count, len(inp)):
        if len(set(inp[i - count : i])) == count:
            return i


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.read()
    print("Part 1:", solve(inp, 4))
    print("Part 2:", solve(inp, 14))
