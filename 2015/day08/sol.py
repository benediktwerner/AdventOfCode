#!/usr/bin/env python3

from os import path
import ast
import json


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    code, decoded, encoded = 0, 0, 0
    for line in f.read().splitlines():
        code += len(line)
        decoded += len(ast.literal_eval(line))
        encoded += len(json.dumps(line))
    print("Part 1:", code - decoded)
    print("Part 2:", encoded - code)
