#!/usr/bin/env python3

from os import path
import itertools as iter
import re


def powerset(xs):
    return iter.chain.from_iterable(iter.combinations(xs, r) for r in range(len(xs) + 1))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    mem1 = {}
    mem2 = {}

    for line in f.read().splitlines():
        if line.startswith("mask"):
            mask = re.fullmatch(r"mask = ([X10]{36})", line).groups()[0]

            or_mask1 = int(mask.replace("X", "0"), 2)
            and_mask1 = int(mask.replace("X", "1"), 2)

            or_mask2 = int(mask.replace("X", "0"), 2)
            and_mask2 = int(mask.replace("0", "1").replace("X", "0"), 2)
            floating = [35 - i for i, c in enumerate(mask) if c == "X"]
        else:
            addr, val = map(int, re.fullmatch(r"mem\[(\d+)] = (\d+)", line).groups())

            mem1[addr] = (val | or_mask1) & and_mask1

            addr &= and_mask2
            addr |= or_mask2
            for comb in powerset(floating):
                new_addr = addr
                for i in comb:
                    new_addr |= 1 << i
                mem2[new_addr] = val

    print("Part 1:", sum(mem1.values()))
    print("Part 2:", sum(mem2.values()))
