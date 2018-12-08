#!/usr/bin/env python3

import os
from sys import argv


TEMPLATE = """\
#!/usr/bin/env python3

from collections import defaultdict


def main():
    with open("input.txt") as f:
        for line in f:
            pass


if __name__ == "__main__":
    main()
"""


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
os.makedirs(dir_name, exist_ok=True)

with open(os.path.join(dir_name, "sol.py"), "w") as f:
    f.write(TEMPLATE)
