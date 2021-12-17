#!/usr/bin/env python3

from os import path
from hashlib import md5
from itertools import count


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    result = f.read().strip().encode()
    for i in count(1):
        if md5(result + str(i).encode()).hexdigest()[:5] == "00000":
            print("Part 1:", i)
            break
    for i in count(i):
        if md5(result + str(i).encode()).hexdigest()[:6] == "000000":
            print("Part 2:", i)
            break
