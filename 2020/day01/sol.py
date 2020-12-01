#!/usr/bin/env python3

from os import path
import itertools
import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    numbers = [int(x) for x in f]

    def solve(count):
        for ns in itertools.combinations(numbers, count):
            if sum(ns) == 2020:
                return math.prod(ns)

    print("Part 1:", solve(2))
    print("Part 2:", solve(3))
