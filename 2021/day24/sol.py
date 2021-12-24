#!/usr/bin/env python3

from os import path


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    prog = [line.split() for line in f.read().splitlines()]
    stack = []
    part1 = [None] * 14
    part2 = [None] * 14
    for i in range(14):
        if prog[18 * i + 4][-1] == "1":
            stack.append((i, int(prog[18 * i + 15][-1])))
        else:
            j, n = stack.pop()
            n += int(prog[18 * i + 5][-1])
            if n > 0:
                part1[i] = 9
                part1[j] = 9 - n
                part2[i] = 1 + n
                part2[j] = 1
            else:
                part1[i] = 9 + n
                part1[j] = 9
                part2[i] = 1
                part2[j] = 1 - n
    print("Part 1:", "".join(map(str, part1)))
    print("Part 2:", "".join(map(str, part2)))
