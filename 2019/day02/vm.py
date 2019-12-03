#!/usr/bin/env python3

import operator as ops

OP_LEN = {
    1: 4,
    2: 4,
}

UN_OPS = {
}

BIN_OPS = {
    1: ops.add,
    2: ops.mul,
}

def run(code, noun, verb):
    ip = 0
    mem = list(code)
    mem[1] = noun
    mem[2] = verb

    while mem[ip] != 99:
        op = mem[ip]

        if op not in OP_LEN:
            raise Exception(f"Unknown opcode: {op}")

        op_len = OP_LEN[op]
        args = mem[ip + 1 : ip + op_len]
        ip += op_len

        if op in UN_OPS:
            a, b = args
            mem[b] = UN_OPS[op](mem[a])
        elif op in BIN_OPS:
            a, b, c = args
            mem[c] = BIN_OPS[op](mem[a], mem[b])
        else:
            raise Exception(f"Unimplemented opcode: {op}")

    return mem[0]


def main():
    with open(__file__.rstrip("vm.py") + "input.txt") as f:
        code = list(map(int, f.readline().strip().split(",")))

        print(run(code, 12, 2))


if __name__ == "__main__":
    main()
