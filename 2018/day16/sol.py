#!/usr/bin/env python3

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
    ambigous_count = 0
    opcodes = {}
    program = []

    with open("input.txt") as f:
        state = 0
        for line in f:
            line = line.strip()
            if state == 0:
                if not line:
                    state = 10
                    continue

                before = eval(line.split(": ")[1])
            elif state == 1:
                instr, a, b, c = (int(x) for x in line.split(" "))
            elif state == 2:
                after = eval(line.strip().split(": ")[1])
            elif state == 3:
                state = -1
                possible_opcodes = set()

                for fn in FUNCTIONS.values():
                    if fn(before, a, b) == after[c]:
                        possible_opcodes.add(fn)
                        count += 1

                if len(possible_opcodes) >= 3:
                    ambigous_count += 1

                if instr not in opcodes:
                    opcodes[instr] = possible_opcodes
                else:
                    opcodes[instr] &= possible_opcodes
            elif state > 11:
                if not line:
                    break

                program.append(tuple(int(x) for x in line.split(" ")))

            state += 1

    print("Part 1:", ambigous_count)

    opc = {}
    found_ops = set()

    while True:
        changed = False

        for key in opcodes:
            for op in found_ops:
                if op in opcodes[key]:
                    opcodes[key].remove(op)

            if len(opcodes[key]) == 1:
                fn = opcodes[key].pop()
                opc[key] = fn
                found_ops.add(fn)
                changed = True

        if not changed:
            break

    r = [0, 0, 0, 0]

    for i, a, b, c in program:
        r[c] = opc[i](r, a, b)

    print("Part 2:", r[0])


if __name__ == "__main__":
    main()
