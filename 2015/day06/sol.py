#!/usr/bin/env python3

from os import path
from collections import defaultdict


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lights1 = defaultdict(bool)
    lights2 = defaultdict(int)

    for instr in map(str.split, f.read().splitlines()):
        toggle = instr[0] == "toggle"
        x1, y1 = map(int, instr[2 - toggle].split(","))
        x2, y2 = map(int, instr[4 - toggle].split(","))
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if toggle:
                    lights1[x, y] = not lights1[x, y]
                else:
                    lights1[x, y] = instr[1] == "on"
                d = 2 if toggle else (-1, 1)[instr[1] == "on"]
                lights2[x, y] = max(0, lights2[x, y] + d)

    print("Part 1:", sum(lights1.values()))
    print("Part 2:", sum(lights2.values()))
