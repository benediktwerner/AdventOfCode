#!/usr/bin/env python3

from collections import defaultdict


def parse(line):
    split = line.split(" ")
    i = split[0][1:]
    x, y = split[2][:-1].split(",")
    w, h = split[3].split("x")
    return map(int, (i, x, y, w, h))


def main():
    squares = defaultdict(lambda: 0)
    count = 0

    with open("input.txt") as f:
        for line in f:
            _, x, y, w, h = parse(line)
            for i in range(x, x+w):
                for j in range(y, y+h):
                    cord = (i, j)
                    if squares[cord] == 1:
                        count += 1
                    squares[cord] += 1

    print("Part 1:", count)

    with open("input.txt") as f:
        for line in f:
            idx, x, y, w, h = parse(line)
            overlap = False
            for i in range(x, x+w):
                for j in range(y, y+h):
                    if squares[(i, j)] > 1:
                        overlap = True
                        break
                if overlap:
                    break

            if not overlap:
                print("Part 2:", idx)


if __name__ == "__main__":
    main()
