#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import itertools
import math
import re
import pyperclip


def ints(string):
    return map(int, re.findall(r"-?[0-9]+", string))

def reg(pattern, string):
    rega(pattern, string)[0]

def rega(pattern, string):
    pattern = pattern.replace(r"\#", "\x80")
    pattern = pattern.replace(r"\$", "\x81")
    pattern = pattern.replace("#", r"([a-zA-Z]+)")
    pattern = pattern.replace("$", r"([0-9]+)")
    pattern = pattern.replace("\x80", "#")
    pattern = pattern.replace("\x81", "$")
    return re.findall(pattern, string)

def out(result):
    print("Output:", result)
    pyperclip.copy(str(result))
    print("Copied to clipboard")


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    for line in f:
        line = line.strip()
