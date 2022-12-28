#!/usr/bin/env python3

from os import path
import heapq
import re


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(hp, dmg, part2):
    dmg_shield = max(1, dmg - 7)
    q = [(0, 49 if part2 else 50, 500, hp, 0, 0, 0)]
    visited = set(q)
    while q:
        spent, hp, mana, e_hp, shield, poison, recharge = heapq.heappop(q)
        if poison > 0:
            poison -= 1
            e_hp -= 3
        if recharge > 0:
            recharge -= 1
            mana += 101
        new = [(spent + 53, hp, mana - 53, e_hp - 4, shield, poison, recharge)]
        if mana >= 73:
            new.append(
                (spent + 73, hp + 2, mana - 73, e_hp - 2, shield, poison, recharge)
            )
        if mana >= 113 and shield <= 1:
            new.append((spent + 113, hp, mana - 113, e_hp, 3, poison, recharge))
        if mana >= 173 and poison == 0:
            new.append((spent + 173, hp, mana - 173, e_hp, shield, 6, recharge))
        if mana >= 229 and recharge <= 1:
            new.append((spent + 229, hp, mana - 229, e_hp, shield, poison, 5))
        for spent, hp, mana, e_hp, shield, poison, recharge in new:
            if poison > 0:
                poison -= 1
                e_hp -= 3
            if e_hp <= 0:
                return spent
            hp -= dmg if shield == 0 else dmg_shield
            if part2:
                hp -= 1
            if hp <= 0 or (mana < 53 and recharge == 0):
                continue
            if recharge > 0:
                recharge -= 1
                mana += 101
            if shield > 0:
                shield -= 1
            n = (spent, hp, mana, e_hp, shield, poison, recharge)
            if n not in visited:
                heapq.heappush(q, n)
                visited.add(n)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    hp, dmg = ints(f.read())
    print("Part 1:", solve(hp, dmg, False))
    print("Part 2:", solve(hp, dmg, True))
