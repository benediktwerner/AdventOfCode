#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from os import path
from typing import Iterator


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


@dataclass
class Range:
    """half open range [start, start+length)"""

    start: int
    length: int

    @property
    def end(self):
        """end is exclusive to the range"""
        return self.start + self.length

    @staticmethod
    def new_with_end(start: int, end: int) -> Range:
        return Range(start, end - start)

    def overlap(self: Range, other: Range) -> Range | None:
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start < end:
            return Range.new_with_end(start, end)

    def shift(self: Range, amount: int):
        return Range(self.start + amount, self.length)

    def remove(self: Range, other: Range) -> Iterator[Range]:
        if self.start < other.start:
            yield Range.new_with_end(self.start, min(self.end, other.start))
        if other.end < self.end:
            yield Range.new_with_end(max(other.end, self.start), self.end)


def solve(ranges: list[Range], maps: list[list[tuple[Range, int]]]):
    for m in maps:
        new_ranges = []
        for source_range, shift in m:
            leftover_ranges = []
            for r in ranges:
                if overlap := source_range.overlap(r):
                    new_ranges.append(overlap.shift(shift))
                    leftover_ranges.extend(r.remove(overlap))
                else:
                    leftover_ranges.append(r)
            ranges = leftover_ranges
        ranges += new_ranges
    return min(r.start for r in ranges)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    seeds, *maps = f.read().split("\n\n")
    seeds = ints(seeds)
    maps = [
        [
            (Range(source_start, map_length), target_start - source_start)
            for target_start, source_start, map_length in map(ints, m.splitlines()[1:])
        ]
        for m in maps
    ]
    print("Part 1:", solve([Range(x, 1) for x in seeds], maps))
    print(
        "Part 2:", solve([Range(s, l) for s, l in zip(seeds[::2], seeds[1::2])], maps)
    )
