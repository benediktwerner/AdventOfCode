#!/usr/bin/env python3

import itertools
import math
import re
from os import path

WIDTH = 101
HEIGHT = 103


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def simulate(robots, steps):
    positions = []
    for x, y, vx, vy in robots:
        x = (x + vx * steps) % WIDTH
        y = (y + vy * steps) % HEIGHT
        positions.append((x, y))
    return positions


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    robots = [ints(line) for line in file.read().splitlines()]

    quadrants = [0, 0, 0, 0]
    for x, y in simulate(robots, 100):
        if x != WIDTH // 2 and y != HEIGHT // 2:
            qx = x < WIDTH // 2
            qy = y < HEIGHT // 2
            quadrants[qx * 2 + qy] += 1

    print("Part 1:", math.prod(quadrants))

    for i in itertools.count(1):
        positions = simulate(robots, i)
        if len(positions) == len(set(positions)):
            break

    print("Part 2:", i)
