#!/usr/bin/env python3

from os import path
import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    start, buses = f.read().splitlines()
    start = int(start)
    buses = [int(b) if b != "x" else None for b in buses.split(",")]

    min_arrival = float("inf")
    min_bus = None
    for b in filter(bool, buses):
        next_arrival = b - start % b
        if next_arrival < min_arrival:
            min_arrival, min_bus = next_arrival, b

    print("Part 1:", min_bus * min_arrival)

    M = math.prod(b for b in buses if b is not None)
    result = 0

    for i, b in enumerate(buses):
        if b is None:
            continue

        Mi = M // b
        mi = pow(Mi, -1, b)
        result += (-i) * Mi * mi

    print("Part 2:", result % M)
