#!/usr/bin/env python3

from collections import defaultdict
from itertools import count
import sys

EMPTY, WATER, CLAY = range(3)


def parse_line(line):
    a, b = line.strip().split(", ")
    a = int(a[2:])
    b, c = map(int, b[2:].split(".."))

    if line[0] == "x":
        return (a, a, b, c)
    return (b, c, a, a)


class Solver:
    def load_input(self):
        self.grid = defaultdict(int)
        self.min_y = 10000
        self.max_y = 0

        with open("input.txt") as f:
            for line in f:
                x1, x2, y1, y2 = parse_line(line)
                for x in range(x1, x2+1):
                    for y in range(y1, y2+1):
                        self.grid[(x, y)] = CLAY
                self.min_y = min(self.min_y, y1)
                self.max_y = max(self.max_y, y2)

    def count_water(self):
        water = 0
        for cord in self.grid:
            if self.grid[cord] == WATER:
                if cord[1] >= self.min_y and cord[1] <= self.max_y:
                    water += 1

        return water

    def print_map(self):
        min_x = min(cord[0] for cord in self.grid if self.grid[cord] == WATER) - 1
        max_x = max(cord[0] for cord in self.grid if self.grid[cord] == WATER) + 1

        for y in range(self.min_y, self.max_y+1):
            for x in range(min_x, max_x+1):
                print(self.grid[(x, y)], end="")
            print()

    def solve(self):
        self.load_input()
        self.fill(500, 0)

        print("Part 1:", self.count_water())

        sys.setrecursionlimit(10000)
        min_x = min(cord[0] for cord in self.grid)
        max_x = max(cord[0] for cord in self.grid)

        for x in range(min_x, max_x+1):
            self.drain(x, self.max_y)

        print("Part 2:", self.count_water())

    def drain(self, x, y):
        if self.grid[(x, y)] != WATER:
            return
        self.grid[(x, y)] = EMPTY
        self.drain(x-1, y)
        self.drain(x+1, y)
        self.drain(x, y-1)

    def fill(self, sx, sy):
        end = False

        for y in count():
            if sy+y > self.max_y:
                end = True
                break
            elif self.grid[(sx, sy+y)] != EMPTY:
                if self.grid[(sx, sy+y)] == WATER:
                    for x in count(1):
                        if self.grid[(sx+x, sy+y)] != WATER:
                            end = (self.grid[(sx+x, sy+y)] == EMPTY)
                            break
                    if not end:
                        for x in count(-1, -1):
                            if self.grid[(sx+x, sy+y)] != WATER:
                                end = (self.grid[(sx+x, sy+y)] == EMPTY)
                                break
                break

        while not end:
            for y in count():
                if sy+y > self.max_y:
                    end = True
                    break
                if self.grid[(sx, sy+y)] != EMPTY:
                    y -= 1
                    self.grid[(sx, sy+y)] = WATER

                    for d in (-1, 1):
                        for x in count(d, d):
                            if self.grid[(sx+x, sy+y)] != EMPTY:
                                if self.grid[(sx+x, sy+y)] == WATER:
                                    end = True
                                break

                            self.grid[(sx+x, sy+y)] = WATER

                            if self.grid[(sx+x, sy+y+1)] == EMPTY:
                                if self.fill(sx+x, sy+y+1):
                                    end = True
                                    break

                    if not end and y == 0:
                        return False
                    break

        for y in range(sy, sy+y):
            self.grid[(sx, y)] = WATER

        return True


if __name__ == "__main__":
    Solver().solve()
