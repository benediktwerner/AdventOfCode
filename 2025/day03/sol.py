#!/usr/bin/env python3


from os import path


def find_max(bank: str, n: int) -> str:
    if n == 1:
        return max(bank)
    a = max(bank[: -n + 1])
    return a + find_max(bank[bank.find(a) + 1 :], n - 1)


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    for bank in file.read().splitlines():
        part1 += int(find_max(bank, 2))
        part2 += int(find_max(bank, 12))

    print("Part 1:", part1)
    print("Part 2:", part2)
