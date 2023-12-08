#!/usr/bin/env python3

from os import path
import itertools
import math


def steps_until(start, end_fn):
    pos = start
    for i, move in enumerate(itertools.cycle(instructions)):
        if end_fn(pos):
            return i
        pos = network[pos][move == "R"]
    assert False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    instructions = lines[0]
    network = {}
    for line in lines[2:]:
        start, ends = line.split(" = ")
        network[start] = ends[1:-1].split(", ")

    print("Part 1:", steps_until("AAA", lambda pos: pos == "ZZZ"))

    steps = [
        steps_until(start, lambda pos: pos.endswith("Z"))
        for start in network
        if start.endswith("A")
    ]
    print("Part 2:", math.lcm(*steps))
