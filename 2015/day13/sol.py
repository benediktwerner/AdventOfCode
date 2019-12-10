#!/usr/bin/env python3

from os import path
from collections import defaultdict


def find_opt(m, names, curr=None):
    if curr is None:
        curr = []

    if not names:
        total = 0
        for i, n in enumerate(curr):
            total += m[n][curr[(i + 1) % len(curr)]]
            total += m[n][curr[(i - 1) % len(curr)]]
        return total

    curr_max = float("-inf")

    for n in tuple(names):
        names.remove(n)
        curr.append(n)
        val = find_opt(m, names, curr)
        if val > curr_max:
            curr_max = val
        curr.pop()
        names.add(n)

    return curr_max


def main():
    with open(path.join(path.dirname(__file__), "input.txt")) as f:
        m = defaultdict(dict)

        for line in f:
            line = line.strip()
            parts = line.split()
            name = parts[0]
            happiness = int(parts[3])
            if parts[2] == "lose":
                happiness *= -1
            target = parts[-1][:-1]
            m[name][target] = happiness

        names = set(m.keys())
        print("Part 1:", find_opt(m, names))

        for n in names:
            m[n]["me"] = 0
            m["me"][n] = 0

        print("Part 2:", find_opt(m, names, ["me"]))


if __name__ == "__main__":
    main()
