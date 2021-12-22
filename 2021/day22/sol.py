#!/usr/bin/env python3

from __future__ import annotations

from os import path
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator


def ints(string):
    return map(int, re.findall(r"-?[0-9]+", string))


@dataclass(frozen=True)
class Line:
    start: int
    end: int

    def cut_off(self, other: Line) -> List[Tuple[bool, Line]]:
        if other.end < self.start or self.end < other.start:
            return [(True, self)]
        elif other.start <= self.start and self.end <= other.end:
            return [(False, self)]
        elif other.start <= self.start and other.end < self.end:
            return [
                (False, Line(self.start, other.end)),
                (True, Line(other.end + 1, self.end)),
            ]
        elif self.start < other.start and self.end <= other.end:
            return [
                (True, Line(self.start, other.start - 1)),
                (False, Line(other.start, self.end)),
            ]
        else:
            return [
                (True, Line(self.start, other.start - 1)),
                (False, other),
                (True, Line(other.end + 1, self.end)),
            ]

    def intersect(self, other: Line) -> Optional[Line]:
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start <= end:
            return Line(start, end)

    @property
    def length(self) -> int:
        return max(self.end - self.start + 1, 0)

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.start, self.end + 1))


@dataclass(frozen=True)
class Cube:
    x: Line
    y: Line
    z: Line

    def cut_off(self, other: Cube) -> Iterator[Cube]:
        for x, xl in self.x.cut_off(other.x):
            for y, yl in self.y.cut_off(other.y):
                for z, zl in self.z.cut_off(other.z):
                    if x or y or z:
                        yield Cube(xl, yl, zl)

    def intersect(self, other: Cube) -> Optional[Cube]:
        x = self.x.intersect(other.x)
        y = self.y.intersect(other.y)
        z = self.z.intersect(other.z)
        if x and y and z:
            return Cube(x, y, z)

    @property
    def volume(self) -> int:
        return self.x.length * self.y.length * self.z.length


def part1(ops: List[Tuple[bool, Cube]]) -> int:
    cubes = set()
    area = Cube(*([Line(-50, 50)] * 3))
    for on, c in ops:
        if cube := c.intersect(area):
            for x in cube.x:
                for y in cube.y:
                    for z in cube.z:
                        coord = (x, y, z)
                        if on:
                            cubes.add(coord)
                        elif coord in cubes:
                            cubes.remove(coord)
    return len(cubes)


def part2(ops: List[Tuple[bool, Cube]]) -> int:
    volume = 0
    for i, (on, c) in enumerate(ops):
        cs = [c] if on else []
        for onn, cube in ops[:i]:
            if on == onn:
                new_cs = []
                for g in cs:
                    new_cs.extend(g.cut_off(cube))
                cs = new_cs
            elif cube := c.intersect(cube):
                new_cs = [cube]
                for g in cs:
                    new_cs.extend(g.cut_off(cube))
                cs = new_cs
        volume += sum(c.volume for c in cs) * (-1, 1)[on]

    return volume


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    ops = []
    for line in f.read().splitlines():
        on = line.split()[0] == "on"
        x1, x2, y1, y2, z1, z2 = ints(line)
        c = Cube(Line(x1, x2), Line(y1, y2), Line(z1, z2))
        ops.append((on, c))

    print("Part 1:", part1(ops))
    print("Part 2:", part2(ops))
