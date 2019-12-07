#!/usr/bin/env python3

import os
import itertools
from collections import defaultdict, deque


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
    def __init__(self, code, inp=None):
        self.mem = list(code)
        self.inp = deque([] if inp is None else inp)
        self.out = []

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
    
    def push_in(self, inp):
        self.inp.extend(inp)
    
    def pop_out(self):
        out = self.out
        self.out = []
        return out

    def run(self):
        self.ip = 0

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
                while not self.inp:
                    yield
                self[a] = self.inp.popleft()
            elif op == OUT:
                self.out.append(a)
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


class Scheduler:
    OUT = object()

    def __init__(self, vms):
        self.vms = vms
        self.connections = [[] for _ in vms]
        self.waiting = deque(range(len(self.vms)))
        self.gens = [vm.run() for vm in self.vms]
        self.out = []
    
    def connect(self, start, end):
        self.connections[start].append(end)

    def run(self):
        while self.waiting:
            curr = self.waiting.popleft()

            try:
                next(self.gens[curr])
                self.waiting.append(curr)
            except StopIteration:
                pass

            out = self.vms[curr].pop_out()
            for conn in self.connections[curr]:
                if conn is Scheduler.OUT:
                    self.out.extend(out)
                else:
                    self.vms[conn].push_in(out)
        
        return self.out


    
with open(os.path.dirname(__file__) + "/input.txt") as f:
    code = list(map(int, f.readline().strip().split(",")))

    result = float("-inf")

    for perm in itertools.permutations(range(5)):
        vms = [VM(code, [p]) for p in perm]
        vms[0].push_in([0])

        sched = Scheduler(vms)
        for i in range(4):
            sched.connect(i, i+1)
        sched.connect(4, Scheduler.OUT)

        out = sched.run()
        result = max(result, out[-1])
    
    print("Part 1:", result)

    result = float("-inf")

    for perm in itertools.permutations(range(5, 10)):
        vms = [VM(code, [p]) for p in perm]
        vms[0].push_in([0])

        sched = Scheduler(vms)
        for i in range(4):
            sched.connect(i, i+1)
        sched.connect(4, 0)
        sched.connect(4, Scheduler.OUT)

        out = sched.run()
        result = max(result, out[-1])
    
    print("Part 2:", result)
