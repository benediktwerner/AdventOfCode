#!/usr/bin/env python3

from os import path
from networkx import Graph, shortest_path, shortest_path_length, bfs_tree

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
        return self.gen.send(inp)


WALL = 0
EMPTY = 1
OXYGEN = 2

DX = (0, 0, 0, -1, 1)
DY = (0, 1, -1, 0, 0)

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code = list(map(int, f.readline().strip().split(",")))
    vm = VM(code)
    vm.run()

    x, y = 0, 0
    m = {(0, 0): EMPTY}
    g = Graph()
    g.add_node((0, 0))
    todo = [(0, 0, d) for d in (1, 2, 3, 4)]

    while todo:
        tx, ty, d = todo.pop()
        ttx = tx + DX[d]
        tty = ty + DY[d]

        if (ttx, tty) in m:
            if m[(ttx, tty)] != WALL:
                g.add_edge((tx, ty), (ttx, tty))
            continue

        if x != tx or y != ty:
            for tx, ty in shortest_path(g, (x, y), (tx, ty))[1:]:
                assert abs(x - tx) + abs(y - ty) == 1
                if ty > y:
                    r, = vm.run(1)
                elif ty < y:
                    r, = vm.run(2)
                elif tx < x:
                    r, = vm.run(3)
                elif tx > x:
                    r, = vm.run(4)
                else:
                    assert False
                assert r == m[(tx, ty)]
                x, y = tx, ty

        r, = vm.run(d)
        m[(ttx, tty)] = r

        if r != WALL:
            x, y = ttx, tty

            g.add_node((x, y))
            g.add_edge((tx, ty), (x, y))

            for td in (1, 2, 3, 4):
                if (0, 2, 1, 4, 3)[td] == d:
                    continue
                todo.append((x, y, td))

            if r == OXYGEN:
                oxygen = (x, y)

    print("Part 1:", shortest_path_length(g, (0, 0), oxygen))

    furthest = list(bfs_tree(g, oxygen))[-1]
    print("Part 2:", shortest_path_length(g, oxygen, furthest))
