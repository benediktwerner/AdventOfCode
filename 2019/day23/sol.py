#!/usr/bin/env python3

from os import path
from collections import deque
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
    def __init__(self, code, i):
        self.mem = list(code)
        self.ip = 0
        self.relative_base = 0
        self.inputs = deque([i])
        self.outputs = deque()
        self.idle_count = 0

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

    def step(self):
        assert self[self.ip] != HALT

        instr = self[self.ip]
        op = instr % 100
        modes = instr // 100

        if op not in OPS:
            raise Exception(f"Unknown opcode: {op}")

        arg_kinds = OPS[op]
        a, b, c, d = self.get_args(arg_kinds, modes)
        self.ip += 1 + len(arg_kinds)

        if op == IN:
            if self.inputs:
                self[a] = self.inputs.popleft()
                self.idle_count = 0
            else:
                self[a] = -1
                self.idle_count += 1
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


def part1(code):
    vms = [VM(code, i) for i in range(50)]

    while True:
        for vm in vms:
            vm.step()

            if len(vm.outputs) >= 3:
                addr = vm.outputs.popleft()
                x = vm.outputs.popleft()
                y = vm.outputs.popleft()

                if addr == 255:
                    return y
                else:
                    vms[addr].inputs.append(x)
                    vms[addr].inputs.append(y)


def part2(code):
    vms = [VM(code, i) for i in range(50)]
    lasty = None

    while True:
        idle = True

        for vm in vms:
            vm.step()

            if len(vm.outputs) >= 3:
                addr = vm.outputs.popleft()
                x = vm.outputs.popleft()
                y = vm.outputs.popleft()

                if addr == 255:
                    natx, naty = x, y
                else:
                    vms[addr].inputs.append(x)
                    vms[addr].inputs.append(y)

            if vm.inputs or vm.outputs or vm.idle_count < 10:
                idle = False

        if idle:
            if naty == lasty:
                return lasty

            vms[0].inputs.append(natx)
            vms[0].inputs.append(naty)
            lasty = naty


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code = list(map(int, f.readline().strip().split(",")))

    print("Part 1:", part1(code))
    print("Part 2:", part2(code))
