#!/usr/bin/env python3

from collections import deque
from itertools import count

DIFF = [(0, -1), (-1, 0), (1, 0), (0, 1)]
ENEMY = {"E": "G", "G": "E"}


class Unit:
    next_idx = 0

    def __init__(self, x, y, dmg, char):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.hp = 200
        self.char = char
        self.enemy = ENEMY[char]

        self.idx = Unit.next_idx
        Unit.next_idx += 1

    def attack(self, units, grid):
        min_hp = 500
        target = None

        for xd, yd in DIFF:
            x = self.x + xd
            y = self.y + yd
            if grid[y][x] == self.enemy:
                unit = get_unit(x, y, units)
                if unit.hp < min_hp:
                    min_hp = unit.hp
                    target = unit

        if target is None:
            return False, False

        target.hp -= self.dmg
        if target.hp <= 0:
            grid[target.y][target.x] = "."
            return True, target.char == "E"

        return True, False


def get_unit(x, y, units):
    for unit in units:
        if unit.x == x and unit.y == y:
            return unit
    return None


def solve(elves_dmg=3):
    units = []
    grid = []

    with open("input.txt") as f:
        for y, line in enumerate(f):
            row = []
            for x, c in enumerate(line.strip()):
                if c == "G":
                    units.append(Unit(x, y, 3, c))
                elif c == "E":
                    units.append(Unit(x, y, elves_dmg, c))
                row.append(c)
            grid.append(row)

    turn = 0
    while True:
        for unit in sorted(units, key=lambda u: u.y * 1000 + u.x):
            if unit.hp <= 0:
                continue

            todo = deque([(unit.x + DIFF[i][0], unit.y + DIFF[i][1], i, i, 1) for i in range(4)])
            attacked, elve_died = unit.attack(units, grid)
            if attacked:
                if elve_died and elves_dmg > 3:
                    return False
                continue

            visited = set()
            last_d = 0
            targets = []
            while todo:
                x, y, first, last, d = todo.popleft()

                if d > last_d:
                    if targets:
                        break
                    last_d = d

                c = grid[y][x]
                if c == ".":
                    for i, (xd, yd) in enumerate(DIFF):
                        x_new = x + xd
                        y_new = y + yd
                        if (x_new, y_new) in visited:
                            continue
                        visited.add((x_new, y_new))
                        todo.append((x_new, y_new, first, i, d + 1))
                elif c == unit.enemy:
                    targets.append((x - DIFF[last][0], y - DIFF[last][1], first))

            if targets:
                *_, first = min(targets, key=lambda t: t[1] * 1000 + t[0])
                xd, yd = DIFF[first]
                grid[unit.y][unit.x] = "."
                unit.x += xd
                unit.y += yd
                grid[unit.y][unit.x] = unit.char
                _, elve_died = unit.attack(units, grid)
                if elve_died and elves_dmg > 3:
                    return False

        units = [unit for unit in units if unit.hp > 0]

        goblins = any(True for unit in units if unit.char == "G")
        elves = any(True for unit in units if unit.char == "E")

        if not goblins or not elves:
            total_hp = sum(unit.hp for unit in units)
            return (turn, total_hp)

        turn += 1


if __name__ == "__main__":
    turn, hp = solve()
    print("Part 1:", turn * hp, "(turn: {}, hp: {})".format(turn, hp))

    for i in count(4):
        result = solve(i)
        if result:
            turn, hp = result
            print("Part 2:", turn * hp, "(turn: {}, hp: {}, dmg: {})".format(turn, hp, i))
            break
