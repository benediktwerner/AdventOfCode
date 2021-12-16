#!/usr/bin/env python3

from os import path
from collections import defaultdict


REG_NAMES = ("a", "b", "c", "d")


def run(instrs, **inits):
    regs = defaultdict(int)
    ip = 0

    for k, v in inits.items():
        regs[k] = v

    while ip < len(instrs):
        instr, *args = instrs[ip]
        if instr == "cpy":
            x, y = args
            if x in REG_NAMES:
                regs[y] = regs[x]
            else:
                regs[y] = int(x)
        elif instr == "inc":
            regs[args[0]] += 1
        elif instr == "dec":
            regs[args[0]] -= 1
        else:
            assert instr == "jnz"
            x, target = args
            val = regs[x] if x in REG_NAMES else int(x)
            if val != 0:
                ip += int(target)
                continue
        ip += 1

    return regs["a"]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    instrs = [line.strip().split() for line in f]
    print("Part 1:", run(instrs))
    print("Part 2:", run(instrs, c=1))
