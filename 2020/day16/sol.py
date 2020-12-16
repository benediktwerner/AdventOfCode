#!/usr/bin/env python3

from os import path
from collections import *
import re

CLASSES, MY_TICKET, NEARBY_TICKETS = range(3)


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    state = CLASSES
    classes = []
    my_ticket = None
    nearby_tickets = []

    for line in f.read().splitlines():
        if not line:
            state += 1
            continue

        if line in ("your ticket:", "nearby tickets:"):
            continue

        if state == CLASSES:
            name, lo1, hi1, lo2, hi2 = re.fullmatch(
                r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line
            ).groups()
            classes.append((name, int(lo1), int(hi1), int(lo2), int(hi2)))
        elif state == MY_TICKET:
            my_ticket = tuple(map(int, line.split(",")))
        else:
            nearby_tickets.append(tuple(map(int, line.split(","))))

    part1 = 0
    valid_tickets = []

    for ticket in nearby_tickets:
        valid = True
        for field in ticket:
            for _, lo1, hi1, lo2, hi2 in classes:
                if lo1 <= field <= hi1 or lo2 <= field <= hi2:
                    break
            else:
                valid = False
                part1 += field
        if valid:
            valid_tickets.append(ticket)

    print("Part 1:", part1)

    options = {i: set(range(len(classes))) for i in range(len(classes))}

    for ticket in valid_tickets:
        for i, field in enumerate(ticket):
            for j, (_, lo1, hi1, lo2, hi2) in enumerate(classes):
                if not (lo1 <= field <= hi1 or lo2 <= field <= hi2):
                    options[i].remove(j)

    part2 = 1

    while options:
        remove_keys = []
        remove_vals = set()
        for i, op in options.items():
            if len(op) == 1:
                cls = next(iter(op))
                if classes[cls][0].startswith("departure"):
                    part2 *= my_ticket[i]
                remove_keys.append(i)
                remove_vals.add(cls)
        for key in remove_keys:
            del options[key]
        for vals in options.values():
            vals.difference_update(remove_vals)

    print("Part 2:", part2)
