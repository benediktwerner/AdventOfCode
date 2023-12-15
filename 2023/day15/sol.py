#!/usr/bin/env python3

from os import path
import re


def hash(inp: str) -> int:
    result = 0
    for c in inp:
        result += ord(c)
        result *= 17
        result %= 256
    return result


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    steps = file.read().strip().split(",")

    print("Part 1:", sum(hash(step) for step in steps))

    boxes = [[] for _ in range(256)]
    for step in steps:
        label, op, focus = re.findall(r"([a-z]+)(=|-)([0-9]*)", step)[0]
        box = boxes[hash(label)]
        match op:
            case "-":
                for i, lens in enumerate(box):
                    if lens[0] == label:
                        box.pop(i)
                        break
            case "=":
                for i, lens in enumerate(box):
                    if lens[0] == label:
                        box[i] = (label, focus)
                        break
                else:
                    box.append((label, focus))
            case _:
                assert False

    result = 0
    for i, box in enumerate(boxes, 1):
        for j, (label, focus) in enumerate(box, 1):
            result += i * j * int(focus)
    print("Part 2:", result)
