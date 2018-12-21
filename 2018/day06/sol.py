#!/usr/bin/env python3

from collections import defaultdict


DIFFS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def main():
    cords = []

    with open("input.txt") as f:
        for line in f:
            cords.append(tuple(map(int, line.strip().split(", "))))

    min_x = min(c[0] for c in cords)
    min_y = min(c[1] for c in cords)
    max_x = max(c[0] for c in cords)
    max_y = max(c[1] for c in cords)

    todo = [(i, x, y) for i, (x, y) in enumerate(cords)]
    area = [0] * len(cords)
    claims = defaultdict(lambda: -1)

    while todo:
        new_todo = []
        claimed_now = defaultdict(lambda: -1)
        for i, x, y in todo:
            if x <= min_x or x >= max_x or y <= min_y or y >= max_y:
                area[i] = float("inf")
                continue

            cord = (x, y)
            if claims[cord] == -1:
                claims[cord] = i
                claimed_now[cord] = i
                area[i] += 1
                for xd, yd in DIFFS:
                    if claims[(x+xd, y+yd)] == -1:
                        new_todo.append((i, x+xd, y+yd))
            elif claims[cord] >= 0 and claimed_now[cord] not in (-1, i):
                area[claimed_now[cord]] -= 1
                claims[cord] = -2
        todo = new_todo

    print("Part 1:", max(a for a in area if a != float("inf")))

    area = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            dist = 0
            for a, b in cords:
                dist += abs(x - a) + abs(y - b)
                if dist >= 10000:
                    break
            else:
                area += 1
    
    print("Part 2:", area)


if __name__ == "__main__":
    main()
