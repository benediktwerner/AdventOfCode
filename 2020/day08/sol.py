#!/usr/bin/env python3

from os import path


NOP, JMP, ACC = range(3)


def run(code):
    visited = set()
    ip = acc = 0

    while ip not in visited and ip < len(code):
        visited.add(ip)
        op, arg = code[ip]

        if op == JMP:
            ip += arg
        else:
            if op == ACC:
                acc += arg
            ip += 1

    return ip >= len(code), acc


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code = []
    for line in f:
        op, arg = line.split()
        code.append([["nop", "jmp", "acc"].index(op), int(arg)])

    print("Part 1:", run(code)[1])

    for i, (op, arg) in enumerate(code):
        if op != ACC:
            code[i][0] = 1 - op

            terminates, acc = run(code)
            if terminates:
                print("Part 2:", acc)
                break

            code[i][0] = op
