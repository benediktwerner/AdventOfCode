#!/usr/bin/env python3

from collections import defaultdict


def dist(a, b):
    return sum(abs(a - b) for a, b in zip(a, b))


class Solver:
    def solve(self):
        points = []

        with open("input.txt") as f:
            for line in f:
                points.append(tuple(map(int, line.strip().split(","))))

        self.connections = {}

        for p in points:
            self.connections[p] = {q for q in points if q != p and dist(p, q) <= 3}

        count = 0
        self.visited = set()

        for p in points:
            if p in self.visited:
                continue

            self.visited.add(p)
            self.visit(p)
            count += 1
        
        print("Part 1:", count)

    def visit(self, p):
        for q in self.connections[p]:
            if q not in self.visited:
                self.visited.add(q)
                self.visit(q)


if __name__ == "__main__":
    Solver().solve()
