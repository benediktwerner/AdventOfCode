#!/usr/bin/env python3

from os import path


def score(mine, theirs):
    return 3 * ((mine - theirs + 1) % 3) + mine + 1


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    score1, score2 = 0, 0

    for line in f.read().splitlines():
        theirs, mine = map(ord, line.split())
        theirs -= ord("A")
        mine -= ord("X")

        score1 += score(mine, theirs)
        score2 += score((theirs + mine - 1) % 3, theirs)

    print("Part 1:", score1)
    print("Part 2:", score2)
