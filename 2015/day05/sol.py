#!/usr/bin/env python3

from os import path
import re


def nice1(s):
    for p in ("ab", "cd", "pq", "xy"):
        if p in s:
            return False
    if not re.findall(r"(.)\1", s):
        return False
    return len(re.findall("[aeiou]", s)) >= 3


def nice2(s):
    if not re.findall(r"(.).\1", s):
        return False
    if not re.findall(r"(.)(.).*\1\2", s):
        return False
    return True


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    print("Part 1:", sum(map(nice1, lines)))
    print("Part 2:", sum(map(nice2, lines)))
