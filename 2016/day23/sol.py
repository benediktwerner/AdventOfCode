#!/usr/bin/env python3

from os import path
from collections import defaultdict


REG_NAMES = ("a", "b", "c", "d")


def run(instrs, **inits):
    instrs = [[instr, args] for instr, *args in instrs]
    regs = defaultdict(int)
    ip = 0

    for k, v in inits.items():
        regs[k] = v

    while ip < len(instrs):
        instr, args = instrs[ip]
        # print(ip, instr, args, regs)
        if instr == "cpy":
            x, y = args
            if y in REG_NAMES:
                if x in REG_NAMES:
                    regs[y] = regs[x]
                else:
                    regs[y] = int(x)
        elif instr == "inc":
            regs[args[0]] += 1
        elif instr == "dec":
            regs[args[0]] -= 1
        elif instr == "tgl":
            assert args[0] in REG_NAMES
            target = ip + regs[args[0]]
            if 0 <= target < len(instrs):
                instrs[target][0] = {
                    "inc": "dec",
                    "dec": "inc",
                    "tgl": "inc",
                    "cpy": "jnz",
                    "jnz": "cpy",
                }[instrs[target][0]]
        elif instr == "jnz":
            x, target = args
            val = regs[x] if x in REG_NAMES else int(x)
            if val != 0:
                ip += regs[target] if target in REG_NAMES else int(target)
                continue
        elif instr == "mul":
            x, y, z = args
            regs[z] = regs[x] * regs[y]
            regs[x] = 0
            regs[y] = 0
        else:
            assert instr == "nop"
        ip += 1

    return regs["a"]


with open(path.join(path.dirname(__file__), "input_opt.txt")) as f:
    instrs = [line.strip().split() for line in f]
    print("Part 1:", run(instrs, a=7))
    print("Part 2:", run(instrs, a=12))
