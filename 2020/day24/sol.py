#!/usr/bin/env python3

from os import path


DIFF = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "ne": (1, -1),
    "nw": (0, -1),
}

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    black = set()

    for line in f.read().splitlines():
        q, r = 0, 0
        while line:
            for k, (qd, rd) in DIFF.items():
                if line.startswith(k):
                    line = line[len(k) :]
                    q += qd
                    r += rd
        if (q,r) in black:
            black.remove((q,r))
        else:
            black.add((q, r))
    
    print("Part 1:", len(black))

    for _ in range(100):
        new = set()
        todo = set()
        for q, r in black:
            black_count = 0
            for dq, dr in DIFF.values():
                n = q+dq,r+dr
                if n in black:
                    black_count += 1
                else:
                    todo.add(n)
            if 0 < black_count <= 2:
                new.add((q, r))
        for q, r in todo:
            black_count = sum((q+dq,r+dr) in black for dq, dr in DIFF.values())
            if black_count == 2:
                new.add((q, r))
        black = new

    print("Part 2:", len(black))
