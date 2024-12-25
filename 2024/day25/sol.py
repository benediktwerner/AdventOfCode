#!/usr/bin/env python3

import re
from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    locks = []
    keys = []

    for schematic in file.read().split("\n\n"):
        lines = schematic.splitlines()
        height = len(lines)
        heights = []
        if all(c == "#" for c in lines[0]):
            for x in range(len(lines[0])):
                for y in range(height):
                    if lines[y][x] == ".":
                        heights.append(y)
                        break
            locks.append(heights)
        else:
            for x in range(len(lines[0])):
                for y in range(height):
                    if lines[-y - 1][x] == ".":
                        heights.append(y)
                        break
            keys.append(heights)

    result = 0

    for key in keys:
        for lock in locks:
            for a, b in zip(key, lock):
                if a + b > height:
                    break
            else:
                result += 1

    print("Part 1:", result)
