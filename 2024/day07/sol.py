#!/usr/bin/env python3

from os import path
import operator
import itertools
from typing import Callable


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def can_compute(
    target: int, nums: list[int], possible_ops: list[Callable[[int, int], int]]
) -> bool:
    for ops in itertools.product(possible_ops, repeat=len(nums) - 1):
        curr = nums[0]
        for i, op in enumerate(ops, start=1):
            curr = op(curr, nums[i])
        if curr == target:
            return True
    return False


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0
    for line in file.read().splitlines():
        target, *nums = map(int, line.replace(":", "").split())
        if can_compute(target, nums, [operator.add, operator.mul]):
            part1 += target
            part2 += target
        elif can_compute(target, nums, [operator.add, operator.mul, concat]):
            part2 += target

    print("Part 1:", part1)
    print("Part 2:", part2)
