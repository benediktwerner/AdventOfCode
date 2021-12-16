#!/usr/bin/env python3

from os import path
from collections import defaultdict


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    intervals = defaultdict(int)

    for line in f.read().splitlines():
        start, end = map(int, line.split("-"))
        intervals[start] += 1
        intervals[end + 1] -= 1

c = 0
count = 0
first = None
last = 0

for k in sorted(intervals):
    v = intervals[k]
    if c == 0 and v != 0:
        count += k - last
    c += v
    if c == 0:
        if first is None:
            first = k
        last = k

print("Part 1:", first)
print("Part 2:", count)
