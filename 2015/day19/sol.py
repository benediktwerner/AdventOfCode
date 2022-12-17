#!/usr/bin/env python3

from os import path
from collections import deque


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    rules, medicine = f.read().strip().split("\n\n")
    rules = [rule.split(" => ") for rule in rules.splitlines()]


def apply_rules(molecule, rules):
    for pattern, to in rules:
        i = 0
        while i <= len(molecule) - len(pattern):
            i = molecule.find(pattern, i)
            if i < 0:
                break
            yield molecule[:i] + to + molecule[i + len(pattern) :]
            i += 1


print("Part 1:", len(set(apply_rules(medicine, rules))))


def solve(rules):
    todo = deque([(medicine, 0)])
    found = set([medicine])
    min_len = len(medicine)
    targets = [to for pat, to in rules if pat == "e"]
    rules = [(b, a) for a, b in rules if a != "e"]

    while todo:
        curr, steps = todo.popleft()
        if len(curr) < min_len:
            min_len = len(curr)
            print(min_len)
        for new in apply_rules(curr, rules):
            if new in targets:
                return steps + 1
            if new not in found:
                found.add(new)
                todo.append((new, steps + 1))


print("Part 2:", solve(rules))
