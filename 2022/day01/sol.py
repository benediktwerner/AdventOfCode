#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    elves = sorted(sum(map(int, elf.splitlines())) for elf in f.read().split("\n\n"))
    print("Part 1:", elves[-1])
    print("Part 2:", sum(elves[-3:]))
