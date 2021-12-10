#!/usr/bin/env python3

from os import path

OPPOSITE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1 = 0
    scores = []
    for line in f.read().splitlines():
        stack = []
        for c in line:
            if c in OPPOSITE:
                stack.append(OPPOSITE[c])
            elif c != stack.pop():
                part1 += {")": 3, "]": 57, "}": 1197, ">": 25137}[c]
                break
        else:
            score = 0
            for c in reversed(stack):
                score *= 5
                score += {")": 1, "]": 2, "}": 3, ">": 4}[c]
            scores.append(score)

    scores.sort()

    print("Part 1:", part1)
    print("Part 2:", scores[len(scores) // 2])
