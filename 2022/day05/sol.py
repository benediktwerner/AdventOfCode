#!/usr/bin/env python3

from os import path
import re


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = iter(f.read().splitlines())
    stacks = [[] for _ in range(10)]

    for line in lines:
        if not line:
            break
        if line.startswith(" 1"):
            continue
        for i, c in enumerate(line[1::4]):
            if not c.isspace():
                stacks[i + 1].insert(0, c)

    stacks2 = [s[:] for s in stacks]

    for line in lines:
        count, fro, to = ints(line)

        for _ in range(count):
            stacks[to].append(stacks[fro].pop())

        stacks2[to].extend(stacks2[fro][-count:])
        stacks2[fro] = stacks2[fro][:-count]

    print("Part 1:", "".join(s[-1] for s in stacks[1:]))
    print("Part 2:", "".join(s[-1] for s in stacks2[1:]))
