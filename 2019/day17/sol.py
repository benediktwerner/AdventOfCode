#!/usr/bin/env python3

from os import path
from collections import defaultdict
import re

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADD_RELATIVE_BASE = 9
HALT = 99

READ = 0
WRITE = 1

OPS = {
    ADD: (READ, READ, WRITE),
    MUL: (READ, READ, WRITE),
    IN: (WRITE,),
    OUT: (READ,),
    JUMP_TRUE: (READ, READ),
    JUMP_FALSE: (READ, READ),
    LESS_THAN: (READ, READ, WRITE),
    EQUALS: (READ, READ, WRITE),
    ADD_RELATIVE_BASE: (READ,),
    HALT: (),
}


class VM:
    def __init__(self, code):
        self.mem = list(code)
        self.ip = 0
        self.relative_base = 0
        self.gen = self.__run()

    def __getitem__(self, index):
        return self.mem[index]

    def __setitem__(self, index, val):
        self.mem[index] = val

    def get_args(self, arg_kinds, modes):
        args = [None] * 4

        for i, kind in enumerate(arg_kinds):
            a = self[self.ip + 1 + i]
            mode = modes % 10
            modes //= 10

            if mode == RELATIVE:
                a += self.relative_base

            if mode in (POSITION, RELATIVE):
                if a < 0:
                    raise Exception(f"Invalid access to negative memory index: {a}")
                elif a >= len(self.mem):
                    self.mem += [0] * (a + 1 - len(self.mem))

                if kind == READ:
                    a = self[a]
                elif kind != WRITE:
                    raise Exception(f"Invalid arg kind: {kind}")

            elif mode == IMMEDIATE:
                if kind == WRITE:
                    raise Exception(f"Invalid arg mode for write arg: {mode}")
            else:
                raise Exception(f"Invalid arg mode: {mode}")

            args[i] = a

        return args

    def __run(self):
        out = []

        while self[self.ip] != HALT:
            instr = self[self.ip]
            op = instr % 100
            modes = instr // 100

            if op not in OPS:
                raise Exception(f"Unknown opcode: {op}")

            arg_kinds = OPS[op]
            a, b, c, d = self.get_args(arg_kinds, modes)
            self.ip += 1 + len(arg_kinds)

            if op == IN:
                self[a] = (yield out)
                out.clear()
            elif op == OUT:
                out.append(a)
            elif op == ADD:
                self[c] = a + b
            elif op == MUL:
                self[c] = a * b
            elif op == LESS_THAN:
                self[c] = 1 if a < b else 0
            elif op == EQUALS:
                self[c] = 1 if a == b else 0
            elif op == JUMP_TRUE:
                if a != 0:
                    self.ip = b
            elif op == JUMP_FALSE:
                if a == 0:
                    self.ip = b
            elif op == ADD_RELATIVE_BASE:
                self.relative_base += a
            else:
                raise Exception(f"Unimplemented opcode: {op}")

        return out

    def run(self, inp=None):
        try:
            return self.gen.send(inp)
        except StopIteration as e:
            return e.value
    

NEWLINE = ord("\n")
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code = list(map(int, f.readline().strip().split(",")))
    code[0] = 2
    vm = VM(code)
    m = defaultdict(int)

    x, y = 0, 0
    for c in vm.run():
        if c == NEWLINE:
            x = 0
            y += 1
        else:
            c = chr(c)
            m[(x, y)] = c
            if c in ("v", "^", "<", ">"):
                robot = (x, y)
            x += 1

    total = 0

    for x, y in [k for (k, v) in m.items() if v == "#"]:
        a = m[(x + 1, y)] == "#"
        b = m[(x - 1, y)] == "#"
        c = m[(x, y + 1)] == "#"
        d = m[(x, y - 1)] == "#"

        if a + b + c + d >= 3:
            total += x * y

    print("Part 1:", total)

    x, y = robot
    d = ("^", ">", "v", "<").index(m[robot])
    commands = []

    while True:
        nx = x + DX[d]
        ny = y + DY[d]
        if m[(nx, ny)] == "#":
            if commands and commands[-1] not in ("R", "L"):
                commands[-1] += 1
            else:
                commands.append(1)
            x, y = nx, ny
            continue

        d = (d + 1) % 4
        if m[(x + DX[d], y + DY[d])] == "#":
            commands.append("R")
            continue

        d = (d + 2) % 4
        if m[(x + DX[d], y + DY[d])] == "#":
            commands.append("L")
            continue

        break

    commands = ",".join(map(str, commands)) + ","
    match = re.match(r"^(.{1,21})\1*(.{1,21})(?:\1|\2)*(.{1,21})(?:\1|\2|\3)*$", commands)
    fa = match.group(1)
    fb = match.group(2)
    fc = match.group(3)
    funcs = []
    while commands:
        if commands.startswith(fa):
            funcs.append("A")
            commands = commands[len(fa):]
        elif commands.startswith(fb):
            funcs.append("B")
            commands = commands[len(fb):]
        elif commands.startswith(fc):
            funcs.append("C")
            commands = commands[len(fc):]
        else:
            assert False

    for c in ",".join(funcs):
        vm.run(ord(c))
    vm.run(NEWLINE)

    for c in fa[:-1]:
        vm.run(ord(c))
    vm.run(NEWLINE)

    for c in fb[:-1]:
        vm.run(ord(c))
    vm.run(NEWLINE)

    for c in fc[:-1]:
        vm.run(ord(c))
    vm.run(NEWLINE)

    vm.run(ord("n"))
    out = vm.run(NEWLINE)[-1]

    print("Part 2:", out)
