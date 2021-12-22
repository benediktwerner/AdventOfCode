#!/usr/bin/env python3

from os import path
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Cube:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    @staticmethod
    def from_line(line):
        return Cube(*map(int, re.findall(r"-?[0-9]+", line)))

    def intersect(self, other):
        c = Cube(
            max(self.x1, other.x1),
            min(self.x2, other.x2),
            max(self.y1, other.y1),
            min(self.y2, other.y2),
            max(self.z1, other.z1),
            min(self.z2, other.z2),
        )
        if c.x1 <= c.x2 and c.y1 <= c.y2 and c.z1 <= c.z2:
            return c

    def volume(self):
        return (
            (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)
        )


def solve(ops, window=None):
    cubes = Counter()
    for on, c in ops:
        if window and (c := c.intersect(window)) is None:
            continue
        new = Counter()
        for cc, count in cubes.items():
            if inter := c.intersect(cc):
                new[inter] -= count
        cubes.update(new)

        if on:
            cubes[c] += 1
    return sum(c.volume() * count for c, count in cubes.items())


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    ops = [
        (line.split()[0] == "on", Cube.from_line(line))
        for line in f.read().splitlines()
    ]
    print("Part 1:", solve(ops, Cube(-50, 50, -50, 50, -50, 50)))
    print("Part 2:", solve(ops))
