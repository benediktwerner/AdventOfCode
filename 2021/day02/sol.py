#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    depth, x = 0, 0
    depth2, x2, aim = 0, 0, 0

    for line in f.read().splitlines():
        d, a = line.split()
        a = int(a)
        if d == "forward":
            x += a
            x2 += a
            depth2 += aim * a
        elif d == "up":
            depth -= a
            aim -= a
        elif d == "down":
            depth += a
            aim += a

    print("Part 1:", depth * x)
    print("Part 2:", depth2 * x2)
