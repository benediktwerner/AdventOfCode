#!/usr/bin/env python3

import os
import shutil
from datetime import datetime
from sys import argv


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = "template.py"
TEMPLATE_PATH = os.path.join(BASE_DIR, TEMPLATE_FILE)


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


dir_name = os.path.join(BASE_DIR, str(year), f"day{day:02}")
os.makedirs(dir_name, exist_ok=True)

target_path = os.path.join(dir_name, "sol.py")
if os.path.exists(target_path):
    print("ERROR:", target_path,"exists already")
else:
    shutil.copy(TEMPLATE_PATH, target_path)
    print("Created", target_path)
