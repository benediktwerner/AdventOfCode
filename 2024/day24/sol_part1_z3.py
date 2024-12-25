#!/usr/bin/env python3

from os import path
from z3 import *
from functools import cache

OUT_BITS = 46


def get_var(name: str) -> BitVecRef:
    if name.startswith("x"):
        n = int(name[1:])
        return Extract(n, n, x)
    elif name.startswith("y"):
        n = int(name[1:])
        return Extract(n, n, y)
    elif name.startswith("z"):
        n = int(name[1:])
        return Extract(n, n, z)
    elif name in wires:
        return wires[name]
    else:
        var = BitVec(name, 1)
        wires[name] = var
        return var


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    s = Solver()
    x, y, z = BitVecs("x y z", OUT_BITS)
    wires: dict[str, BitVecRef] = {}

    init, connections = file.read().split("\n\n")

    for line in init.splitlines():
        wire, state = line.split(": ")
        s.add(get_var(wire) == int(state))

    for line in connections.splitlines():
        a, op, b, _, out = line.split()
        a = get_var(a)
        b = get_var(b)
        out = get_var(out)
        match op:
            case "AND":
                s.add(a & b == out)
            case "OR":
                s.add(a | b == out)
            case "XOR":
                s.add(a ^ b == out)

    assert s.check() == sat

    print("Part 1:", s.model()[z].as_long())
