#!/usr/bin/env python3

from os import path
from functools import cmp_to_key


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    orderings, updates = map(str.splitlines, file.read().split("\n\n"))
    orderings = {tuple(map(int, line.split("|"))) for line in orderings}

    def compare(a: int, b: int) -> int:
        if (a, b) in orderings:
            return -1
        return 1

    part1 = part2 = 0

    for update in updates:
        update = list(map(int, update.split(",")))
        update_sorted = sorted(update, key=cmp_to_key(compare))
        middle = update_sorted[len(update_sorted) // 2]
        if update == update_sorted:
            part1 += middle
        else:
            part2 += middle

    print("Part 1:", part1)
    print("Part 2:", part2)
