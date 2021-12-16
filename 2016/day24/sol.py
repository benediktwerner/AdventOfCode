#!/usr/bin/env python3

from collections import defaultdict
from itertools import chain, permutations
from os import path

from networkx import Graph, shortest_path_length


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    nodes = set()
    goals = set()
    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(line):
            if c != "#":
                nodes.add((x, y))
                if c == "0":
                    start = x, y
                elif c != ".":
                    goals.add((x, y))

    G = Graph()
    for x, y in nodes:
        if (x + 1, y) in nodes:
            G.add_edge((x, y), (x + 1, y))
        if (x, y + 1) in nodes:
            G.add_edge((x, y), (x, y + 1))

    shortest = defaultdict(dict)
    for a in chain(goals, [start]):
        for b in chain(goals, [start]):
            shortest[a][b] = shortest_path_length(G, a, b)

    print(
        "Part 1:",
        min(
            sum(shortest[a][b] for a, b in zip(chain([start], perm), perm))
            for perm in permutations(goals)
        ),
    )
    print(
        "Part 2:",
        min(
            sum(
                shortest[a][b]
                for a, b in zip(chain([start], perm), chain(perm, [start]))
            )
            for perm in permutations(goals)
        ),
    )
