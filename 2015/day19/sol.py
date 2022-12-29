#!/usr/bin/env python3

from collections import defaultdict
from os import path
from lark import Lark


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    rule_lines, medicine = f.read().strip().split("\n\n")
    rules = defaultdict(list)
    for rule in rule_lines.splitlines():
        pat, to = rule.split(" => ")
        rules[pat].append(to)


def apply_rules(molecule, rules):
    for pattern, to in rules.items():
        i = 0
        while i <= len(molecule) - len(pattern):
            i = molecule.find(pattern, i)
            if i < 0:
                break
            for t in to:
                yield molecule[:i] + t + molecule[i + len(pattern) :]
            i += 1


print("Part 1:", len(set(apply_rules(medicine, rules))))


def to_non_terminal(x):
    return "n_" + "_".join(c if c.islower() else 2 * c.lower() for c in x)


grammar = defaultdict(list, {"start": ["n_e"]})

for pat, to in rules.items():
    results = []
    for t in to:
        i = 0
        rule = []
        while i < len(t):
            if i < len(t) - 1 and t[i : i + 2] in rules:
                rule.append(to_non_terminal(t[i : i + 2]))
                i += 2
            else:
                nt = to_non_terminal(t[i])
                rule.append(nt)
                i += 1
        results.append("(" + " ".join(rule) + ")")
    if len(pat) > 1:
        results.append("dont_count_" + to_non_terminal(pat))
        grammar["dont_count_" + to_non_terminal(pat)] = [
            " ".join(to_non_terminal(c) for c in pat)
        ]
    grammar[to_non_terminal(pat)] = results


for c in {c for words in list(rules.keys()) + sum(rules.values(), []) for c in words}:
    grammar[to_non_terminal(c)].append('"' + c + '"')

lark = Lark("\n".join(n + ": " + " | ".join(ks) for n, ks in grammar.items()))
tree = lark.parse(medicine)


def count(tree):
    return sum(map(count, tree.children)) + (
        -1 if tree.data.value.startswith("dont_count") else 1
    )


# subtract terminal productions and start
print("Part 2:", count(tree) - len(medicine) - 1)
