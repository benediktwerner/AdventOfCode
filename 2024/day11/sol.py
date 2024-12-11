#!/usr/bin/env python3

from collections import defaultdict
from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    counts = {int(stone): 1 for stone in file.read().strip().split()}

    for i in range(75):
        if i == 25:
            print("Part 1:", sum(counts.values()))

        new_counts = defaultdict(int)
        for s, c in counts.items():
            if s == 0:
                new_counts[1] += c
                continue
            ss = str(s)
            if len(ss) % 2 == 0:
                new_counts[int(ss[: len(ss) // 2])] += c
                new_counts[int(ss[len(ss) // 2 :])] += c
            else:
                new_counts[s * 2024] += c
        counts = new_counts

    print("Part 2:", sum(counts.values()))
