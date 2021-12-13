#!/usr/bin/env python3

from os import path


def play(inp, iters):
    # cups[x] is the cup following the cup with value x
    cups = [0] * (max(inp) + 1)
    for a, b in zip(inp, inp[1:] + inp[:1]):
        cups[a] = b

    mod = max(inp)
    curr = inp[0]

    for _ in range(iters):
        a = cups[curr]
        b = cups[a]
        c = cups[b]
        dest = (curr - 2) % mod + 1
        while dest in (a, b, c):
            dest = (dest - 2) % mod + 1
        last = cups[dest]
        cups[dest] = a
        cups[curr] = cups[c]
        curr = cups[curr]
        cups[c] = last

    return cups


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    cups = list(map(int, f.read().strip()))

    p1 = play(cups, 100)
    curr = p1[1]
    out = ""
    while curr != 1:
        out += str(curr)
        curr = p1[curr]
    print("Part 1:", out)

    cups.extend(range(10, 1_000_001))
    p2 = play(cups, 10_000_000)
    print("Part 2:", p2[1] * p2[p2[1]])
