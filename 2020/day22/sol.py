#!/usr/bin/env python3

from os import path
from collections import deque
from itertools import islice


def part1(p1, p2):
    while p1 and p2:
        a, b = p1.popleft(), p2.popleft()
        if a > b:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)

    print("Part 1:", sum(v * (i + 1) for i, v in enumerate(reversed(p1 or p2))))


def part2(p1, p2):
    history = set()
    while p1 and p2:
        key = ",".join(map(str, p1)) + ":" + ",".join(map(str, p2))
        if key in history:
            return True, p1
        history.add(key)

        a, b = p1.popleft(), p2.popleft()
        if len(p1) >= a and len(p2) >= b:
            p1wins, _ = part2(deque(islice(p1, a)), deque(islice(p2, b)))
        else:
            p1wins = a > b

        if p1wins:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)

    return bool(p1), (p1 or p2)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    state = 0
    p1, p2 = deque(), deque()

    for line in f.read().splitlines():
        if state in (0, 2) or not line:
            state += 1
        elif state == 1:
            p1.append(int(line))
        else:
            p2.append(int(line))

    part1(p1.copy(), p2.copy())

    _, deck = part2(p1, p2)
    print("Part 1:", sum(v * (i + 1) for i, v in enumerate(reversed(deck))))
