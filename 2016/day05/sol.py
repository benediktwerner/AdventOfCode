#!/usr/bin/env python3

from hashlib import md5
import random
import string


def print_pwd(pwd):
    print("".join(random.choice(string.hexdigits) if c is None else c for c in pwd), flush=True, end="\r")

def main():
    with open("input.txt") as f:
        door_id = f.readline().strip()

        pwd = [None] * 8
        i = 0
        print("Part 1:")

        for pos in range(8):
            while True:
                h = md5((door_id + str(i)).encode()).hexdigest()
                i += 1
                if h[:5] == "00000":
                    pwd[pos] = h[5]
                    print_pwd(pwd)
                    break
                elif i % 100_000 == 0:
                    print_pwd(pwd)

        print()
        print("Part 2:")

        pwd = [None] * 8
        found = 0
        i = 0

        while found < 8:
            while True:
                h = md5((door_id + str(i)).encode()).hexdigest()
                i += 1
                if h[:5] == "00000":
                    pos = int(h[5], 16)
                    if pos < 8 and pwd[pos] is None:
                        pwd[pos] = h[6]
                        found += 1
                        print_pwd(pwd)
                    break
                elif i % 100_000 == 0:
                    print_pwd(pwd)

        print()


if __name__ == "__main__":
    main()
