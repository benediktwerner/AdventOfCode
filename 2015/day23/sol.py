#!/usr/bin/env python3

from os import path


def solve(instrs, a):
    regs = {"a":a, "b":0}
    ip = 0
    while 0 <= ip < len(instrs):
        instr, args = instrs[ip].split(maxsplit=1)
        args = args.split(", ")
        ip += 1
        match (instr, *args):
            case ("hlf", r):
                regs[r] //= 2
            case ("tpl", r):
                regs[r] *= 3
            case ("inc", r):
                regs[r] += 1
            case ("jmp", off):
                ip += int(off) - 1
            case ("jie", r, off):
                if regs[r] % 2 == 0:
                    ip += int(off) - 1
            case ("jio", r, off):
                if regs[r] == 1:
                    ip += int(off) - 1
            case _:
                assert False, f"illegal instruction: {instrs[ip]}"
    return regs["b"]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    instrs = f.read().splitlines()
    print("Part 1:", solve(instrs, 0))
    print("Part 2:", solve(instrs, 1))
