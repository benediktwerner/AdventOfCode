#!/usr/bin/env python3

import os


with open(os.path.dirname(__file__) + "/input.txt") as f:
    total1 = 0
    total2 = 0

    for line in f:
        line = line.strip()

        fuel = int(line) // 3 - 2
        total1 += fuel

        while fuel > 0:
            total2 += fuel
            fuel = fuel // 3 - 2

    print("Part 1:", total1)
    print("Part 2:", total2)
