#!/usr/bin/env python3

import re
from collections import defaultdict
from z3 import Int, If, Optimize


def z3_abs(x):
    return If(x < 0, -x, x)


def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])


def main():
    bots = []

    with open("input.txt") as f:
        for line in f:
            bots.append(tuple(map(int, re.findall(r"-?\d+", line))))

    x, y, z, r = max(bots, key=lambda b: b[3])
    in_range = sum((abs(x-b[0])+abs(y-b[1])+abs(z-b[2]) <= r) for b in bots)
    print("Part 1:", in_range)

    x, y, z = Int("x"), Int("y"), Int("z")
    point = (x, y, z)
    count = sum(If(z3_dist(b[:3], point) <= b[3], 1, 0) for b in bots)

    opt = Optimize()
    opt.maximize(count)
    opt.minimize(z3_dist(point, (0, 0, 0)))

    opt.check()
    model = opt.model()
    result = model[x].as_long() + model[y].as_long() + model[z].as_long()

    print("Part 2:", result)


if __name__ == "__main__":
    main()
