#!/usr/bin/env python3

from os import path


NUMBERS_PART_1 = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}

NUMBERS_PART_2 = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def try_parse(line: str, numbers: dict[str, int]) -> int | None:
    for num, value in numbers.items():
        if line.startswith(num):
            return value


def solve(lines: list[str], numbers: dict[str, int]):
    result = 0
    for line in lines:
        for i in range(len(line)):
            value = try_parse(line[i:], numbers)
            if value is not None:
                result += value * 10
                break

        for i in reversed(range(len(line))):
            value = try_parse(line[i:], numbers)
            if value is not None:
                result += value
                break

    return result


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    print("Part 1:", solve(lines, NUMBERS_PART_1))
    print("Part 2:", solve(lines, NUMBERS_PART_1 | NUMBERS_PART_2))
