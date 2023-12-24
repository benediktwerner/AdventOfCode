#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from os import path

import z3

MIN = 200000000000000
MAX = 400000000000000


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


@dataclass
class Projectile:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @staticmethod
    def from_str(string: str):
        return Projectile(*ints(string))

    def at(self, t: int) -> Point2:
        return Point2(self.x + self.vx * t, self.y + self.vy * t)

    def meet(self, other) -> Point2 | None:
        if self.vx == 0:
            if other.vx == 0:
                if self.x != other.x:
                    return None
                assert False
            # other.x + other.vx * t = self.x
            t = (self.x - other.x) / other.vx
            return other.at(t)

        if other.vx == 0:
            # self.x + self.vx * t = other.x
            t = (other.x - self.x) / self.vx
            return self.at(t)

        sm = self.vy / self.vx
        om = other.vy / other.vx

        if sm == om:
            if self.y != other.y:
                return None
            assert False

        # self.y + sm * (x - self.x) = other.y + om * (x - other.x)
        x = (other.y - self.y + sm * self.x - om * other.x) / (sm - om)
        # self.x + self.vx * t = x
        t = (x - self.x) / self.vx
        if t < 0:
            return None
        t = (x - other.x) / other.vx
        if t < 0:
            return None
        return other.at(t)


@dataclass
class Point2:
    x: int
    y: int


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = 0
    projectiles = [Projectile.from_str(line) for line in file.read().splitlines()]
    x, y, z, vx, vy, vz = z3.Ints("x y z vx vy vz")
    s = z3.Solver()
    for i, a in enumerate(projectiles):
        t = z3.Int(f"t{i}")
        s.add(t >= 0)
        s.add(x + vx * t == a.x + a.vx * t)
        s.add(y + vy * t == a.y + a.vy * t)
        s.add(z + vz * t == a.z + a.vz * t)
        for b in projectiles[i + 1 :]:
            if (meet := a.meet(b)) and MIN <= meet.x <= MAX and MIN <= meet.y <= MAX:
                part1 += 1

    print("Part 1:", part1)

    assert s.check() == z3.sat
    m = s.model()
    print("Part 2:", sum(m[t].as_long() for t in (x, y, z)))
