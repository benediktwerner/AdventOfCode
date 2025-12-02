#!/usr/bin/env python3

from os import path


def is_repeated(n: str, times: int) -> bool:
    if len(n) % times != 0:
        return False
    size = len(n) // times
    pattern = n[:size]
    for i in range(1, times):
        if pattern != n[i * size : (i + 1) * size]:
            return False
    return True


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    for r in file.read().strip().split(","):
        a, b = map(int, r.split("-"))
        for n in map(str, range(a, b + 1)):
            if is_repeated(n, 2):
                part1 += int(n)
            if any(is_repeated(n, times) for times in range(2, len(n) + 1)):
                part2 += int(n)

    print("Part 1:", part1)
    print("Part 2:", part2)
