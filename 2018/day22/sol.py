#!/usr/bin/env python3

import re
import heapq
from collections import defaultdict

NEITHER, TORCH, CLIMBING = range(3)
DIFF = ((0, 1), (0, -1), (1, 0), (-1, 0))
EQUIPMENT = (
    (TORCH, CLIMBING),
    (NEITHER, CLIMBING),
    (NEITHER, TORCH)
)


def main():
    with open("input.txt") as f:
        depth = int(re.findall(r"\d+", f.readline())[0])
        target = tuple([int(x) for x in re.findall(r"\d+", f.readline())])

    erosions = defaultdict(int)
    grid = defaultdict(int)
    danger = 0

    for x in range(target[0]+1000):
        for y in range(target[1]+1000):
            if (x, y) == (0, 0) or (x, y) == target:
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = erosions[(x-1, y)] * erosions[(x, y-1)]

            erosion = (geo + depth) % 20183
            erosions[(x, y)] = erosion
            grid[(x, y)] = erosion % 3

            if x <= target[0] and y <= target[1]:
                danger += (erosion % 3)

    print("Part 1:", danger)

    heap = [(0, TORCH, 0, 0)]  # time, equipment, x, y
    visited = set()

    while True:
        time, eq, x, y = heapq.heappop(heap)

        if (eq, x, y) in visited:
            continue
        visited.add((eq, x, y))

        if (x, y) == target and eq == 1:
            print("Part 2:", time)
            return

        for xd, yd in DIFF:
            nx, ny = x+xd, y+yd

            if nx < 0 or ny < 0:
                continue

            if eq not in EQUIPMENT[grid[(nx, ny)]]:
                continue

            heapq.heappush(heap, (time+1, eq, nx, ny))

        for other_eq in EQUIPMENT[grid[(x, y)]]:
            if eq != other_eq and (other_eq, x, y) not in visited:
                heapq.heappush(heap, (time+7, other_eq, x, y))


if __name__ == "__main__":
    main()
