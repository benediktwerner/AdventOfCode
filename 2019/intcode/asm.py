#!/usr/bin/env python3

from os import path
from sys import argv, stderr
from collections import defaultdict


READ = 0
WRITE = 1

OPS = {
    "add": (1, (READ, READ, WRITE)),
    "mul": (2, (READ, READ, WRITE)),
    "in": (3, (WRITE,)),
    "out": (4, (READ,)),
    "jnz": (5, (READ, READ)),
    "jz": (6, (READ, READ)),
    "lt": (7, (READ, READ, WRITE)),
    "eq": (8, (READ, READ, WRITE)),
    "hlt": (99, ()),
}

PREPROCESS_RULES = {
    "halt": ((), ["hlt"]),
    "jtrue": ((READ, READ), ["jnz $0 $1"]),
    "jfalse": ((READ, READ), ["jz $0 $1"]),
    "mov": ((READ, WRITE), ["add 0 $0 $1"]),
    "sub": ((READ, READ, WRITE), ["mul -1 $1 __tmp", "add $0 __tmp $2"]),
    "div": ((READ, READ, WRITE), ["divmod $0 $1 $2 __rest"]),
    "mod": (
        (READ, READ, WRITE),
        [
            "mov $1 __div",
            "mov $0 $2",
            "__loop$:",
            "lt $2 __div __tmp",
            "jtrue __tmp :__end$",
            "sub $2 __div $2",
            "jmp :__loop$",
            "__end$:",
        ],
    ),
    "divmod": (
        (READ, READ, WRITE, WRITE),
        [
            "mov $1 __div",
            "mov $0 $3",
            "mov 0 $2",
            "__loop$:",
            "lt $3 __div __tmp",
            "jtrue __tmp :__end$",
            "sub $3 __div $3",
            "add $2 1 $2",
            "jmp :__loop$",
            "__end$:",
        ],
    ),
    "jmp": ((READ,), ["add 0 0 __tmp", "jz __tmp $0"]),
    "and": (
        (READ, READ, WRITE),
        [
            "jz $0 :__first$",
            "mov $1 $2",
            "jmp :__end$",
            "__first$:",
            "mov $0 $2",
            "__end$:",
        ],
    ),
    "or": (
        (READ, READ, WRITE),
        [
            "jnz $0 :__first$",
            "mov $1 $2",
            "jmp :__end$",
            "__first$:",
            "mov $0 $2",
            "__end$:",
        ],
    ),
    "not": (
        (READ, WRITE),
        [
            "jz $0 :__false$",
            "mov $1 1",
            "jmp :__end$",
            "__false$:",
            "mov $1 0",
            "__end$:",
        ],
    ),
    "leq": ((READ, READ, WRITE), ["lt $0 $1 __tmp", "eq $0 $1 $2", "or __tmp $2 $2"]),
    "gt": ((READ, READ, WRITE), ["lt $1 $0 $2"]),
    "geq": ((READ, READ, WRITE), ["leq $1 $0 $2"]),
}


def eprint(*args, **kwargs):
    print(*args, **kwargs, file=stderr)


def warn(i, line, msg):
    eprint(f"Warning at line {i}:", msg)
    eprint(" " * 5, "|")
    eprint(f"{i:5} |   ", line.strip())
    eprint(" " * 5, "|")


def error(i, line, msg):
    eprint(f"Error at line {i}:", msg)
    eprint(" " * 5, "|")
    eprint(f"{i:5} |   ", line.strip())
    eprint(" " * 5, "|")
    exit(3)


preprocess_tmp_suffix = 0


def preprocess(f):
    for i, line in enumerate(f):
        if "#" in line:
            line = line[: line.find("#")]

        yield from __preprocess(i, line, line)


def __preprocess(i, line, pline):
    global preprocess_tmp_suffix

    parts = pline.split()
    if not parts:
        return

    if parts[0] in PREPROCESS_RULES:
        rule = PREPROCESS_RULES[parts[0]]
        if len(parts[1:]) != len(rule[0]):
            error(
                i, line, f"Macro expected {len(rule[0])} args but got {len(parts[1:])}"
            )
        for sub in PREPROCESS_RULES[parts[0]][1]:
            for a in set(c for c in sub.split() if c[0] == "$"):
                sub = sub.replace(a, parts[int(a[1:]) + 1])
            if "$" in sub:
                sub.replace("$", str(preprocess_tmp_suffix))
                preprocess_tmp_suffix += 1
            yield from __preprocess(i, line, sub)
    else:
        yield i, line, parts


if len(argv) != 2 or "-h" in argv[1:] or "--help" in argv[1:]:
    eprint("Usage:", argv[0], "FILE")
    exit(1)
elif not path.isfile(argv[1]):
    eprint(f"File '{argv[1]}' not found")
    eprint("Usage:", argv[0], "FILE")
    exit(2)


labels = {}
patches = defaultdict(list)
patch_lines = defaultdict(list)
written_to = set()
read_from = set()
values = {}
code = []
has_hlt = False

with open(argv[1]) as f:
    for i, line, parts in preprocess(f):
        if parts[0][-1] == ":":
            if len(parts) > 1:
                error(i, line, "Unexpected input after label")
            labels[":" + parts[0][:-1]] = len(code)
        elif parts[0] in OPS:
            opcode, arg_kinds = OPS[parts[0]]
            mode = 0
            args = []

            if opcode == 99:
                has_hlt = True

            if len(parts[1:]) != len(arg_kinds):
                error(
                    i,
                    line,
                    f"Expected {len(arg_kinds)} arguments but found {len(parts[1:])}",
                )
            for i, (arg, kind) in enumerate(zip(parts[1:], arg_kinds)):
                if arg[0] == ":":
                    patches[arg].append(len(code) + 1 + i)
                    patch_lines[arg].append((i, line))
                    mode += 10 ** (i + 2)
                else:
                    try:
                        arg = int(arg, 0)
                        mode += 10 ** (i + 2)
                    except ValueError:
                        patches[arg].append(len(code) + 1 + i)
                        patch_lines[arg].append((i, line))
                        if kind == READ:
                            read_from.add(arg)
                        else:
                            written_to.add(arg)
                args.append(arg)
            code.append(opcode + mode)
            code.extend(args)
        elif len(parts) == 3 and parts[1] == "=":
            if parts[0] in values:
                error(i, line, f"'{parts[0]}' was already defined")
            try:
                values[parts[0]] = int(parts[2], 0)
            except ValueError:
                error(i, line, f"Failed to parse '{parts[1]}' as an int")
        else:
            error(i, line, f"Unknown opcode: {parts[0]}")


for k, locs in patches.items():
    if k[0] == ":" and k not in labels:
        for i, line in patch_lines[k]:
            error(i, line, f"Unknown label: {k[1:]}")

    val = labels.get(k, len(code))
    for loc in locs:
        code[loc] = val

    if k not in labels:
        if k not in values and k not in written_to:
            for i, line in patch_lines[k]:
                warn(i, line, f"Variable {k} is never initialized explicitly")
        elif k not in read_from:
            for i, line in patch_lines[k]:
                warn(i, line, f"Variable {k} is never read")
        code.append(values.get(k, 0))


eprint("Assembled successfully!")

if not has_hlt:
    eprint("Warning: The programs has no 'hlt' instruction!")

print(*code, sep=",")
