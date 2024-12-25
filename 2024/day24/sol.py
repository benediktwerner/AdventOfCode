#!/usr/bin/env python3

import re
from functools import cache
from os import path

OUT_BITS = 46


def index(s: str) -> int:
    return int(re.findall(r"\d+", s)[0])


@cache
def get_wire_state(wire: str) -> bool:
    if wire in wire_states:
        return wire_states[wire]

    a, op, b = gates[wire]
    a = get_wire_state(a)
    b = get_wire_state(b)
    match op:
        case "AND":
            return a & b
        case "OR":
            return a | b
        case "XOR":
            return a ^ b
        case _:
            assert False


def is_processed(wire: str) -> bool:
    return is_input(wire) or wire in renamed


def is_input(wire: str) -> bool:
    return wire.startswith("x") or wire.startswith("y")


def swap(a, b):
    tmp = gates[a]
    gates[a] = gates[b]
    gates[b] = tmp
    swapped_gates.extend((a, b))


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    init, connections = file.read().split("\n\n")

    wire_states = {}
    gates = {}
    swapped_gates = []

    for line in init.splitlines():
        wire, state = line.split(": ")
        wire_states[wire] = bool(int(state))

    for line in connections.splitlines():
        a, op, b, _, out = line.split()
        a, b = sorted((a, b))
        gates[out] = (a, op, b)

    result = 0
    for i in range(OUT_BITS):
        name = f"z{i:02}"
        result |= get_wire_state(name) << i
    print("Part 1:", result)

    swap("vmv", "z07")
    swap("kfm", "z20")
    swap("hnv", "z28")
    swap("tqr", "hth")

    print("Part 2:", ",".join(sorted(swapped_gates)))

    renamed = {}
    todo = set(gates)
    for wire in tuple(todo):
        if is_input(wire):
            todo.remove(wire)
        a, op, b = gates[wire]
        if a == "x00" and b == "y00" and op == "AND":
            renamed[wire] = "carry_00"
            todo.remove(wire)

    changed = True
    error = False
    while changed and not error:
        changed = False
        for wire in tuple(todo):
            a, op, b = gates[wire]
            if not is_processed(a) or not is_processed(b):
                continue
            a = renamed.get(a, a)
            b = renamed.get(b, b)
            changed = True
            todo.remove(wire)
            if a.startswith("x") and b.startswith("y"):
                if a[1:] == b[1:]:
                    if op == "XOR":
                        renamed[wire] = "direct_bit_" + a[1:]
                        continue
                    if op == "AND":
                        renamed[wire] = "direct_carry_" + a[1:]
                        continue
            elif op == "AND" and (
                (
                    a.startswith("direct_bit_")
                    and b.startswith("carry_")
                    and index(a) == index(b) + 1
                )
                or (
                    b.startswith("direct_bit_")
                    and a.startswith("carry_")
                    and index(b) == index(a) + 1
                )
            ):
                n = max(index(a), index(b))
                renamed[wire] = "indirect_carry_" + f"{n:02}"
                continue
            elif (
                op == "OR"
                and index(a) == index(b)
                and (
                    (a.startswith("direct_carry_") and b.startswith("indirect_carry_"))
                    or (
                        b.startswith("direct_carry_")
                        and a.startswith("indirect_carry_")
                    )
                )
            ):
                renamed[wire] = f"carry_{index(a):02}"
                continue
            elif (
                wire.startswith("z")
                and op == "XOR"
                and (
                    (
                        a.startswith("direct_bit_")
                        and b.startswith("carry_")
                        and index(wire) == index(a) == index(b) + 1
                    )
                    or (
                        b.startswith("direct_bit_")
                        and a.startswith("carry_")
                        and index(wire) == index(b) == index(a) + 1
                    )
                )
            ):
                continue

            print(f"Error: {wire} = {renamed.get(a, a)} {op} {renamed.get(b, b)}")

    lines = []
    for wire, (a, op, b) in gates.items():
        lines.append(
            f"{renamed.get(wire, wire)} ({wire}) = {renamed.get(a, a)} {op} {renamed.get(b, b)}"
        )

    with open("result.txt", "w") as of:
        for line in sorted(lines):
            print(line, file=of)
