#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
import operator
import re
from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import cache
from os import path

import pyperclip


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def move_by(self, dir: int) -> Pos:
        dx, dy = DIR_TO_DELTA[dir]
        return Pos(self.x + dx, self.y + dy)


RIGHT, DOWN, LEFT, UP, ACTIVATE = range(5)
DIR_TO_DELTA = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}
ALLOWED_DIRS_ROBO = {
    Pos(1, 0): [RIGHT, DOWN],
    Pos(2, 0): [LEFT, DOWN],
    Pos(0, 1): [RIGHT],
    Pos(1, 1): [LEFT, UP, RIGHT],
    Pos(2, 1): [LEFT, UP],
}
BUTTON_ROBO = {
    Pos(1, 0): UP,
    Pos(2, 0): ACTIVATE,
    Pos(0, 1): LEFT,
    Pos(1, 1): DOWN,
    Pos(2, 1): RIGHT,
}
ALLOWED_DIRS_DOOR = {
    Pos(0, 0): [DOWN, RIGHT],
    Pos(1, 0): [LEFT, DOWN, RIGHT],
    Pos(2, 0): [LEFT, DOWN],
    Pos(0, 1): [UP, DOWN, RIGHT],
    Pos(1, 1): [UP, LEFT, DOWN, RIGHT],
    Pos(2, 1): [UP, LEFT, DOWN],
    Pos(0, 2): [UP, RIGHT],
    Pos(1, 2): [UP, LEFT, DOWN, RIGHT],
    Pos(2, 2): [UP, LEFT, DOWN],
    Pos(1, 3): [UP, RIGHT],
    Pos(2, 3): [UP, LEFT],
}
BUTTON_DOOR = {
    Pos(0, 0): "7",
    Pos(1, 0): "8",
    Pos(2, 0): "9",
    Pos(0, 1): "4",
    Pos(1, 1): "5",
    Pos(2, 1): "6",
    Pos(0, 2): "1",
    Pos(1, 2): "2",
    Pos(2, 2): "3",
    Pos(1, 3): "0",
    Pos(2, 3): "A",
}


def solve_code(code: str, robots) -> int:
    def activate(i: int) -> int | None:
        curr = positions[i]
        next = positions[i - 1]
        if BUTTON_ROBO[curr] != ACTIVATE and BUTTON_ROBO[curr] not in (
            ALLOWED_DIRS_ROBO[next] if i > 1 else ALLOWED_DIRS_DOOR[next]
        ):
            return
        if BUTTON_ROBO[curr] == ACTIVATE:
            if i > 1:
                return activate(i - 1)
            elif BUTTON_DOOR[next] == code[code_index]:
                if code_index + 1 == len(code):
                    return presses + 1
                if (code_index + 1, positions) not in seen:
                    seen.add((code_index + 1, positions))
                    todo.append((presses + 1, code_index + 1, positions))
        else:
            new_positions = (
                positions[: i - 1] + (next.move_by(BUTTON_ROBO[curr]),) + positions[i:]
            )
            if (code_index, new_positions) not in seen:
                seen.add((code_index, new_positions))
                todo.append((presses + 1, code_index, new_positions))

    todo = deque([(0, 0, (Pos(2, 3),) + tuple(Pos(2, 0) for _ in range(robots)))])
    seen = set([todo[0][1:]])
    while todo:
        presses, code_index, positions = todo.popleft()
        for d in ALLOWED_DIRS_ROBO[positions[-1]]:
            new_positions = positions[:-1] + (positions[-1].move_by(d),)
            if (code_index, new_positions) not in seen:
                seen.add((code_index, new_positions))
                todo.append((presses + 1, code_index, new_positions))
        if result := activate(robots):
            return result

    assert False


def solve(inp: str):
    result = 0

    for code in inp.splitlines():
        result += solve_code(code, 25) * int(code[:-1])

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
