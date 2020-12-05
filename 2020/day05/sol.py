#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    ids = set()

    for line in f:
        row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
        col = int(line[7:].replace("L", "0").replace("R", "1"), 2)
        ids.add(row * 8 + col)

    print("Part 1:", max(ids))

    for i in range(1, 0b1_0000000_000):
        if i not in ids and i - 1 in ids and i + 1 in ids:
            print("Part 2:", i)
            break
