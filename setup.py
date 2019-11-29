#!/usr/bin/env python3

import os
from datetime import datetime
from sys import argv


TEMPLATE = """\
#!/usr/bin/env python3

from collections import *
from networkx import *
import re


def ints(s):
    return list(map(int, re.findall(r"-?\d+", s)))


def main():
    with open(__file__.rstrip("sol.py") + "input.txt") as f:
        lines = f.read().strip().splitlines()
        for line in lines:
            pass


if __name__ == "__main__":
    main()
"""


def print_usage():
    print("Usage:", argv[0], "[YEAR] DAY")
    exit(1)


def arg_to_int(i, name):
    try:
        return int(argv[i])
    except ValueError:
        print("Error:", name, "is not a number")
        print_usage()


if len(argv) == 2:
    year = datetime.now().year
    day = arg_to_int(1, "DAY")
elif len(argv) == 3:
    year = arg_to_int(1, "YEAR")
    day = arg_to_int(2, "DAY")
else:
    print_usage()


dir_name = "{}/day{:02}".format(year, day)
os.makedirs(dir_name, exist_ok=True)
print("Created directory", dir_name)

with open(os.path.join(dir_name, "sol.py"), "w") as f:
    f.write(TEMPLATE)

print("Created sol.py template")
