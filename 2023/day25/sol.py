#!/usr/bin/env python3

from os import path
from collections import *

import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import itertools
import math
import re
import pyperclip


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp: str):
    graph = defaultdict(set)
    G = nx.Graph()
    for line in inp.splitlines():
        start, ends = line.split(": ")
        ends = ends.split()
        for end in ends:
            graph[start].add(end)
            graph[end].add(start)
            G.add_edge(start, end)
    G.remove_edge("pmn", "kdc")
    G.remove_edge("hvm", "grd")
    G.remove_edge("zfk", "jmn")
    return math.prod(map(len, nx.connected_components(G)))
    # pos = nx.spring_layout(G)
    # nx.draw_networkx(G)
    # plt.show()


example = """\

"""

if example and not example.isspace():
    print("Example:", solve(example))
else:
    print("No example provided")

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    result = solve(file.read())
    print("Output:", result)
    pyperclip.copy(str(result))
    print("Copied to clipboard")
