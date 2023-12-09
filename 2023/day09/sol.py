#!/usr/bin/env python3

from os import path


def extrapolate(line: list[int], part2: bool) -> int:
    diffs = [line]
    while not all(x == 0 for x in diffs[-1]):
        line = diffs[-1]
        diffs.append([])
        for a, b in zip(line, line[1::]):
            diffs[-1].append(b - a)
    last = 0
    for line in reversed(diffs[:-1]):
        if part2:
            last = line[0] - last
        else:
            last = line[-1] + last
    return last


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = [list(map(int, line.split())) for line in f.read().splitlines()]
    print("Part 1:", sum(extrapolate(line, False) for line in lines))
    print("Part 2:", sum(extrapolate(line, True) for line in lines))
