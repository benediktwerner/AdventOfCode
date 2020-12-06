#!/usr/bin/env python3

from os import path
import string

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1 = part2 = 0

    for group in f.read().split("\n\n"):
        answers1 = set()
        answers2 = set(string.ascii_lowercase)

        for person in group.split():
            answers1.update(person)
            answers2 &= set(person)

        part1 += len(answers1)
        part2 += len(answers2)

    print("Part 1:", part1)
    print("Part 2:", part2)
