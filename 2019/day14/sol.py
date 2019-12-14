#!/usr/bin/env python3

from os import path
from collections import defaultdict
import math


def ore_needed(fuel):
    have = defaultdict(int, {"FUEL": -fuel})
    todo = ["FUEL"]

    while todo:
        ele = todo.pop()
        needed = -have[ele]
        produced, inp = made_by[ele]
        repeat = math.ceil(needed / produced)
        have[ele] += repeat * produced

        for amt, ele in inp:
            have[ele] -= amt * repeat
            if ele != "ORE" and have[ele] < 0:
                todo.append(ele)

    return -have["ORE"]


def parse(x):
    amount, ele = x.split()
    return (int(amount), ele)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    made_by = {}

    for line in f:
        line = line.strip()
        inp, out = line.split(" => ")
        inp = [parse(x) for x in inp.split(", ")]
        out_amount, out_ele = parse(out)
        made_by[out_ele] = (out_amount, inp)

    ore = ore_needed(1)

    print("Part 1:", ore)

    min_fuel = 10 ** 12 // ore
    max_fuel = min_fuel * 5

    while min_fuel != max_fuel:
        fuel = (min_fuel + max_fuel + 1) // 2
        if ore_needed(fuel) > 10 ** 12:
            max_fuel = fuel - 1
        else:
            min_fuel = fuel

    print("Part 2:", max_fuel)
