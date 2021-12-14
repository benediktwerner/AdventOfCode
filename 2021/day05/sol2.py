#!/usr/bin/env python3

# Challenge: https://www.reddit.com/r/adventofcode/comments/r9hpfs/2021_day_5_bigger_vents/

from __future__ import annotations
from collections import defaultdict

from os import path
import re
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point

    @classmethod
    def from_str(cls, line: str) -> Line:
        x1, y1, x2, y2 = map(int, re.findall(r"-?[0-9]+", line))
        assert x1 == x2 or y1 == y2
        return cls(Point(min(x1, x2), min(y1, y2)), Point(max(x1, x2), max(y1, y2)))

    def horizontal(self: Line) -> bool:
        return self.start.y == self.end.y

    def contains(self, p: Point) -> bool:
        if self.horizontal():
            return p.y == self.start.y and self.start.x <= p.x <= self.end.x
        else:
            return p.x == self.start.x and self.start.y <= p.y <= self.end.y

    def intersect(self: Line, other: Line) -> Union[Line, Point, None]:
        if self.horizontal() == other.horizontal():
            if self.contains(other.start):
                if self.contains(other.end):
                    return other
                else:
                    return Line(other.start, self.end)
            elif self.contains(other.end):
                return Line(self.start, other.end)
        else:
            p = (
                Point(self.start.y, other.start.x)
                if self.horizontal()
                else Point(self.start.x, other.start.y)
            )
            if self.contains(p):
                return Line(p, p)


def combine(lines, start, end):
    it = iter(lines)
    for x1, x2 in it:
        if x2 < start:
            yield x1, x2
        elif x1 <= start or x1 <= end:
            x1 = min(x1, start)
            x2 = max(x2, end)
            for xx1, xx2 in it:
                if x2 < xx1:
                    yield x1, x2
                    yield xx1, xx2
                    yield from it
                    return
                x2 = max(x2, xx2)
            yield x1, x2
            yield from it
            return
        else:
            yield start, end
            yield x1, x2
            yield from it
            return

    yield start, end


with open(path.join(path.dirname(__file__), "input2.txt")) as f:
    lines = []
    horizontal = defaultdict(list)
    vertical = defaultdict(list)
    for line in f.read().splitlines():
        line = Line.from_str(line)
        for other in lines:
            if inter := line.intersect(other):
                if inter.horizontal():
                    horizontal[inter.start.y] = list(
                        combine(horizontal[inter.start.y], inter.start.x, inter.end.x)
                    )
                else:
                    vertical[inter.start.x] = list(
                        combine(vertical[inter.start.x], inter.start.y, inter.end.y)
                    )
        lines.append(line)

    double_points = set()
    for y, h in horizontal.items():
        for x1, x2 in h:
            for x, v in vertical.items():
                if x2 < x or x < x1:
                    continue
                for y1, y2 in v:
                    if y1 <= y <= y2:
                        double_points.add(Point(x, y))
                        break

    print(sum(len(h) for h in horizontal.values()))
    print(sum(len(h) for h in vertical.values()))
    print(sum(a == b for h in horizontal.values() for a, b in h))

    horizontal_len = sum(b - a + 1 for h in horizontal.values() for a, b in h)
    vertical_len = sum(b - a + 1 for v in vertical.values() for a, b in v)
    print(horizontal_len)
    print(vertical_len)
    print(double_points)
    print(horizontal_len + vertical_len - len(double_points))
