#!/usr/bin/env python3

from collections import defaultdict
from os import path


def expand_cliques(cliques: set[tuple[str, ...]]) -> set[tuple[str, ...]]:
    """Given the set of n-size cliques, returns the set of (n+1)-size cliques"""

    new_cliques = set()
    for a, *rest in cliques:
        for n in graph[a]:
            if n not in rest and all(n in graph[b] for b in rest):
                new_cliques.add(tuple(sorted((a, n, *rest))))
    return new_cliques


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    graph = defaultdict(set)
    two_cliques = set()
    for line in file.read().splitlines():
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)
        two_cliques.add(tuple(sorted((a, b))))

    three_cliques = expand_cliques(two_cliques)
    print("Part 1:", sum(any(x.startswith("t") for x in cs) for cs in three_cliques))

    cliques = three_cliques
    while len(cliques) > 1:
        cliques = expand_cliques(cliques)

    print("Part 2:", ",".join(sorted(cliques.pop())))
