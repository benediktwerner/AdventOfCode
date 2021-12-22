#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    curr = f.read().strip()
    for i in range(50):
        new = ""
        count = 0
        last = None
        for c in curr:
            if c != last:
                if last is not None:
                    new += f"{count}{last}"
                last = c
                count = 0
            count += 1
        curr = new + f"{count}{last}"

        if i == 39:
            print("Part 1:", len(curr))

    print("Part 2:", len(curr))
