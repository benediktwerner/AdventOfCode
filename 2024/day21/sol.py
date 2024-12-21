#!/usr/bin/env python3

import itertools
from functools import cache
from os import path
from typing import Iterable


RIGHT, DOWN, LEFT, UP, ACTIVATE = range(5)
DIR_TO_DELTA = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}
ROBO_BUTTON_TO_POS = {
    UP: (1, 0),
    ACTIVATE: (2, 0),
    LEFT: (0, 1),
    DOWN: (1, 1),
    RIGHT: (2, 1),
}
DOOR_BUTTON_TO_POS = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}


def paths_from_to(
    sx: int, sy: int, ex: int, ey: int, on_door: bool
) -> Iterable[tuple[int]]:
    dx, dy = ex - sx, ey - sy

    moves = []
    if dx > 0:
        moves += [RIGHT] * dx
    elif dx < 0:
        moves += [LEFT] * -dx
    if dy > 0:
        moves += [DOWN] * dy
    elif dy < 0:
        moves += [UP] * -dy

    if is_valid_path(sx, sy, moves, on_door):
        yield tuple(moves)

    moves.reverse()
    if is_valid_path(sx, sy, moves, on_door):
        yield tuple(moves)


def is_valid_path(x: int, y: int, moves: list[int], on_door: bool) -> bool:
    for m in moves:
        dx, dy = DIR_TO_DELTA[m]
        x, y = x + dx, y + dy
        if on_door:
            if x == 0 and y == 3:
                return False
        elif x == 0 and y == 0:
            return False
    return True


@cache
def presses_to_move_and_then_activate(moves: tuple[int], level: int) -> int:
    if level == 0:
        return len(moves) + 1

    presses = 0
    x, y = ROBO_BUTTON_TO_POS[ACTIVATE]
    for b in itertools.chain(moves, [ACTIVATE]):
        tx, ty = ROBO_BUTTON_TO_POS[b]
        presses += min(
            presses_to_move_and_then_activate(moves, level - 1)
            for moves in paths_from_to(x, y, tx, ty, False)
        )
        x, y = tx, ty
    return presses


def code_complexity(code: str, levels: int) -> int:
    presses = 0
    x, y = DOOR_BUTTON_TO_POS["A"]
    for b in code:
        tx, ty = DOOR_BUTTON_TO_POS[b]
        presses += min(
            presses_to_move_and_then_activate(moves, levels)
            for moves in paths_from_to(x, y, tx, ty, True)
        )
        x, y = tx, ty
    return presses * int(code[:-1])


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    part1 = part2 = 0

    for code in file.read().splitlines():
        part1 += code_complexity(code, 2)
        part2 += code_complexity(code, 25)

    print("Part 1:", part1)
    print("Part 2:", part2)
