#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    instrs = f.read().splitlines()
    a = int(instrs[1].split()[1])
    b = int(instrs[2].split()[1])
    curr = a * b
    curr_b = f"{curr:b}"
    target = int("10" * (len(curr_b) // 2), 2)
    print("Part 1:", target - curr)
