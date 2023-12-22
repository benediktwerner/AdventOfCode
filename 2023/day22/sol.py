#!/usr/bin/env python3

from os import path
from collections import defaultdict
import re


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def find_blockers(x1, y1, x2, y2, z):
    blockers = set()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if (x, y, z) in occupied:
                blockers.add(occupied[x, y, z])
    return blockers


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    bricks = []
    for line in file.read().splitlines():
        start, end = line.split("~")
        bricks.append((ints(start), ints(end)))

    bricks.sort(key=lambda x: x[0][2])  # sort by z

    occupied = {}
    supporting = defaultdict(set)

    for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(bricks):
        assert x2 >= x1
        assert y2 >= y1
        assert z2 >= z1
        zd = z2 - z1
        lowest_z = z1
        for lowest_z in range(z1 - 1, 0, -1):
            if supporters := find_blockers(x1, y1, x2, y2, lowest_z):
                supporting[i] = supporters
                lowest_z += 1
                break
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(lowest_z, lowest_z + zd + 1):
                    occupied[x, y, z] = i

    supported_by = defaultdict(list)
    for i, supporters in supporting.items():
        for s in supporters:
            supported_by[s].append(i)

    part1 = 0
    for i in range(len(bricks)):
        if not supported_by[i] or all(len(supporting[s]) > 1 for s in supported_by[i]):
            part1 += 1

    print("Part 1:", part1)

    part2 = 0
    for i in range(len(bricks)):
        dropped = set([i])
        for i in range(i + 1, len(bricks)):
            if supporting[i] and all(s in dropped for s in supporting[i]):
                dropped.add(i)
        part2 += len(dropped) - 1

    print("Part 2:", part2)
