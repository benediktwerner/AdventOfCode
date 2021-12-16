#!/usr/bin/env python3

from os import path
import math


SUM, PRODUCT, MIN, MAX, LITERAL, GT, LT, EQ = range(8)

OPS = {
    SUM: sum,
    PRODUCT: math.prod,
    MIN: min,
    MAX: max,
    GT: lambda subs: subs[0] > subs[1],
    LT: lambda subs: subs[0] < subs[1],
    EQ: lambda subs: subs[0] == subs[1],
}


def decode(pkg):
    version = int(pkg[:3], 2)
    type_id = int(pkg[3:6], 2)

    if type_id == LITERAL:
        num = 0
        todo = pkg[6:]
        while True:
            num <<= 4
            num |= int(todo[1:5], 2)
            if todo[0] == "0":
                return version, num, todo[5:]
            todo = todo[5:]

    subs = []

    if pkg[6] == "0":
        length = int(pkg[7:22], 2)
        todo, pkg = pkg[22 : 22 + length], pkg[22 + length :]
        while todo:
            sub_version, sub, todo = decode(todo)
            subs.append(sub)
            version += sub_version
    else:
        count = int(pkg[7:18], 2)
        pkg = pkg[18:]
        for _ in range(count):
            sub_version, sub, pkg = decode(pkg)
            subs.append(sub)
            version += sub_version

    return version, OPS[type_id](subs), pkg


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.read().strip()

pkg = "".join(f"{int(c, 16):04b}" for c in inp)
version, result, _ = decode(pkg)

print("Part 1:", version)
print("Part 2:", result)
