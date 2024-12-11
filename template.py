#!/usr/bin/env python3

import itertools
import math
import operator
import re
from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import cache
from os import path

import pyperclip
from tqdm import tqdm

# from networkx import *


RIGHT, DOWN, LEFT, UP = range(4)
DIRS1 = ((0, 1), (0, -1), (1, 0), (-1, 0))
DIRS2 = DIRS1 + ((1, 1), (1, -1), (-1, 1), (-1, -1))
DIRS = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (1, 0),
}


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp: str):
    result = 0
    lines = inp.splitlines()
    width, height = len(lines[0]), len(lines)

    def ok(x, y=None):
        if y is None:
            x, y = x
        return 0 <= x < width and 0 <= y < height

    def neighbors(x, y=None):
        if y is None:
            x, y = x
        for dx, dy in DIRS1:
            nx, ny = x + dx, y + dy
            if ok(nx, ny):
                yield nx, ny

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pass

    for line in lines:
        pass

    return result


example = """\

"""

if example and not example.isspace():
    print("Example:", solve(example))
else:
    print("No example provided")

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    result = solve(file.read())
    print("Output:", result)
    pyperclip.copy(str(result))
    print("Copied to clipboard")
