#!/usr/bin/env python3

from collections import defaultdict
import sys

DIFF = {
    "N": (0, -1),
    "S": (0, 1),
    "W": (-1, 0),
    "E": (1, 0)
}

WALL, DOOR, ROOM = range(3)


class Solver:
    def solve(self):
        with open("input.txt") as f:
            self.regex = f.read().strip()[1:-1]

        self.map = defaultdict(int)

        sys.setrecursionlimit(10000)
        self.explore(0, 0, 0)

        furthest_doors, far_away_count = self.find_furthest()
        print("Part 1:", furthest_doors)
        print("Part 2:", far_away_count)

    def find_furthest(self):
        found = set()
        todo = [(0, 0, 0)]
        count = 0

        while todo:
            x, y, d = todo.pop(0)

            if d >= 1000:
                count += 1

            for xd, yd in DIFF.values():
                nx = x+2*xd
                ny = y+2*yd

                if (nx, ny) in found:
                    continue

                if self.map[(x+xd, y+yd)] == DOOR:
                    found.add((nx, ny))
                    todo.append((nx, ny, d+1))

        return d, count

    def explore(self, i, x, y):
        if i >= len(self.regex):
            return

        self.map[(x, y)] = ROOM

        if self.regex[i] in ("W", "N", "S", "E"):
            xd, yd = DIFF[self.regex[i]]
            self.map[(x+xd, y+yd)] = DOOR

            if self.map[(x+2*xd, y+2*yd)] == ROOM:
                # Room already found
                return

            self.explore(i+1, x+2*xd, y+2*yd)

        elif self.regex[i] == "(":
            paths = [i+1]
            brackets = 1

            while brackets > 0:
                i += 1
                if self.regex[i] == "(":
                    brackets += 1
                elif self.regex[i] == ")":
                    brackets -= 1
                elif self.regex[i] == "|" and brackets == 1:
                    paths.append(i+1)

            for path in paths:
                self.explore(path, x, y)

        elif self.regex[i] == ")":
            self.explore(i+1, x, y)

        elif self.regex[i] == "|":
            brackets = 1

            while brackets > 0:
                i += 1
                if self.regex[i] == "(":
                    brackets += 1
                elif self.regex[i] == ")":
                    brackets -= 1

            self.explore(i+1, x, y)


if __name__ == "__main__":
    Solver().solve()
