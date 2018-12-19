#!/usr/bin/env python3

from collections import defaultdict

OPEN = "."
TREE = "|"
LUMBER = "#"

DIFF = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]


def get_adjacent(grid, x, y):
    count = defaultdict(int)
    for xd, yd in DIFF:
        xadj = x+xd
        yadj = y+yd
        if 0 <= xadj < len(grid[0]) and 0 <= yadj < len(grid):
            count[grid[yadj][xadj]] += 1
    return count


def main():
    grid = []
    with open("input.txt") as f:
        for line in f:
            grid.append(list(line.strip()))

    history = {}
    minute = 0

    while minute < 1000000000:
        new_grid = []
        for y, line in enumerate(grid):
            row = []
            for x, value in enumerate(line):
                adj = get_adjacent(grid, x, y)
                if value == OPEN:
                    row.append(TREE if adj[TREE] >= 3 else value)
                elif value == TREE:
                    row.append(LUMBER if adj[LUMBER] >= 3 else value)
                else:
                    row.append(LUMBER if adj[LUMBER] >= 1 and adj[TREE] >= 1 else OPEN)
            new_grid.append(row)

        grid = new_grid
        minute += 1

        if minute == 10:
            tree_count = sum(v == TREE for row in grid for v in row)
            lumber_count = sum(v == LUMBER for row in grid for v in row)
            print("Part 1:", tree_count * lumber_count)

        grid_value = "".join("".join(line) for line in grid)
        if grid_value in history:
            cycle = minute - history[grid_value]
            cycles = (1000000000 - minute) // cycle
            minute += cycles * cycle
        else:
            history[grid_value] = minute

    tree_count = sum(v == TREE for row in grid for v in row)
    lumber_count = sum(v == LUMBER for row in grid for v in row)
    print("Part 2:", tree_count * lumber_count)

if __name__ == "__main__":
    main()
