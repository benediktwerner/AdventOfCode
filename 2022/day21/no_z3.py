#!/usr/bin/env python3

from os import path


def evaluate(curr):
    if curr == "humn":
        return curr

    try:
        return int(curr)
    except:
        a, op, b = curr.split(" ")
        a = evaluate(monkeys[a])
        b = evaluate(monkeys[b])
        if not isinstance(a, int) or not isinstance(b, int):
            return (a, op, b)
        if op == "*":
            return a * b
        if op == "/":
            return a // b
        if op == "+":
            return a + b
        if op == "-":
            return a - b

    assert False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    monkeys = [line.split(": ") for line in f.read().splitlines()]
    monkeys = {name: equation for name, equation in monkeys}

    monkeys["humn"] = "humn"
    a, op, b = evaluate(monkeys["root"])
    humn, other = (b, a) if isinstance(a, int) else (a, b)
    while humn != "humn":
        a, op, b = humn
        humn, other2 = (b, a) if isinstance(a, int) else (a, b)
        if op == "*":
            other //= other2
        elif op == "+":
            other -= other2
        elif op == "-":
            if a == humn:
                other += other2
            else:
                other = other2 - other
        elif op == "/":
            if a == humn:
                other *= other2
            else:
                other = other2 // other
    print(other)
