#!/usr/bin/env python3

import os
from networkx import DiGraph, dfs_postorder_nodes, shortest_path


with open(os.path.dirname(__file__) + "/input.txt") as f:
    g = DiGraph()

    for line in f:
        line = line.strip()

        a, b = line.split(")")
        g.add_edge(a, b)

    total_orbits = 0

    for n in dfs_postorder_nodes(g, "COM"):
        curr_orbits = 0

        for s in g[n]:
            curr_orbits += g.nodes[s]["orbits"] + 1

        g.nodes[n]["orbits"] = curr_orbits
        total_orbits += curr_orbits

    print("Part 1:", total_orbits)

    shortest_transfer = shortest_path(g.to_undirected(), "YOU", "SAN")
    transfers = len(shortest_transfer) - 3

    print("Part 2:", transfers)
