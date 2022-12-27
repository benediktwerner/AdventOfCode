#!/usr/bin/env python3

from os import path
import itertools
import re


# cost, dmg, armor
WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]

ARMORS = [
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

RINGS = [
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def simulate(m_hp, m_dmg, m_armor, e_hp, e_dmg, e_armor):
    while True:
        e_hp -= max(1, m_dmg - e_armor)
        if e_hp <= 0:
            return True
        m_hp -= max(1, e_dmg - m_armor)
        if m_hp <= 0:
            return False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    enemy = ints(f.read())
    min_cost = float("inf")
    max_cost = 0
    for equipment in itertools.product(WEAPONS, ARMORS, RINGS, RINGS):
        if equipment[2] == equipment[3] != (0, 0, 0):
            continue
        cost = sum(e[0] for e in equipment)
        dmg = sum(e[1] for e in equipment)
        defense = sum(e[2] for e in equipment)
        if simulate(100, dmg, defense, *enemy):
            min_cost = min(cost, min_cost)
        else:
            max_cost = max(cost, max_cost)
    print("Part 1:", min_cost)
    print("Part 2:", max_cost)
