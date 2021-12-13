#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    points = set()
    lines = iter(f.read().splitlines())

    for line in lines:
        if not line:
            break
        points.add(tuple(map(int, line.split(","))))

    for i, line in enumerate(lines):
        (*_, dir), p = line.split("=")
        p = int(p)
        for x, y in tuple(points):
            if dir == "x":
                if x > p:
                    points.remove((x, y))
                    points.add((2 * p - x, y))
            elif y > p:
                points.remove((x, y))
                points.add((x, 2 * p - y))

        if i == 0:
            print("Part 1:", len(points))

    xmax = max(x for x, _ in points)
    ymax = max(y for _, y in points)

    print("Part 2:")

    for y in range(ymax + 1):
        print("".join((" ", "█")[(x, y) in points] for x in range(xmax + 1)))
