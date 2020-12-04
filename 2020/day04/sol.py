#!/usr/bin/env python3

from os import path
import re


REQUIREMENTS = [
    ("byr", lambda x: 1920 <= int(x) <= 2002),
    ("iyr", lambda x: 2010 <= int(x) <= 2020),
    ("eyr", lambda x: 2020 <= int(x) <= 2030),
    (
        "hgt",
        lambda x: (x[-2:] == "cm" and 150 <= int(x[:-2]) <= 193)
        or (x[-2:] == "in" and 59 <= int(x[:-2]) <= 76),
    ),
    ("hcl", lambda x: re.fullmatch(r"#[0-9a-f]{6}", x)),
    ("ecl", lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")),
    ("pid", lambda x: re.fullmatch(r"[0-9]{9}", x)),
]


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1 = part2 = 0

    for passport_lines in f.read().split("\n\n"):
        passport = {}

        for line in passport_lines.splitlines():
            for parts in line.split():
                key, value = parts.split(":")
                passport[key] = value

        valid1 = True
        valid2 = True

        for key, req in REQUIREMENTS:
            if key not in passport:
                valid1 = False
                break

            if not req(passport[key]):
                valid2 = False

        if valid1:
            part1 += 1
            part2 += valid2

    print("Part 1:", part1)
    print("Part 2:", part2)
