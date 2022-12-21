#!/usr/bin/env python3

from os import path
from z3 import Solver, Int, ArithRef, sat


def evaluate(curr):
    if isinstance(curr, ArithRef):
        return curr

    try:
        return int(curr)
    except:
        a, op, b = curr.split(" ")
        a = evaluate(monkeys[a])
        b = evaluate(monkeys[b])
        if op == "*":
            return a * b
        if op == "/":
            if isinstance(a, int) and isinstance(b, int):
                return a // b
            return a / b
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "=":
            return a == b

    assert False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    monkeys = [line.split(": ") for line in f.read().splitlines()]
    monkeys = {name: equation for name, equation in monkeys}

    print("Part 1:", evaluate(monkeys["root"]))

    s = Solver()
    monkeys["humn"] = Int("humn")
    s.add(evaluate(monkeys["root"].replace("+", "=")))
    assert s.check() == sat
    model = s.model()
    print("Part 2:", model[monkeys["humn"]].as_long())
