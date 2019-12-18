#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import itertools
import math


mem_path = {}
mem_shortest = {}


def path_length(a, b):
    if (a, b) not in mem_path:
        mem_path[(a, b)] = shortest_path_length(g, a, b)
    return mem_path[(a, b)]


def shortest(pos, qkeys, have=None):
    if have is None:
        have = set()
    elif len(have) == len(qkeys):
        return 0

    mem_key = (pos, tuple(sorted(have)))
    if mem_key in mem_shortest:
        return mem_shortest[mem_key]

    m = math.inf

    for k in qkeys - have:
        nx, ny, need = keys[k]
        if need - have:
            continue
        have.add(k)
        m = min(m, shortest((nx, ny), qkeys, have) + path_length(pos, (nx, ny)))
        have.remove(k)

    mem_shortest[mem_key] = m
    return m


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    m = [line.strip() for line in f]
    g = Graph()
    keys = {}
    todo = []

    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == "@":
                start = (x, y)
                todo.append((x, y, set()))

    g.add_node(start)

    while todo:
        x, y, doors = todo.pop()
        c = m[y][x]

        if c.isupper():
            doors.add(c.lower())
        elif c.islower():
            keys[c] = (x, y, doors)

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx = x + dx
            ny = y + dy
            if m[ny][nx] != "#":
                if (nx, ny) not in g:
                    todo.append((nx, ny, doors.copy()))
                g.add_edge((x, y), (nx, ny))

    print("Part 1:", shortest(start, keys.keys()))

    sx, sy = start
    mem_path.clear()
    mem_shortest.clear()
    quadrant_keys = [set() for _ in range(4)]

    for dx, dy in ((0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)):
        g.remove_node((sx + dx, sy + dy))

    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c.islower():
                if x < sx and y < sy:
                    quadrant_keys[0].add(c)
                elif x > sx and y < sy:
                    quadrant_keys[1].add(c)
                elif x > sx and y > sy:
                    quadrant_keys[2].add(c)
                else:
                    quadrant_keys[3].add(c)

    for k, (*_, doors) in keys.items():
        for q in quadrant_keys:
            if k in q:
                doors.intersection_update(q)
                break
    print(
        "Part 2:",
        sum(
            shortest((sx + dx, sy + dy), quadrant_keys[i])
            for i, (dx, dy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))
        ),
    )
