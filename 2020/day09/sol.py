#!/usr/bin/env python3

from os import path
import itertools


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    nums = [int(line) for line in f]

    for i, num in enumerate(nums[25:], 25):
        for pair in itertools.combinations(nums[i-25:i], 2):
            if sum(pair) == num:
                break
        else:
            print("Part 1:", num)
            break

    for n in itertools.count(2):
        for i in range(len(nums) - n):
            group = nums[i : i + n]
            if sum(group) == num:
                print("Part 2:", min(group) + max(group))
                break
        else:
            continue
        break
