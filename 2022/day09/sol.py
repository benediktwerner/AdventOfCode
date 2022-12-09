#!/usr/bin/env python3

from os import path


def simulate(moves, length):
    pos = [[0, 0] for _ in range(length)]
    s = set()
    for line in moves:
        d, v = line.split()
        for _ in range(int(v)):
            s.add(tuple(pos[-1]))
            if d == "D":
                pos[0][1] += 1
            elif d == "U":
                pos[0][1] -= 1
            elif d == "L":
                pos[0][0] -= 1
            elif d == "R":
                pos[0][0] += 1
            for i, ((hx, hy), (tx, ty)) in enumerate(zip(pos, pos[1:])):
                if abs(hx - tx) > 1:
                    tx += 1 if hx > tx else -1
                    if abs(hy - ty) > 0:
                        ty += 1 if hy > ty else -1
                elif abs(hy - ty) > 1:
                    ty += 1 if hy > ty else -1
                    if abs(hx - tx) > 0:
                        tx += 1 if hx > tx else -1
                pos[i + 1][0] = tx
                pos[i + 1][1] = ty

    s.add(tuple(pos[-1]))

    return len(s)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.read().splitlines()
    print("Part 1:", simulate(inp, 2))
    print("Part 2:", simulate(inp, 10))
