#!/usr/bin/env python3

from os import path
import re


def build_re(rule):
    if "|" in rule:
        parts = rule.split(" | ")
        return "(?:" + "|".join(f"(?:{build_re(x)})" for x in parts) + ")"
    if rule[0] == '"':
        return rule[1]
    if rule[-1] == "+":
        return build_re(rules[rule[:-1]]) + "+"
    return "".join(build_re(rules[r]) for r in rule.split())


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = (line.strip() for line in f)
    rules = {}
    for line in lines:
        if not line:
            break
        num, rule = line.split(": ")
        rules[num] = rule

    regex1 = build_re(rules["0"])

    # rules["8"] = "42 | 42 8"
    # rules["11"] = "42 31 | 42 11 31"

    rules["8"] = "42+"
    rules["11"] = "42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 | 42 42 42 42 42 31 31 31 31 31 | 42 42 42 42 42 42 31 31 31 31 31 31 | 42 42 42 42 42 42 42 31 31 31 31 31 31 31 | 42 42 42 42 42 42 42 42 31 31 31 31 31 31 31 31"
    
    regex2 = build_re(rules["0"])

    part1 = part2 = 0
    for line in lines:
        if re.fullmatch(regex1, line):
            part1 += 1
        if re.fullmatch(regex2, line):
            part2 += 1
    
    print("Part 1:", part1)
    print("Part 2:", part2)
