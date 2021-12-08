#!/usr/bin/env python3

from os import path


def euler_sum(x):
    return (x + 1) * x // 2


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    crabs = list(map(int, f.read().strip().split(",")))
    left, right = min(crabs), max(crabs)
    part1, part2 = float("inf"), float("inf")
    for target in range(left, right + 1):
        part1 = min(part1, sum(abs(target - c) for c in crabs))
        part2 = min(part2, sum(euler_sum(abs(target - c)) for c in crabs))
    print("Part 1:", part1)
    print("Part 2:", part2)

    from math import ceil

    mean = sum(crabs) / len(crabs)
    target = ceil((sum(crabs) - sum(c < mean for c in crabs)) / len(crabs))
    print("Part 2:", sum(euler_sum(abs(target - c)) for c in crabs))

    # part1 target = median i.e. crabs.sort(); crans[len(crabs)//2]
    # part2 target = mean = sum(crabs)/len(crabs); ceil((sum(crabs) - sum(c < mean for c in crabs))/len(crabs))
