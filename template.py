#!/usr/bin/env python3

from os import path
from collections import *
# from networkx import *
from copy import deepcopy
from tqdm import tqdm
import itertools
import math
import re
import pyperclip


def ints(string) -> list[int]:
    return list(map(int, re.findall(r"-?[0-9]+", string)))


def solve(inp: str):
    result = 0
    lines = inp.splitlines()
    for line in lines:
        pass
    return result


example = """\

"""

if example and not example.isspace():
    print("Example:", solve(example))
else:
    print("No example provided")

with open(path.join(path.dirname(__file__), "input.txt")) as file:
    result = solve(file.read())
    print("Output:", result)
    pyperclip.copy(str(result))
    print("Copied to clipboard")
