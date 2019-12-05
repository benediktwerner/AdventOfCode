#!/usr/bin/env python3

import os
from networkx import DiGraph, topological_sort


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        g = DiGraph()

        for line in f:
            line = line.strip()
            parts = line.split()
            if parts[0] == "value":
                val = int(parts[1])
                bot = int(parts[5])
                if bot not in g:
                    g.add_node(bot, vals=[val])
                else:
                    g.nodes[bot]["vals"].append(val)
            else:
                start = int(parts[1])
                low_type = parts[5]
                low_to = int(parts[6])
                high_type = parts[10]
                high_to = int(parts[11])

                if start not in g:
                    g.add_node(start, vals=[])
                if low_type == "bot":
                    if low_to not in g:
                        g.add_node(low_to, vals=[])
                    g.add_edge(start, low_to, x="low")
                else:
                    g.nodes[start]["output_low"] = low_to
                if high_type == "bot":
                    if high_to not in g:
                        g.add_node(high_to, vals=[])
                    g.add_edge(start, high_to, x="high")
                else:
                    g.nodes[start]["output_high"] = high_to

        outputs = {}

        for bot in topological_sort(g):
            low = min(g.nodes[bot]["vals"])
            high = max(g.nodes[bot]["vals"])
            if low == 17 and high == 61:
                print("Part 1:", bot)
            for n in g[bot]:
                if g[bot][n]["x"] == "low":
                    g.nodes[n]["vals"].append(low)
                else:
                    g.nodes[n]["vals"].append(high)
            if "output_low" in g.nodes[bot]:
                outputs[g.nodes[bot]["output_low"]] = low
            if "output_high" in g.nodes[bot]:
                outputs[g.nodes[bot]["output_high"]] = high

        print("Part 2:", outputs[0] * outputs[1] * outputs[2])


if __name__ == "__main__":
    main()
