#!/usr/bin/env python3

import os
import hashlib
from collections import deque


def md5(index, stretch):
    h = hashlib.md5(salt + str(index).encode()).hexdigest()
    for _ in range(stretch):
        h = hashlib.md5(h.encode()).hexdigest()
    return h


def triple(s):
    for a, b, c in zip(s, s[1:], s[2:]):
        if a == b == c:
            return a
    return None


def quint(s, k):
    for a, b, c, d, e in zip(s, s[1:], s[2:], s[3:], s[4:]):
        if k == a == b == c == d == e:
            return True
    return False


def find(stretch):
    index = 0
    hashes = deque([md5(i, stretch) for i in range(1000)])

    for _ in range(64):
        while True:
            h = hashes.popleft()
            hashes.append(md5(index + 1000, stretch))
            trip = triple(h)
            index += 1
            if trip is not None and any(quint(h, trip) for h in hashes):
                break

    return index - 1


with open(os.path.dirname(__file__) + "/input.txt") as f:
    salt = f.readline().strip().encode()

    print("Part 1:", find(0))
    print("Part 1:", find(2016))
