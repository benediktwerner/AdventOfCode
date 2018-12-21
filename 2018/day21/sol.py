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

    r = [0] * 6
    found = set()
    last = None
    ip = 0

    while 0 <= ip < len(program):
        if ip == 28:
            if last is None:
                print("Part 1:", r[3])

            if r[3] in found:
                print("Part 2:", last)
                return

            last = r[3]
            found.add(last)

        instr, a, b, c = program[ip]
        r[ip_reg] = ip
        r[c] = FUNCTIONS[instr](r, a, b)
        ip = r[ip_reg] + 1


if __name__ == "__main__":
    main()
