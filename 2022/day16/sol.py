#!/usr/bin/env python3

from os import path
from collections import defaultdict
from networkx import *


def do(pos1, pos2, min1, min2, graph, rates, visited, flow, minutes):
    if minutes == 0:
        return flow

    if min1 > 0 and min2 > 0:
        return do(
            pos1, pos2, min1 - 1, min2 - 1, graph, rates, visited, flow, minutes - 1
        )

    best = flow
    if min1 == 0:
        found = False
        for to, dist in graph[pos1]:
            if dist >= minutes or to in visited:
                continue
            found = True
            visited.add(to)
            result = do(
                to,
                pos2,
                dist,
                min2,
                graph,
                rates,
                visited,
                flow + rates[to] * (minutes - dist),
                minutes,
            )
            visited.remove(to)
            if result > best:
                best = result
        if found:
            return best

    if min2 == 0:
        for to, dist in graph[pos2]:
            if dist >= minutes or to in visited:
                continue
            visited.add(to)
            result = do(
                pos1,
                to,
                min1,
                dist,
                graph,
                rates,
                visited,
                flow + rates[to] * (minutes - dist),
                minutes,
            )
            visited.remove(to)
            if result > best:
                best = result

    return best


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    G = Graph()
    rates = {"AA": 0}
    for line in f.read().splitlines():
        words = line.split()
        name = words[1]
        rate = int(words[4][5:-1])
        if rate > 0:
            rates[name] = rate
        G.add_node(name)
        for to in "".join(words[9:]).split(","):
            G.add_edge(name, to)

    graph = defaultdict(list)
    for fro in rates:
        for to in rates:
            graph[fro].append((to, shortest_path_length(G, fro, to) + 1))

    print("Part 1:", do("AA", "AA", 0, 100, graph, rates, set(["AA"]), 0, 30))
    print(
        "This will take a while. Print graph, paste it into the code, comment out networkx, and run with pypy for speedup."
    )
    print("Part 2:", do("AA", "AA", 0, 0, graph, rates, set(["AA"]), 0, 26))
