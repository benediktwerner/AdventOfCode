#!/usr/bin/env python3

from os import path
import re
import pyperclip


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp: str):
    result = 1
    times, dists = map(ints, inp.splitlines())
    for t, d in zip(times, dists):
        result *= sum((t - hold_t) * hold_t > d for hold_t in range(t))
    return result


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    input = f.read()
    print("Part 1:", solve(input))
    print("Part 2:", solve(input.replace(" ", "")))
