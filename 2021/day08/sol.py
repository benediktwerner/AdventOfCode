#!/usr/bin/env python3

from os import path
from collections import defaultdict


def single(s, filter_fn=None):
    if filter_fn:
        s = filter(filter_fn, s)
    return next(iter(s))


def solve(pattern):
    by_count = defaultdict(list)
    for x in pattern:
        by_count[len(x)].append(x)

    one = single(by_count[2])
    four = single(by_count[4])
    seven = single(by_count[3])
    eight = single(by_count[7])
    six = single(by_count[6], lambda x: not all(k in x for k in one))
    a = single(seven - one)
    f = single(six & one)
    c = single(one - {f})
    three = single(by_count[5], lambda x: f in x and c in x)
    two = single(by_count[5], lambda x: f not in x and c in x)
    five = single(by_count[5], lambda x: f in x and c not in x)
    e = single(two - three)
    b = single(five - three)
    d = single((two & four) - {c})
    g = single(two - {a, c, d, e})
    zero = {a, b, c, e, f, g}
    six = {a, b, d, e, f, g}
    nine = {a, b, c, d, f, g}
    return [zero, one, two, three, four, five, six, seven, eight, nine]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1, part2 = 0, 0

    for line in f.read().splitlines():
        pattern, output = (list(map(set, x.split())) for x in line.split("|"))
        sol = solve(pattern)
        out = 0
        for digit in output:
            d = sol.index(digit)
            out = out * 10 + d
            if d in (1, 4, 7, 8):
                part1 += 1
        part2 += out

    print("Part 1:", part1)
    print("Part 2:", part2)
