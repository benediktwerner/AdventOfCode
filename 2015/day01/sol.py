#!/usr/bin/env python3

import os


with open(os.path.dirname(__file__) + "/input.txt") as f:
    floor = 0
    first_basement = None

    for i, c in enumerate(f.readline().strip()):
        if c == "(":
            floor += 1
        else:
            floor -= 1
        if floor < 0 and first_basement is None:
            first_basement = i + 1

    print("Part 1:", floor)
    print("Part 2:", first_basement)
