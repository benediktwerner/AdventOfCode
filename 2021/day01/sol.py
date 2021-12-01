#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    depths = [int(x) for x in f.read().splitlines()]
    print("Part 1:", sum(b > a for a, b in zip(depths, depths[1:])))
    print("Part 2:", sum(b > a for a, b in zip(depths, depths[3:])))
