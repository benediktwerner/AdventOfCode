#!/usr/bin/env python3

from os import path
from sys import argv


POSITION = 0
IMMEDIATE = 1

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
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
    HALT: (),
}


class VM:
    def __init__(self, code):
        self.code = list(code)

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

            if kind == READ:
                if mode == POSITION:
                    a = self[a]
            elif kind == WRITE:
                if mode != POSITION:
                    raise Exception(f"Invalid arg mode for write arg: {mode}")
            else:
                raise Exception(f"Invalid arg kind: {kind}")

            args[i] = a

        return args

    def run(self):
        self.ip = 0
        self.mem = self.code.copy()

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
                self[a] = int(input("Input: "))
            elif op == OUT:
                print("Output:", a)
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
            else:
                raise Exception(f"Unimplemented opcode: {op}")


if len(argv) != 2 or "-h" in argv[1:] or "--help" in argv[1:]:
    print("Usage:", argv[0], "FILE")
    exit(1)
elif not path.isfile(argv[1]):
    print(f"File '{argv[1]}' not found")
    print("Usage:", argv[0], "FILE")
    exit(2)

with open(argv[1]) as f:
    code = list(map(int, f.readline().strip().split(",")))
    VM(code).run()
