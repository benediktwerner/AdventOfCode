#!/usr/bin/env python3

from os import path
from functools import lru_cache


@lru_cache(maxsize=None)
def solve(buckets, target, num=100):
    if num == 0:
        return 0
    total = 0
    for i, b in enumerate(buckets):
        if b > target:
            continue
        elif b == target:
            total += 1
        else:
            total += solve(buckets[i+1:], target - b, num-1)
    return total


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    buckets = tuple(sorted(map(int, f.read().splitlines()), reverse=True))

    print("Part 1:", solve(buckets, 150))

    for i in range(100):
        res = solve(buckets, 150, i)
        if res != 0:
            print("Part 2:", res)
            break
