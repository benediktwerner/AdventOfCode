#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    age = {}
    nums = list(map(int, f.read().strip().split(",")))
    for i, n in enumerate(nums[:-1]):
        age[n] = i

    last = nums[-1]
    for t in range(len(nums)-1, 2019):
        age[last], last = t, t - age.get(last, t)

    print("Part 1:", last)

    for t in range(2019, 30000000-1):
        age[last], last = t, t - age.get(last, t)

    print("Part 2:", last)
