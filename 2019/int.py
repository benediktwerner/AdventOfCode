#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import itertools
import math

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
        self.inputs = deque()
        self.outputs = deque()
        self.halted = False
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
                while not self.inputs:
                    yield
                self[a] = self.inputs.popleft()
            elif op == OUT:
                self.outputs.append(a)
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

        self.halted = True
        yield

    def run(self, *inputs, out=None):
        for inp in inputs:
            if isinstance(inp, str):
                self.inputs.extend(ord(c) for c in inp)
            else:
                self.inputs.append(inp)

        next(self.gen)
        return self.out(out)

    def out(self, n=None, ascii=False):
        if n is None:
            outs = list(self.outputs)
            self.outputs.clear()
        else:
            outs = [self.outputs.popleft() for _ in range(n)]

        return "".join(map(chr, outs)) if ascii else outs


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code = list(map(int, f.readline().strip().split(",")))
    vm = VM(code)
