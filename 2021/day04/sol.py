#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    nums = map(int, lines[0].split(","))
    lines = lines[2:]

    boards = [
        [list(map(int, row.split())) for row in lines[6 * i : 6 * i + 5]]
        for i in range(len(lines) // 6)
    ]
    marked = [{} for _ in boards]
    won = set()
    for n in nums:
        for i, (m, b) in enumerate(zip(marked, boards)):
            if i in won:
                continue
            for y, row in enumerate(b):
                for x, c in enumerate(row):
                    if c == n:
                        m[(x, y)] = c
                        if all((x, yy) in m for yy in range(5)) or all(
                            (xx, y) in m for xx in range(5)
                        ):
                            score = (sum(sum(row) for row in b) - sum(m.values())) * n
                            if not won:
                                print("Part 1:", score)
                            won.add(i)
                            if len(won) == len(boards):
                                print("Part 2:", score)
