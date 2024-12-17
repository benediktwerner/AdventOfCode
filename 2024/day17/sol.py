#!/usr/bin/env python3

import re
from os import path

from z3 import BitVec, Solver, sat


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def evaluate(a, b, c, program, part2):
    def combo_operand():
        match literal_operand:
            case 0 | 1 | 2 | 3:
                return literal_operand
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                assert False, f"invalid combo operand: {literal_operand}"

    def int_div(a, b):
        if part2:
            return a / b
        return a // b

    conditions = []
    out = []
    ip = 0
    while 0 <= ip < len(program):
        opcode = program[ip]
        literal_operand = program[ip + 1]

        match opcode:
            case 0:
                a = int_div(a, (1 << combo_operand()))
            case 1:
                b = b ^ literal_operand
            case 2:
                b = combo_operand() % 8
            case 3:
                if part2:
                    # assumes there is only a single looping jnz instruction
                    # and no output after it
                    # => only loop if len(out) < len(program)
                    if len(out) < len(program):
                        conditions.append(a != 0)
                        ip = literal_operand - 2
                    else:
                        conditions.append(a == 0)
                        break
                elif a != 0:
                    ip = literal_operand - 2
            case 4:
                b ^= c
            case 5:
                out.append(combo_operand() % 8)
            case 6:
                b = int_div(a, (1 << combo_operand()))
            case 7:
                c = int_div(a, (1 << combo_operand()))
            case _:
                assert False, f"invalid opcode: {opcode}"

        ip += 2

    return out, conditions


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    lines = file.read().splitlines()
    a, b, c = [int(line.split()[-1]) for line in lines[:3]]
    program = list(map(int, lines[4].split()[-1].split(",")))

    out, _ = evaluate(a, b, c, program, False)
    print("Part 1:", ",".join(map(str, out)))

    a = BitVec("a", 64)
    out, conditions = evaluate(a, b, c, program, True)
    s = Solver()
    s.add(*[o == program[i] for i, o in enumerate(out)])
    s.add(*conditions)

    min_a = float("inf")
    while s.check() == sat:
        curr_a = s.model()[a].as_long()
        min_a = min(min_a, curr_a)
        s.add(a != curr_a)

    print("Part 2:", min_a)
