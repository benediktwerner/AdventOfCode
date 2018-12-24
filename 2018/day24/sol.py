#!/usr/bin/env python3

import re
from itertools import count


class Unit:
    def __init__(self, infection, units, hp, dmg, initiative):
        self.units = units
        self.hp = hp
        self.dmg = dmg
        self.initiative = initiative
        self.infection = infection
        self.immunities = set()
        self.weaknesses = set()

    def effective_dmg(self):
        return self.units * self.dmg

    def dmg_from(self, unit):
        if unit.dmg_type in self.immunities:
            return 0
        if unit.dmg_type in self.weaknesses:
            return unit.effective_dmg() * 2
        return unit.effective_dmg()

    def choose_target(self, targets):
        self.target = None
        self.target_dmg = 1
        self.target_eff_dmg = 0
        for t in targets:
            dmg = t.dmg_from(self)
            if self.rather_attack(t, dmg):
                self.target = t
                self.target_dmg = dmg
                self.target_eff_dmg = t.effective_dmg()
        if self.target:
            targets.remove(self.target)

    def rather_attack(self, target, dmg):
        if dmg > self.target_dmg:
            return True
        if dmg == self.target_dmg:
            if not self.target:
                return True
            eff_dmg = target.effective_dmg()
            if eff_dmg > self.target_eff_dmg:
                return True
            if eff_dmg == self.target_eff_dmg:
                return target.initiative > self.target.initiative
        return False

    def attack(self):
        if self.units <= 0 or self.target is None:
            return False

        dmg = self.target.dmg_from(self)
        dmg //= self.target.hp

        if dmg == 0:
            return False

        self.target.units -= dmg
        return True

    def __repr__(self):
        return ("Immune", "Infection")[self.infection] + "({}, hp={}, dmg={}, dmg_type={}, weaknesses={}, immunities={}".format(self.units, self.hp, self.dmg, self.dmg_type, self.weaknesses, self.immunities)


def re_find(regex, line):
    out = re.findall(regex, line)
    if out:
        return out[0].split(", ")
    return out


def parse_line(line, infection):
    unit = Unit(infection, *map(int, re.findall(r"\d+", line)))
    unit.dmg_type = re.findall(r"(\w+) damage", line)[0]
    unit.immunities = set(re_find(r"immune to ([a-z ,]+)[;)]", line))
    unit.weaknesses = set(re_find(r"weak to ([a-z ,]+)[;)]", line))
    return unit


def choose_targets(attackers, defenders):
    targets = defenders[:]
    for unit in sorted(attackers, key=lambda u: u.effective_dmg()*1000 + u.initiative, reverse=True):
        unit.choose_target(targets)


def simulate(units, boost=0):
    immune = [unit for unit in units if not unit.infection]
    infection = [unit for unit in units if unit.infection]

    for unit in immune:
        unit.dmg += boost

    while immune and infection:
        choose_targets(immune, infection)
        choose_targets(infection, immune)

        changes = False
        for unit in sorted(units, key=lambda u: u.initiative, reverse=True):
            if unit.attack():
                changes = True

        if not changes:
            return False, units

        units = [unit for unit in units if unit.units > 0]
        immune = [unit for unit in immune if unit.units > 0]
        infection = [unit for unit in infection if unit.units > 0]

    return True, units


def get_input():
    units = []

    with open("input.txt") as f:
        state = 0
        for line in f:
            line = line.strip()

            if not line or line == "Immune System:":
                continue
            elif line == "Infection:":
                state = 1
            elif state == 0:
                units.append(parse_line(line, False))
            else:
                units.append(parse_line(line, True))

    return units


def main():
    _, result = simulate(get_input())
    print("Part 1:", sum(unit.units for unit in result))

    for boost in count(1):
        combat_finished, result = simulate(get_input(), boost)

        if combat_finished and result and not result[0].infection:
            print("Part 2:", sum(unit.units for unit in result), boost)
            break


if __name__ == "__main__":
    main()
