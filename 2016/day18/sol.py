#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    rows = [f.read().strip()]

    for i in range(399_999):
        last = rows[-1]
        new = last[1]
        for i in range(1, len(last) - 1):
            new += "^" if last[i-1] != last[i+1] else "."
        new += last[-2]
        rows.append(new)

    print("Part 1:", sum(c == "." for row in rows[:40] for c in row))
    print("Part 2:", sum(c == "." for row in rows for c in row))
