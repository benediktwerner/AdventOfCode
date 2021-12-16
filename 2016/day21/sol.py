#!/usr/bin/env python3

from os import path


def solve(pwd, instrs, reverse):
    rev_rotate = {}
    for i in range(len(pwd)):
        rot = 1 + i + (i >= 4)
        rev_rotate[(i + rot) % len(pwd)] = (-rot) % len(pwd)

    for instr in instrs:
        parts = instr.split()
        if parts[0] == "swap" and parts[1] == "position":
            x, y = int(parts[2]), int(parts[5])
            x, y = min(x, y), max(x, y)
            pwd = pwd[:x] + pwd[y] + pwd[x + 1 : y] + pwd[x] + pwd[y + 1 :]
        elif parts[0] == "swap":
            x, y = parts[2], parts[5]
            pwd = pwd.replace(x, "_").replace(y, x).replace("_", y)
        elif parts[0] == "rotate" and parts[1] == "based":
            x = pwd.index(parts[6])
            if reverse:
                rotate = rev_rotate[x]
            else:
                rotate = (1 + x + (x >= 4)) % len(pwd)
            pwd = pwd[-rotate:] + pwd[:-rotate]
        elif parts[0] == "rotate":
            rotate = int(parts[2]) % len(pwd)
            if (parts[1] == "right") ^ reverse:
                rotate *= -1
            pwd = pwd[rotate:] + pwd[:rotate]
        elif parts[0] == "reverse":
            x, y = int(parts[2]), int(parts[4])
            pwd = pwd[:x] + "".join(reversed(pwd[x : y + 1])) + pwd[y + 1 :]
        elif parts[0] == "move":
            x, y = int(parts[2]), int(parts[5])
            if reverse:
                x, y = y, x
            c = pwd[x]
            pwd = pwd[:x] + pwd[x + 1 :]
            pwd = pwd[:y] + c + pwd[y:]
        else:
            assert False, instr

    return pwd


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    instrs = f.read().splitlines()
    print("Part 1:", solve("abcdefgh", instrs, False))
    print("Part 2:", solve("fbgdceah", reversed(instrs), True))
