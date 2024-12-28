#!/usr/bin/env python3

from os import path
from z3 import *


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


def get_dependencies(wire: str) -> set[str]:
    if wire.startswith("x") or wire.startswith("y"):
        return set()
    a, _, b = gates[wire]
    return get_dependencies(a) | get_dependencies(b) | {wire}


def setup_solver():
    solver = Solver()
    solver.add(ULT(x, 1 << (output_bits - 1)))
    solver.add(ULT(y, 1 << (output_bits - 1)))
    for out, (a, op, b) in gates.items():
        a = get_var(a)
        b = get_var(b)
        out = get_var(out)
        match op:
            case "AND":
                solver.add(a & b == out)
            case "OR":
                solver.add(a | b == out)
            case "XOR":
                solver.add(a ^ b == out)
    return solver


def swap(a, b):
    tmp = gates[a]
    gates[a] = gates[b]
    gates[b] = tmp


def determine_swap(i: int) -> tuple[str, str]:
    good = get_dependencies(f"z{i - 1:02}")
    bad = get_dependencies(f"z{i:02}") - good

    for a in bad:
        for b in set(gates) - good:
            if b in bad and b <= a:
                continue

            swap(a, b)
            solver = setup_solver()
            solver.add(Extract(i, i, x + y) != Extract(i, i, z))
            if solver.check() == unsat:
                return a, b
            swap(a, b)

    assert False, f"failed to find swap to fix {i}"


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    init, connections = file.read().split("\n\n")

    output_bits = 0
    gates = {}

    for line in connections.splitlines():
        a, op, b, _, out = line.split()
        a, b = sorted((a, b))
        gates[out] = (a, op, b)
        if out.startswith("z"):
            output_bits = max(output_bits, int(out[1:]) + 1)

    wires: dict[str, BitVecRef] = {}
    x, y, z = BitVecs("x y z", output_bits)

    solver = setup_solver()

    for line in init.splitlines():
        wire, state = line.split(": ")
        solver.add(get_var(wire) == int(state))

    assert solver.check() == sat

    print("Part 1:", solver.model()[z].as_long())

    swaps = []

    for i in range(output_bits):
        solver = setup_solver()
        solver.add(Extract(i, i, x + y) != Extract(i, i, z))
        if solver.check() == sat:
            swaps.extend(determine_swap(i))

    print("Part 2:", ",".join(sorted(swaps)))
