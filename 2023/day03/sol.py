#!/usr/bin/env python3

from os import path
from collections import defaultdict
import math


def neighbors(lines, x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            xx = x + dx
            yy = y + dy
            if xx < 0 or yy < 0 or xx >= len(lines) or yy >= len(lines):
                continue
            yield xx, yy, lines[yy][xx]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    part1 = 0
    potential_gears = defaultdict(list)

    for y, line in enumerate(lines):
        x = 0
        while x < len(line):
            if not line[x].isdigit():
                x += 1
                continue

            is_part_number = False
            stars = set()
            num = ""

            while x < len(line) and line[x].isdigit():
                num += line[x]
                for xx, yy, cc in neighbors(lines, x, y):
                    if cc == "*":
                        stars.add((xx, yy))
                    if cc != "." and not cc.isdigit():
                        is_part_number = True
                x += 1

            if is_part_number:
                part1 += int(num)
            for g in stars:
                potential_gears[g].append(int(num))
            x += 1

    print("Part 1:", part1)
    print("Part 2:", sum(math.prod(g) for g in potential_gears.values() if len(g) == 2))
