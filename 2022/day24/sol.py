#!/usr/bin/env python3

from os import path
import itertools
from dataclasses import dataclass

BLIZZARDS = ">v<^"
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


@dataclass
class Blizzard:
    d: int
    x: int
    y: int

    def move(self):
        dx, dy = DIRS[self.d]
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < width and 0 <= ny < height:
            self.x, self.y = nx, ny
        elif self.d == 0:
            self.x = 0
        elif self.d == 1:
            self.y = 0
        elif self.d == 2:
            self.x = width - 1
        else:
            self.y = height - 1


def shortest_path(start, target):
    pos = {start}
    for i in itertools.count():
        free = set((x, y) for x in range(width) for y in range(height))
        free.add(start)
        free.add(target)
        for b in blizzards:
            b.move()
            free -= {(b.x, b.y)}
        new_pos = set()
        for x, y in pos:
            new_pos.add((x, y))
            for dx, dy in DIRS:
                new_pos.add((x + dx, y + dy))
        pos = new_pos & free
        if target in pos:
            return i + 1


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = [line[1:-1] for line in f.read().splitlines()[1:-1]]

width = len(grid[0])
height = len(grid)

blizzards = []
for y, line in enumerate(grid):
    for x, c in enumerate(line):
        if c in BLIZZARDS:
            blizzards.append(Blizzard(BLIZZARDS.index(c), x, y))

start = (0, -1)
target = (width - 1, height)
part1 = shortest_path(start, target)
print("Part 1:", part1)
print("Part 2:", part1 + shortest_path(target, start) + shortest_path(start, target))
