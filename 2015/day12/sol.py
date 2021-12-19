#!/usr/bin/env python3

from os import path
import json


def nums(j):
    if isinstance(j, int):
        return j
    if isinstance(j, list):
        return sum(map(nums, j))
    if isinstance(j, str):
        return 0
    assert isinstance(j, dict), type(j)
    if p2 and any(v == "red" for v in j.values()):
        return 0
    return sum(map(nums, j.values()))

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = json.load(f)
    p2 = False
    print("Part 1:", nums(inp))
    p2 = True
    print("Part 2:", nums(inp))
