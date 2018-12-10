#!/usr/bin/env python3

import os
import requests
from sys import argv


YEAR = 2018
URL = "https://adventofcode.com/{year}/day/{day}/input"


if len(argv) != 2:
    print("Usage:", argv[0], "DAY")
    exit(1)

try:
    day = int(argv[1])
except ValueError:
    print("Error: DAY is not a number")
    print("Usage:", argv[0], "DAY")
    exit(1)


dir_name = "day{:02}".format(day)
cookies = {}

with open("cookie") as f:
    cookies["session"] = f.read().strip()

target_file = os.path.join(dir_name, "input.txt")

with open(target_file, "w") as f:
    url = URL.format(year=YEAR, day=argv[1])
    req = requests.get(url, cookies=cookies)
    f.write(req.text)

print("Input for", dir_name, "written to", target_file)
