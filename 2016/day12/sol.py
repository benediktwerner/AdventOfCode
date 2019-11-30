#!/usr/bin/env python3

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
            if y == "1":
                print("2")
            if x in REG_NAMES:
                regs[y] = regs[x]
            else:
                regs[y] = int(x)
        elif instr == "inc":
            if args[0] == "1":
                print("2")
            regs[args[0]] += 1
        elif instr == "dec":
            if args[0] == "1":
                print("3")
            regs[args[0]] -= 1
        else:
            x, target = args
            val = regs[x] if x in REG_NAMES else int(x)
            if val != 0:
                ip += int(target)
                continue
        ip += 1

    return regs["a"]


def main():
    with open(__file__.rstrip("sol.py") + "input.txt") as f:
        instrs = [line.strip.split() for line in f]

        print("Part 1:", run(instrs))

        print("Part 2:", run(instrs, c=1))


if __name__ == "__main__":
    main()
