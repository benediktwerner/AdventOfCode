#!/usr/bin/env python3

from os import path
from functools import lru_cache


@lru_cache(maxsize=None)
def wins(scores, positions, turn):
    if scores[0] >= 21:
        return 1, 0
    if scores[1] >= 21:
        return 0, 1

    wins1, wins2 = 0, 0
    for i in range(3):
        p = turn // 3
        pos = (positions[p] + i) % 10 + 1
        score = scores[p] + (turn % 3 == 2 and pos)
        w1, w2 = wins(
            (scores[0], score) if p == 1 else (score, scores[1]),
            (positions[0], pos) if p == 1 else (pos, positions[1]),
            (turn + 1) % 6,
        )
        wins1 += w1
        wins2 += w2
    return wins1, wins2


def part1(pos):
    pos = list(pos)
    scores = [0, 0]
    throws = 0
    while True:
        p = (throws // 3) % 2
        for _ in range(3):
            throw = throws % 100 + 1
            pos[p] = (pos[p] + throw - 1) % 10 + 1
            throws += 1
        scores[p] += pos[p]
        if scores[p] >= 1000:
            return scores[1 - p] * throws


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    positions = tuple([int(line.split()[-1]) for line in f.read().splitlines()])
    print("Part 1:", part1(positions))
    print("Part 2:", max(wins((0, 0), positions, 0)))
