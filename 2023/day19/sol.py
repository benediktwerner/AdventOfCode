#!/usr/bin/env python3

import math
import operator
from copy import deepcopy
from os import path


def part1(rules, parts):
    return sum(sum(part.values()) for part in parts if accepted(rules, part))


def accepted(rules, part):
    rule = "in"
    while True:
        for var, op, val, action in rules[rule]:
            op = {"<": operator.lt, ">": operator.gt}[op]
            if op(part[var], val):
                if action == "A":
                    return True
                if action == "R":
                    return False
                rule = action
                break


def part2(rules):
    todo = [("in", {c: [0, 4001] for c in "xmas"})]
    accepted = 0
    while todo:
        rule, part = todo.pop()
        if rule == "A":
            accepted += math.prod(hi - lo - 1 for lo, hi in part.values())
            continue
        elif rule == "R":
            continue
        rule = rules[rule]
        for var, op, val, action in rule:
            new_part = deepcopy(part)
            if op == ">":
                new_min = max(part[var][0], val)
                if new_min + 1 < part[var][1]:
                    new_part[var][0] = new_min
                    todo.append((action, new_part))
                new_max = min(part[var][1], val + 1)
                if new_max - 1 > part[var][0]:
                    part[var][1] = new_max
                else:
                    break
            elif op == "<":
                new_max = min(part[var][1], val)
                if new_max - 1 > part[var][0]:
                    new_part[var][1] = new_max
                    todo.append((action, new_part))
                new_min = max(part[var][0], val - 1)
                if new_min + 1 < part[var][1]:
                    part[var][0] = new_min
                else:
                    break
            else:
                assert False
    return accepted


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    raw_rules, raw_parts = file.read().split("\n\n")

    rules = {}
    for rule in raw_rules.splitlines():
        name, rule = rule.split("{")
        steps = []
        for step in rule[:-1].split(","):
            if ":" in step:
                cond, action = step.split(":")
                var, op, val = cond[0], cond[1], int(cond[2:])
                steps.append((var, op, val, action))
            else:
                steps.append(("x", ">", 0, step))
        rules[name] = steps

    parts = []
    for part in raw_parts.splitlines():
        parts.append(
            eval(part.replace("{", '{"').replace(",", ',"').replace("=", '":'))
        )

    print("Part 1:", part1(rules, parts))
    print("Part 2:", part2(rules))
