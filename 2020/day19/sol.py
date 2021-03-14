#!/usr/bin/env python3

from os import path
import re


def build_re(rule):
    if "|" in rule:
        a, b = rule.split(" | ")
        return f"(?:(?:{build_re(a)})|(?:{build_re(b)}))"
    if rule[0] == '"':
        return rule[1]
    return "".join(build_re(rules[r]) for r in rule.split())


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = map(lambda line: line.strip(), f)
    rules = {}
    for line in lines:
        if not line:
            break
        num, rule = line.split(": ")
        rules[num] = rule

    regex = build_re(rules["0"])

    count = 0
    for line in lines:
        if re.fullmatch(regex, line):
            count += 1
    
    print("Part 1:", count)
