#!/usr/bin/env python3

from os import path


OPS = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "LSHIFT": lambda a, b: (a << b) & 0xffff,
    "RSHIFT": lambda a, b: (a >> b) & 0xffff,
}

def solve(wire):
    if wire in cache:
        return cache[wire]

    try:
        return int(wire)
    except ValueError:
        pass

    inp = lines[wire]

    if len(inp) == 1:
        res = solve(inp[0])
    elif len(inp) == 2:
        res = (~solve(inp[1])) & 0xffff
    else:
        left, op, right = inp
        res = OPS[op](solve(left), solve(right))
    
    cache[wire] = res
    return res


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = {}

    for line in f:
        a, b = line.strip().split(" -> ")
        lines[b] = a.split()

    cache = {}
    part1 = solve("a")
    print("Part 1:", part1)

    cache = {"b": part1}
    print("Part 2:", solve("a"))
