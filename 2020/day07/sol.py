#!/usr/bin/env python3

from os import path
from networkx import DiGraph, dfs_postorder_nodes

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    G = DiGraph()

    for line in f:
        bag, contains = line.strip().rstrip(".").split(" bags contain ")

        if contains == "no other bags":
            continue

        for other in contains.split(", "):
            count = int(other[0])
            other = other[2:].rstrip("bags").strip()
            G.add_edge(bag, other, count=count)

    print("Part 1:", len(list(dfs_postorder_nodes(G.reverse(), "shiny gold"))) - 1)

    for node in dfs_postorder_nodes(G, "shiny gold"):
        G.nodes[node]["count"] = sum(
            (G.nodes[n]["count"] + 1) * v["count"] for (n, v) in G[node].items()
        )

    print("Part 2:", G.nodes["shiny gold"]["count"])
