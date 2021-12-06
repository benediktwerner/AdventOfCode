#!/usr/bin/env python3

from os import path
from collections import Counter


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    count = Counter(map(int, f.read().strip().split(",")))

    for i in range(256):
        if i == 80:
            print("Part 1:", sum(count.values()))

        new_count = Counter()

        for fish, c in count.items():
            if fish == 0:
                new_count[6] += c
                new_count[8] += c
            else:
                new_count[fish-1] += c

        count = new_count

    print("Part 2:", sum(count.values()))
