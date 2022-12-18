#!/usr/bin/env python3

from os import path


def free_neighbors(point):
    for i in range(3):
        for d in (-1, 1):
            p = list(point)
            p[i] += d
            p = tuple(p)
            if p not in drops:
                yield p, i


def floodfill(cc):
    todo = [cc]
    connected = set()
    while todo:
        c = todo.pop()
        for n, i in free_neighbors(c):
            if n[i] < mins[i] or n[i] > maxs[i]:
                outside.update(connected)
                return True
            if n not in connected:
                connected.add(n)
                todo.append(n)
    pockets.update(connected)
    return False


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    drops = set(tuple(map(int, line.split(","))) for line in f.read().splitlines())
    part1, part2 = 0, 0
    mins = [min(c[i] for c in drops) for i in range(3)]
    maxs = [max(c[i] for c in drops) for i in range(3)]
    pockets, outside = set(), set()
    for c in drops:
        for n, _ in free_neighbors(c):
            part1 += 1
            if n not in pockets and (n in outside or floodfill(n)):
                part2 += 1
    print("Part 1:", part1)
    print("Part 2:", part2)
