#!/usr/bin/env python3

from os import path
import itertools
import re


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    disks = []

    for line in f:
        line = line.strip()
        mod, start = map(int, re.fullmatch(r"Disc #\d has (\d+) positions; at time=0, it is at position (\d+).", line).groups())
        disks.append([mod, start])

    last_mod, last_pos = 11, 0
    part1_done = False

    for time in itertools.count():
        part1 = True
        part2 = True

        for i, disk in enumerate(disks, 1):
            mod, pos = disk

            if  (pos + i) % mod != 0:
                part1 = part2 = False
            
            disk[1] = (pos + 1) % mod
        
        if  (last_pos + len(disks) + 1) % last_mod != 0:
            part2 = False
        last_pos = (last_pos + 1) % last_mod

        if not part1_done and part1:
            print("Part 1:", time)
            part1_done = True

        if part2:
            print("Part 2:", time)
            break
