#!/usr/bin/env python3

from os import path
import itertools


shapes = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (1, -1), (0, -1), (1, -2), (2, -1)),
    ((0, 0), (1, 0), (2, 0), (2, -1), (2, -2)),
    ((0, 0), (0, -1), (0, -2), (0, -3)),
    ((0, 0), (1, 0), (0, -1), (1, -1)),
]


def solve(jets, total_iters):
    jets = itertools.cycle(enumerate(jets))
    blocks = itertools.cycle(enumerate(shapes))
    grid = set((x, 0) for x in range(7))
    min_y = 0
    seen = {}
    i = 0
    found_repeat = False
    while i < total_iters:
        block_i, shape = next(blocks)
        width = max(x for x, _ in shape) + 1
        jet_i, jet = next(jets)
        if not found_repeat:
            for floor_y in range(min_y, -1, 1):
                if all((x, floor_y) in grid for x in range(7)):
                    top = tuple(sorted((x, y - min_y) for x, y in grid if y <= floor_y))
                    if (top, block_i, jet_i) in seen:
                        prev_i, prev_min_y = seen[(top, block_i, jet_i)]
                        period = i - prev_i
                        iters = (total_iters - i) // period
                        i += iters * period
                        y_diff = prev_min_y - min_y
                        min_y -= iters * y_diff
                        gg = list(grid)
                        grid = set()
                        for x, y in gg:
                            grid.add((x, y - iters * y_diff))
                        found_repeat = True
                    seen[(top, block_i, jet_i)] = i, min_y
                    break
        xx, yy = 2, min_y - 4
        while True:
            if jet == "<":
                if xx > 0 and not any(
                    (xx + xd - 1, yy + yd) in grid for xd, yd in shape
                ):
                    xx -= 1
            else:
                if xx + width < 7 and not any(
                    (xx + xd + 1, yy + yd) in grid for xd, yd in shape
                ):
                    xx += 1
            if any((xx + xd, yy + yd + 1) in grid for xd, yd in shape):
                for xd, yd in shape:
                    grid.add((xx + xd, yy + yd))
                break
            yy += 1
            jet_i, jet = next(jets)
        min_y = min(y for _, y in grid)
        i += 1
    return -min_y


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    jets = f.read().strip()
    print("Part 1:", solve(jets, 2022))
    print("Part 1:", solve(jets, 1000000000000))
