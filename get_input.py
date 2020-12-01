#!/usr/bin/env python3

import os
import requests
from datetime import datetime
from sys import argv


URL = "https://adventofcode.com/{year}/day/{day}/input"


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
        print("Failed to deduce day: There is no new AoC puzzle today.")
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
cookies = {}

try:
    with open("cookie") as f:
        cookies["session"] = f.read().strip()
except FileNotFoundError:
    print("No cookie file found.")
    print("Please paste the value of the 'session' cookie on the AoC website into a file named 'cookie'.")
    exit(2)

os.makedirs(dir_name, exist_ok=True)
target_file = os.path.join(dir_name, "input.txt")

url = URL.format(year=year, day=day)
req = requests.get(url, cookies=cookies)

if req.status_code != 200:
    print("Error. Got status:", req.status_code)
    print(req.text)
    exit(3)
else:
    with open(target_file, "w") as f:
        f.write(req.text)
    print("Input for", dir_name, "written to", target_file)
