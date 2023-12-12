#!/usr/bin/env python3

from os import path
from functools import cache


@cache
def arrangements(symbols, numbers, i=0):
    if not numbers:
        if not any(s == "#" for s in symbols[i:]):
            return 1
        return 0

    nxt = numbers[0]

    while True:
        if i + nxt > len(symbols):
            return 0
        can_place_here = all(c in "#?" for c in symbols[i : i + nxt])
        can_leave_next_empty = i + nxt >= len(symbols) or symbols[i + nxt] != "#"
        if can_place_here and can_leave_next_empty:
            count = arrangements(symbols, numbers[1:], i + nxt + 1)
            if symbols[i] == "?":
                count += arrangements(symbols, numbers, i + 1)
            return count
        if symbols[i] == "#":
            return 0
        i += 1


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1, part2 = 0, 0

    for line in file.read().splitlines():
        symbols, numbers = line.split()
        numbers = tuple(map(int, numbers.split(",")))

        part1 += arrangements(symbols, numbers)

        symbols = "?".join(5 * [symbols])
        numbers *= 5
        part2 += arrangements(symbols, numbers)

    print("Part 1:", part1)
    print("Part 2:", part2)
