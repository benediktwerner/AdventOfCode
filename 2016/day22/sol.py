#!/usr/bin/env python3

from os import path
from itertools import permutations
from collections import defaultdict, deque
from dataclasses import dataclass
import re


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int

    @property
    def coord(self):
        return self.x, self.y

    @property
    def avail(self):
        return self.size - self.used


nodes = {}

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    for line in f.read().splitlines()[2:]:
        x, y, size, used, avail = map(
            int,
            re.match(
                r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line
            ).groups(),
        )
        nodes[x, y] = Node(x, y, size, used)

moves = defaultdict(list)
viable = 0

for a, b in permutations(nodes.values(), 2):
    if a.used != 0 and a.used <= b.avail:
        viable += 1
    if a.used <= b.size and abs(a.x - b.x) + abs(a.y - b.y) == 1:
        moves[b.coord].append(a.coord)

print("Part 1:", viable)


def path_steps(start, end, blocked):
    if start == end:
        return 0

    todo = deque([(start, 0)])
    seen = set([start, blocked])
    while todo:
        c, s = todo.popleft()
        for n in moves[c]:
            if n not in seen:
                if n == end:
                    return s + 1
                seen.add(n)
                todo.append((n, s + 1))


x = max(x for x, _ in nodes)
empty = next(n.coord for n in nodes.values() if n.used == 0)
steps = 0

while x != 0:
    steps += path_steps(empty, (x - 1, 0), (x, 0)) + 1
    empty = x, 0
    x -= 1

print("Part 2:", steps)
