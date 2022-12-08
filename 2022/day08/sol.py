#!/usr/bin/env python3

from os import path

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = [list(map(int, line)) for line in f.read().splitlines()]
    max_score = float("-inf")
    visibles = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            score = 1
            visible = False
            c = grid[y][x]
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                xx, yy = x, y
                dist = 0
                while True:
                    xx += dx
                    yy += dy
                    if not (0 <= xx < len(grid[0]) and 0 <= yy < len(grid)):
                        visible = True
                        break
                    dist += 1
                    if grid[yy][xx] >= c:
                        break
                score *= dist

            max_score = max(max_score, score)
            if visible:
                visibles += 1

    print("Part 1:", visibles)
    print("Part 2:", max_score)
