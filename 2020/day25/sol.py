#!/usr/bin/env python3

from os import path
from itertools import count


def transform(subj, loop_size):
    val = 1
    for _ in range(loop_size):
        val *= subj
        val %= 20201227
    return val


def find_loop_size(subj, res):
    val = 1
    for loop_size in count(0):
        if val == res:
            return loop_size
        val *= subj
        val %= 20201227


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    pub1, pub2, = (int(x) for x in f.read().splitlines())
    loop1 = find_loop_size(7, pub1)
    loop2 = find_loop_size(7, pub2)
    print("Part 1:", transform(pub2, loop1))
