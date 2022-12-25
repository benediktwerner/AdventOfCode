#!/usr/bin/env python3

from os import path
import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    total = 0
    for line in f.read().splitlines():
        for i, c in enumerate(reversed(line)):
            total += ("=-012".index(c) - 2) * 5 ** i

    largest_power = int(math.log(total, 5)) + 2
    coeffs = []
    for i in reversed(range(largest_power)):
        for j in reversed(range(5)):
            if j * 5 ** i <= total:
                coeffs.append(j)
                total -= j * 5 ** i
                break

    while any(c > 2 for c in coeffs):
        for i, c in enumerate(coeffs):
            if c > 2:
                coeffs[i - 1] += 1
                coeffs[i] = c - 5

    while coeffs[0] == 0:
        coeffs = coeffs[1:]

    print("".join("012=-"[c] for c in coeffs))
