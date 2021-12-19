#!/usr/bin/env python3

from os import path
from dataclasses import dataclass
import re


@dataclass
class Reindeer:
    fly_speed: int
    fly_time: int
    rest_time: int
    score: int = 0
    pos: int = 0
    flying: bool = False
    left: int = 0

    def step(self):
        if self.left == 0:
            self.flying = not self.flying
            self.left = self.fly_time if self.flying else self.rest_time
        if self.flying:
            self.pos += self.fly_speed
        self.left -= 1

    @staticmethod
    def from_line(line):
        return Reindeer(*map(int, re.findall(r"-?[0-9]+", line)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    reindeer = [Reindeer.from_line(line) for line in f.read().splitlines()]

    for _ in range(2503):
        for r in reindeer:
            r.step()
        max(reindeer, key=lambda r: r.pos).score += 1

    print("Part 1:", max(r.pos for r in reindeer))
    print("Part 2:", max(r.score for r in reindeer))
