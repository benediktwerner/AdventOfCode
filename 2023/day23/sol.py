#!/usr/bin/env python3

from os import path
import networkx


def contract(g: networkx.Graph):
    """
    Contract chains of neighboring vertices with degree 2 into a single edge.
    Based on https://stackoverflow.com/questions/68499507/reduce-number-of-nodes-edges-of-a-graph-in-nedworkx
    """

    # create subgraph of all nodes with degree 2
    chain_nodes = [node for node, degree in g.degree() if degree == 2]
    chains = g.subgraph(chain_nodes)

    # contract connected components (which should be chains of variable length) into single node
    components = [
        chains.subgraph(c) for c in networkx.components.connected_components(chains)
    ]

    not_chain = [node for node in g.nodes() if node not in chain_nodes]
    h = g.subgraph(not_chain).copy()

    for component in components:
        end_points = [node for node, degree in component.degree() if degree < 2]
        a = [n for n in g.neighbors(end_points[0]) if n not in component][0]
        b = [n for n in g.neighbors(end_points[1]) if n not in component][0]
        length = sum(
            component.get_edge_data(*edge)["length"] for edge in component.edges()
        )
        length += g.get_edge_data(a, end_points[0])["length"]
        length += g.get_edge_data(b, end_points[1])["length"]
        h.add_edge(a, b, length=length)

    return h


def path_length(g: networkx.Graph, path: list) -> int:
    return sum(g.get_edge_data(*edge)["length"] for edge in zip(path, path[1:]))


def longest_path(g: networkx.Graph, start, end) -> int:
    return max(
        path_length(g, path) for path in networkx.all_simple_paths(g, start, end)
    )


def part1(grid: list[str]) -> networkx.Graph:
    g = networkx.DiGraph()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            match c:
                case "#":
                    continue
                case "^":
                    g.add_edge((x, y), (x, y - 1), length=1)
                case ">":
                    g.add_edge((x, y), (x + 1, y), length=1)
                case "v":
                    g.add_edge((x, y), (x, y + 1), length=1)
                case "<":
                    g.add_edge((x, y), (x - 1, y), length=1)
                case ".":
                    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < len(row)
                            and 0 <= ny < len(grid)
                            and grid[ny][nx] != "#"
                        ):
                            g.add_edge((x, y), (nx, ny), length=1)
                case _:
                    assert False
    return g


def part2(grid: list[str]) -> networkx.Graph:
    g = networkx.Graph()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            match c:
                case "#":
                    continue
                case "." | "v" | "<" | ">" | "^":
                    for dx, dy in [(1, 0), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < len(row)
                            and 0 <= ny < len(grid)
                            and grid[ny][nx] != "#"
                        ):
                            g.add_edge((x, y), (nx, ny), length=1)
                case _:
                    assert False
    return contract(g)


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = file.read().splitlines()
    start = grid[0].index("."), 0
    end = grid[-1].index("."), len(grid) - 1

    print("Part 1:", longest_path(part1(grid), start, end))
    print("Part 2:", longest_path(part2(grid), start, end))
