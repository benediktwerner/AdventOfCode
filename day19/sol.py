#!/usr/bin/env python3

from collections import defaultdict


FUNCTIONS = {
    "addr": lambda r, a, b: r[a]+r[b],
    "addi": lambda r, a, b: r[a]+b,
    "mulr": lambda r, a, b: r[a]*r[b],
    "muli": lambda r, a, b: r[a]*b,
    "banr": lambda r, a, b: r[a] & r[b],
    "bani": lambda r, a, b: r[a] & b,
    "borr": lambda r, a, b: r[a] | r[b],
    "bori": lambda r, a, b: r[a] | b,
    "setr": lambda r, a, b: r[a],
    "seti": lambda r, a, b: a,
    "gtir": lambda r, a, b: 1 if a > r[b] else 0,
    "gtri": lambda r, a, b: 1 if r[a] > b else 0,
    "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,
    "eqir": lambda r, a, b: 1 if a == r[b] else 0,
    "eqri": lambda r, a, b: 1 if r[a] == b else 0,
    "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0,
}


def simulate(program, ip_reg, r, break_on=None):
    ip = 0
    while 0 <= ip < len(program):
        if ip == break_on:
            break
        instr, a, b, c = program[ip]
        r[ip_reg] = ip
        r[c] = FUNCTIONS[instr](r, a, b)
        ip = r[ip_reg] + 1
    return r


def main():
    ip_reg = 0
    program = []
    with open("input.txt") as f:
        for line in f:
            if line[0] == "#":
                ip_reg = int(line.strip().split(" ")[1])
            else:
                instr, a, b, c = line.strip().split(" ")
                program.append((instr, int(a), int(b), int(c)))

    r = simulate(program, ip_reg, [0]*6)
    print("Part 1:", r[0])

    r = simulate(program, ip_reg, [1] + [0]*5, break_on=1)
    number = max(r)
    total = 0

    for x in range(1, number+1):
        if number % x == 0:
            total += x

    print("Part 2:", total)

# Decompiled input (regs 0-6 => a-f):
# b = 10551300 if a == 1 else 900
# a = 0
# for f in range(1, b+1):
#   for e in range(1, b+1):
#       c = e * f
#       if c == b:
#           a += f
# Result in a


if __name__ == "__main__":
    main()
