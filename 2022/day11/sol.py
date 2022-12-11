#!/usr/bin/env python3

from os import path
from dataclasses import dataclass
import math
import re


@dataclass
class Monkey:
    items: list[int]
    op: str
    div_by: int
    targets: tuple[int, int]


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp, n, div_by_3):
    monkeys: list[Monkey] = []
    for i, monkey in enumerate(inp.split("\n\n")):
        lines = monkey.splitlines()
        monkeys.append(
            Monkey(
                ints(lines[1]),
                lines[2].split(" = ")[1],
                ints(lines[3])[0],
                (ints(lines[5])[0], ints(lines[4])[0]),
            )
        )

    k = math.prod(m.div_by for m in monkeys)
    active = [0] * len(monkeys)
    for _ in range(n):
        for i, m in enumerate(monkeys):
            for it in m.items:
                active[i] += 1
                new = eval(m.op.replace("old", str(it)))
                new = new // 3 if div_by_3 else new % k
                monkeys[m.targets[new % m.div_by == 0]].items.append(new)
            m.items.clear()

    active.sort()
    return active[-1] * active[-2]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.read()
    print("Part 1:", solve(inp, 20, True))
    print("Part 2:", solve(inp, 10000, False))
