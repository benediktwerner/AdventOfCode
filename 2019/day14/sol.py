#!/usr/bin/env python3

from os import path
from collections import *
import math


def to_vec(x):
    v = [0] * len(elements_to_index)
    for amt, e in x:
        v[e] += amt
    return tuple(v)


def apply_reaction(need, have, reaction_index, times):
    inp, out = reactions[reaction_index]

    for i, a in enumerate(inp):
        a *= times
        if have[i] >= a:
            have[i] -= a
        else:
            a -= have[i]
            have[i] = 0
            need[i] += a

    for i, a in enumerate(out):
        a *= times
        if a > need[i]:
            have[i] += a - need[i]
            need[i] = 0
        else:
            need[i] -= a


def ore_needed(need, have):
    for e in range(len(elements_to_index)):
        if have[e] > 0 and need[e] > 0:
            print("x")
            if have[e] > need[e]:
                have[e] -= need[e]
                need[e] = 0
            else:
                need[e] -= have[e]

    for e, a in enumerate(need):
        if e != ore_index and a > 0:
            break
    else:
        return need[ore_index]

    for e, a in enumerate(need):
        if a > 0 and len(made_by[e]) == 1:
            ri = made_by[e][0]
            reaction = reactions[ri]
            apply_reaction(need, have, ri, math.ceil(a / reaction[1][e]))
            return ore_needed(need, have)

    raise Exception("need to brute-force")


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    elements_to_index = {}
    reactions = []
    made_by = defaultdict(list)

    for line in f:
        line = line.strip()
        inp, out = line.split(" => ")
        inp2, out2 = [], []

        for ie in inp.split(", "):
            amount, e = ie.split()
            if e not in elements_to_index:
                elements_to_index[e] = len(elements_to_index)
            inp2.append((int(amount), elements_to_index[e]))

        for oe in out.split(", "):
            amount, e = oe.split()
            if e not in elements_to_index:
                elements_to_index[e] = len(elements_to_index)
            out2.append((int(amount), elements_to_index[e]))
            made_by[elements_to_index[e]].append(len(reactions))

        reactions.append((inp2, out2))

    reactions = [(to_vec(inp), to_vec(out)) for inp, out in reactions]

    ore_index = elements_to_index["ORE"]
    fuel_index = elements_to_index["FUEL"]
    have = [0] * len(elements_to_index)

    need = list(to_vec([(1, fuel_index)]))
    ore = ore_needed(need, have)

    print("Part 1:", ore)

    min_fuel = 10 ** 12 // ore
    max_fuel = min_fuel * 5

    while min_fuel != max_fuel:
        fuel = (min_fuel + max_fuel + 1) // 2
        need = list(to_vec([(fuel, fuel_index)]))
        if ore_needed(need, have) > 10 ** 12:
            max_fuel = fuel - 1
        else:
            min_fuel = fuel

    print("Part 2:", max_fuel)
