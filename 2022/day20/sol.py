#!/usr/bin/env python3

from os import path


def solve(inp, repeat):
    nums = list(enumerate(inp))
    new = nums[:]
    for _ in range(repeat):
        for p in nums:
            if p[1] == 0:
                continue
            i = new.index(p)
            new.remove(p)
            target = (i + p[1]) % len(new)
            if target == 0:
                new.append(p)
            else:
                new.insert(target, p)
    zero = [n for _, n in new].index(0)
    return sum(new[(zero + i) % len(new)][1] for i in (1000, 2000, 3000))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = list(map(int, f.read().splitlines()))
    print("Part 1:", solve(inp, 1))
    print("Part 2:", solve(map(lambda x: x * 811589153, inp), 10))
