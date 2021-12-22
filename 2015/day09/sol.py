#!/usr/bin/env python3

from os import path
from collections import defaultdict
import itertools

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    G = defaultdict(dict)
    for line in f.read().splitlines():
        start, _, end, _, cost = line.split()
        G[start][end] = int(cost)
        G[end][start] = int(cost)

    def dists():
        for perm in itertools.permutations(G):
            yield sum(G[a][b] for a, b in zip(perm, perm[1:]))

    print("Part 1:", min(dists()))
    print("Part 2:", max(dists()))
