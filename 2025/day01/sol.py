#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0
    dial = 50

    for line in file.read().splitlines():
        direction = line[0]
        amount = int(line[1:])
        old_dial = dial

        if amount >= 100:
            part2 += amount // 100
            amount %= 100

        if direction == "R":
            dial += amount
        else:
            dial -= amount

        if old_dial != 0 and (dial <= 0 or dial >= 100):
            part2 += 1

        dial %= 100

        if dial == 0:
            part1 += 1

    print("Part 1:", part1)
    print("Part 2:", part2)
