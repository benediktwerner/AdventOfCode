#!/usr/bin/env python3

import os
from datetime import datetime
from sys import argv


TEMPLATE = """\
#!/usr/bin/env python3

from os import path
from collections import *
from networkx import *
import itertools
import math
import re
import pyperclip


def out(result):
    print("Output:", result)
    pyperclip.copy(str(result))
    print("Copied to clipboard")


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    for line in f:
        line = line.strip()

"""


def print_usage():
    print("Usage:", argv[0], "[[YEAR] DAY]")
    exit(1)


def arg_to_int(i, name):
    try:
        return int(argv[i])
    except ValueError:
        print("Error:", name, "is not a number")
        print_usage()


if len(argv) == 1:
    now = datetime.now()
    if now.month != 12 or now.day > 25:
        print("Failed to deduce day: There is no new AoC puzzle today!")
        print_usage()
    year = now.year
    day = now.day
elif "-h" in argv[1:] or "--help" in argv[1:]:
    print_usage()
elif len(argv) == 2:
    day = arg_to_int(1, "DAY")
    now = datetime.now()
    year = now.year
    if now.month < 12:
        year -= 1
elif len(argv) == 3:
    year = arg_to_int(1, "YEAR")
    day = arg_to_int(2, "DAY")
else:
    print_usage()


dir_name = "{}/day{:02}".format(year, day)
os.makedirs(dir_name, exist_ok=True)

target_path = os.path.join(dir_name, "sol.py")
if os.path.exists(target_path):
    print("ERROR:", target_path,"exists already")
else:
    with open(target_path, "w") as f:
        f.write(TEMPLATE)

    print("Created", target_path)
