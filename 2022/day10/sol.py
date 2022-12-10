#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1, part2 = 0, ""
    cycle = 1
    value = 1

    for line in f.read().splitlines():
        if (cycle - 1) % 40 == 0:
            part2 += "\n"
        part2 += "#" if (cycle - 1) % 40 in (value - 1, value, value + 1) else " "
        if cycle in (20, 60, 100, 140, 180, 220):
            part1 += cycle * value

        if line.startswith("noop"):
            cycle += 1
        else:
            if cycle % 40 == 0:
                part2 += "\n"
            part2 += "#" if cycle % 40 in (value - 1, value, value + 1) else " "
            if cycle + 1 in (20, 60, 100, 140, 180, 220):
                part1 += (cycle + 1) * value
            cycle += 2
            value += int(line.split()[1])

    print("Part 1:", part1)
    print("Part 2:", part2)
