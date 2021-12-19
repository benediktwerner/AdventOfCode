#!/usr/bin/env python3

from os import path
import re


def valid(pwd):
    for a, b, c in zip(pwd, pwd[1:], pwd[2:]):
        if ord(a) + 1 == ord(b) == ord(c) - 1:
            break
    else:
        return False
    return (
        all(c not in ("i", "o", "l") for c in pwd)
        and len(re.findall(r"(.)\1", pwd)) >= 2
    )


def nxt(pwd):
    while True:
        new = ""
        inc = True
        for c in reversed(pwd):
            if inc:
                if c == "z":
                    new = "a" + new
                else:
                    inc = False
                    new = chr(ord(c) + 1) + new
            else:
                new = c + new
        pwd = new
        if valid(pwd):
            return pwd


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    pwd = nxt(f.read().strip())
    print("Part 1:", pwd)
    print("Part 2:", nxt(pwd))
