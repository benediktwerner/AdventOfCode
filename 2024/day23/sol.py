#!/usr/bin/env python3

from os import path

import networkx as nx


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    G = nx.Graph()
    for line in file.read().splitlines():
        G.add_edge(*line.split("-"))

    print(
        "Part 1:",
        sum(
            len(clique) == 3 and any(n.startswith("t") for n in clique)
            for clique in nx.enumerate_all_cliques(G)
        ),
    )

    max_clique = max(nx.find_cliques(G), key=len)
    print("Part 2:", ",".join(sorted(max_clique)))
