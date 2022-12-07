#!/usr/bin/env python3

from os import path
from collections import defaultdict


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    dirs = defaultdict(int)
    ls = False
    for line in f.read().splitlines():
        if line.startswith("$ cd"):
            ls = False
            d = line[5:]
            if d == "/":
                cwd = []
            elif d == "..":
                cwd.pop()
            else:
                cwd.append(d)
        elif line.startswith("$ ls"):
            ls = True
        elif ls:
            try:
                dirs["/".join(cwd)] += int(line.split()[0])
            except ValueError:
                pass

for d in sorted(dirs.keys(), key=lambda x: x.count("/"), reverse=True):
    if d:
        dirs["/".join(d.split("/")[:-1])] += dirs[d]

print("Part 1:", sum(s for s in dirs.values() if s <= 100_000))

free = 70_000_000 - dirs[""]
needed = 30_000_000 - free
print("Part 2:", min(v for v in dirs.values() if v > needed))
