#!/usr/bin/env python3

from os import path
from collections import defaultdict


def filter(nums: list, op, i=0):
    if len(nums) == 1:
        return int(nums[0], 2)

    c = sum((x[i] == "1") * 2 - 1 for x in nums)
    nums = [x for x in nums if op(c, 0) == int(x[i])]
    return filter(nums, op, i + 1)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    bit_count = defaultdict(int)
    nums = []

    for line in f.read().splitlines():
        for i, bit in enumerate(reversed(line)):
            bit_count[i] += (bit == "1") * 2 - 1
        nums.append(line)

    gamma, epsilon = 0, 0

    for i, x in bit_count.items():
        gamma |= (x > 0) << i
        epsilon |= (x < 0) << i

    print("Part 1:", gamma * epsilon)
    print("Part 2:", filter(nums, int.__ge__) * filter(nums, int.__lt__))
