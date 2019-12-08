#!/usr/bin/env python3

import os
from collections import deque


def is_free(x, y):
    if x < 0 or y < 0:
        return False

    k = x * x + 3 * x + 2 * x * y + y + y * y + designer_num
    b = sum(c == "1" for c in bin(k))
    return b % 2 == 0


def part1():
    came_from = {(1, 1): None}
    todo = deque([(1, 1)])

    while todo:
        x, y = curr = todo.popleft()
        for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = nxt = x + dx, y + dy

            if nx == 31 and ny == 39:
                length = 0
                while curr is not None:
                    curr = came_from[curr]
                    length += 1
                return length

            if nxt not in came_from and is_free(nx, ny):
                came_from[nxt] = curr
                todo.append(nxt)


with open(os.path.dirname(__file__) + "/input.txt") as f:
    designer_num = int(f.readline().strip())

    print("Part 1:", part1())

    visited = set([(1, 1)])
    todo = deque([(1, 1, 0)])

    while todo:
        x, y, s = todo.popleft()
        for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = nxt = x + dx, y + dy

            if nxt not in visited and is_free(nx, ny):
                visited.add(nxt)
                if s < 49:
                    todo.append((nx, ny, s + 1))

    print("Part 2:", len(visited))
