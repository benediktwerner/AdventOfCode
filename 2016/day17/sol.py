#!/usr/bin/env python3

from os import path
from collections import deque
from hashlib import md5


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    passcode = f.read().strip().encode()
    todo = deque([(0, 0, b"")])
    shortest, longest = None, 0

    while todo:
        x, y, path = todo.popleft()
        h = md5(passcode + path).hexdigest()[:4]
        if x > 0 and int(h[2], 16) > 10:
            todo.append((x - 1, y, path + b"L"))
        if x < 3 and int(h[3], 16) > 10:
            if x == 2 and y == 3:
                if shortest is None:
                    shortest = path.decode() + "R"
                elif len(path) + 1 > longest:
                    longest = len(path) + 1
            else:
                todo.append((x + 1, y, path + b"R"))
        if y > 0 and int(h[0], 16) > 10:
            todo.append((x, y - 1, path + b"U"))
        if y < 3 and int(h[1], 16) > 10:
            if x == 3 and y == 2:
                if shortest is None:
                    shortest = path.decode() + "D"
                elif len(path) + 1 > longest:
                    longest = len(path) + 1
            else:
                todo.append((x, y + 1, path + b"D"))

    print("Part 1:", shortest)
    print("Part 2:", longest)
