#!/usr/bin/env python3

from os import path
from math import log2


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    elves = int(f.read())
    pow2 = 2 ** int(log2(elves))
    print("Part 1:", (elves - pow2) * 2 + 1)

    prev = 0
    for i in range(2, elves + 1):
        remove = i // 2
        prev += 1
        if prev >= remove:
            prev += 1
        prev %= i

    print("Part 2:", prev + 1)
