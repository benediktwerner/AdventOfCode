#!/usr/bin/env python3

import itertools
from collections import defaultdict
from os import path

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    grid = [list(line) for line in file.read().splitlines()]
    width, height = len(grid[0]), len(grid)

    def compute_costs(x, y):
        area_id = grid[y][x]
        grid[y][x] = "."
        todo = [(x, y)]
        seen = set([(x, y)])
        perimeter = 0
        fences_by_direction = defaultdict(set)

        while todo:
            x, y = todo.pop()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == area_id:
                    grid[ny][nx] = "."
                    todo.append((nx, ny))
                    seen.add((nx, ny))
                elif (nx, ny) not in seen:
                    perimeter += 1
                    fences_by_direction[(dx, dy)].add((x, y))

        area = len(seen)
        sides = 0
        for (dx, dy), fences in fences_by_direction.items():
            while fences:
                x, y = fences.pop()
                sides += 1
                for d in (1, -1):
                    for i in itertools.count(d, d):
                        if (x + i * dy, y + i * dx) in fences:
                            fences.remove((x + i * dy, y + i * dx))
                        else:
                            break

        return area * perimeter, area * sides

    part1 = part2 = 0

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != ".":
                c1, c2 = compute_costs(x, y)
                part1 += c1
                part2 += c2

    print("Part 1:", part1)
    print("Part 2:", part2)
