#!/usr/bin/env python3

from os import path
import itertools
import re


def ints(string):
    return list(map(int, re.findall(r"-?[0-9]+", string)))


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    row, column = ints(f.read())
    val = 20151125
    for diag in itertools.count(1):
        r, c = diag, 1
        for _ in range(diag):
            val = (val * 252533) % 33554393
            r -= 1
            c += 1
            if r == row and c == column:
                print("Part 1:", val)
                exit()
