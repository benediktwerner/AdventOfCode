#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    numbers = [int(x) for x in f]
    part1 = None
    part2 = None

    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers[i + 1 :], i + 1):
            if a + b == 2020:
                part1 = a * b

            for c in numbers[j + 1 :]:
                if a + b + c == 2020:
                    part2 = a * b * c

    print("Part 1:", part1)
    print("Part 2:", part2)
