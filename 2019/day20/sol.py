#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import itertools
import math


def add_portal(portal, pos):
    global start, end

    if portal == "AA":
        start = pos
    elif portal == "ZZ":
        end = pos
    elif portal in portals:
        g.add_edge(pos, portals[portal], portal=True)
    else:
        portals[portal] = pos


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    m = [line.rstrip("\n") for line in f]
    width = len(m[0])
    height = len(m)

    g = Graph()
    portals = {}

    for x in range(2, width - 2):
        for y in range(2, height - 2):
            if m[y][x] != ".":
                continue

            right = m[y][x + 1]
            if right == ".":
                g.add_edge((x, y), (x + 1, y), portal=False)
            elif right.isupper():
                add_portal(right + m[y][x + 2], (x, y))

            down = m[y + 1][x]
            if down == ".":
                g.add_edge((x, y), (x, y + 1), portal=False)
            elif down.isupper():
                add_portal(down + m[y + 2][x], (x, y))

            if m[y - 1][x].isupper():
                add_portal(m[y - 2][x] + m[y - 1][x], (x, y))

            if m[y][x - 1].isupper():
                add_portal(m[y][x - 2] + m[y][x - 1], (x, y))

    print("Part 1:", shortest_path_length(g, start, end))

    todo = deque([(0, start, 0)])
    visited = set([(0, start)])

    while todo:
        lvl, pos, steps = todo.popleft()
        
        if lvl == 0 and pos == end:
            print("Part 2:", steps)
            break

        for nxt, attrs in g[pos].items():
            if attrs["portal"]:
                if pos[0] in (2, width-3) or pos[1] in (2, height-3):
                    if lvl == 0:
                        continue
                    lvl -= 1
                else:
                    lvl += 1

            if (lvl, nxt) not in visited:
                todo.append((lvl, nxt, steps+1))
                visited.add((lvl, nxt))
