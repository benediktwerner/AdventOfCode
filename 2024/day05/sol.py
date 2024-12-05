#!/usr/bin/env python3

from os import path
from typing import Sequence


def is_ordered(update: Sequence[str]) -> bool:
    for i, a in enumerate(update[:-1]):
        for b in update[i + 1 :]:
            if (a, b) not in orderings:
                return False
    return True


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    orderings, updates = map(str.splitlines, file.read().split("\n\n"))
    orderings = {tuple(line.split("|")) for line in orderings}

    part1 = part2 = 0

    for update in updates:
        update = update.split(",")
        if is_ordered(update):
            part1 += int(update[len(update) // 2])
            continue

        half = len(update) // 2
        for a in update:
            count_after = sum((a, b) in orderings for b in update if b != a)
            if count_after == half:
                part2 += int(a)
                break

    print("Part 1:", part1)
    print("Part 2:", part2)
