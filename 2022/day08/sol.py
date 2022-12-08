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

            for i in range(x + 1, len(grid[0])):
                if grid[y][i] >= c:
                    score *= i - x
                    break
            else:
                score *= len(grid[0]) - 1 - x
                visible = True

            for i in range(x - 1, -1, -1):
                if grid[y][i] >= c:
                    score *= x - i
                    break
            else:
                score *= x
                visible = True

            for i in range(y + 1, len(grid)):
                if grid[i][x] >= c:
                    score *= i - y
                    break
            else:
                score *= len(grid) - 1 - y
                visible = True

            for i in range(y - 1, -1, -1):
                if grid[i][x] >= c:
                    score *= y - i
                    break
            else:
                score *= y
                visible = True

            max_score = max(max_score, score)
            if visible:
                visibles += 1

    print("Part 1:", visibles)
    print("Part 2:", max_score)
