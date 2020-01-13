#!/usr/bin/env python3

from os import path


def find_ab(m):
    a, b = 1, 0

    with open(path.join(path.dirname(__file__), "input.txt")) as f:
        for line in f:
            parts = line.strip().split()

            if parts[0] == "cut":
                index = int(parts[1])
                na, nb = 1, -index
            elif parts[1] == "into":
                na, nb = -1, -1
            else:
                inc = int(parts[3])
                na, nb = inc, 0

            a = (a * na) % m
            b = (b * na + nb) % m

    return a, b


def modinv(x, m):
    # if m is prime
    return pow(x, m - 2, m)


cards = 10007
a, b = find_ab(cards)
print("Part 1:", (a * 2019 + b) % cards)

cards = 119315717514047
repeat = 101741582076661
a, b = find_ab(cards)
ra = pow(a, repeat, cards)
rb = (b * (ra - 1) * modinv(a - 1, cards)) % cards
print("Part 2:", (2020 - rb) * modinv(ra, cards) % cards)
