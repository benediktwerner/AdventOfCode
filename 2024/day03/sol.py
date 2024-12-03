#!/usr/bin/env python3

from os import path
import math
import re


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0
    enabled = True
    for line in file.read().splitlines():
        for op in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line):
            if op == "do()":
                enabled = True
            elif op == "don't()":
                enabled = False
            else:
                nums = re.findall(r"\d+", op)
                result = math.prod(map(int, nums))
                part1 += result
                if enabled:
                    part2 += result

    print("Part 1:", part1)
    print("Part 2:", part2)
