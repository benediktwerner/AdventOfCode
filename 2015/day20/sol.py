#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    target = int(f.read().strip())


N = 1_000_000
houses = [0] * N
for elf in range(1, N):
    num = elf
    presents = elf * 10
    while num < N:
        houses[num] += presents
        num += elf

for h, p in enumerate(houses):
    if p >= target:
        print("Part 1:", h)
        break


houses = [0] * N
for elf in range(1, N):
    num = elf
    presents = elf * 11
    for _ in range(50):
        houses[num] += presents
        num += elf
        if num >= N:
            break

for h, p in enumerate(houses):
    if p >= target:
        print("Part 2:", h)
        break
