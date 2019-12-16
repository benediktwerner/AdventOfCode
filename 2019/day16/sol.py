#!/usr/bin/env python3

from os import path
from collections import *
import itertools
import math


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp = f.readline().strip()

    digits = list(map(int, inp))
    for _ in range(100):
        for i in range(len(digits)):
            val = 0
            for j, d in enumerate(digits[i:], i):
                val += d * (0,1,0,-1)[(j+1) // (i+1) % 4]
            digits[i] = int(str(val)[-1])
    
    print("Part 1: ", *digits[:8], sep="")

    digits = list(map(int, inp))
    digits *= 10000
    offset = int(inp[:7])

    for _ in range(100):
        for i in reversed(range(offset, len(digits)-1)):
            digits[i] = (digits[i] + digits[i+1]) % 10

    print("Part 2: ", *digits[offset:offset+8], sep="")
