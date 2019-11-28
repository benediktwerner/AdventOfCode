#!/usr/bin/env python3


def gen(line, length):
    while len(line) < length:
        line += "0" + "".join("1" if c == "0" else "0" for c in reversed(line))
    return line[:length]


def checksum(line):
    if len(line) % 2 == 1:
        return line

    out = ""

    for a, b in zip(line[::2], line[1::2]):
        if a == b:
            out += "1"
        else:
            out += "0"

    return checksum(out)


def main():
    with open(__file__.rstrip("sol.py") + "input.txt") as f:
        start = f.readline().strip()

        print("Part 1:", checksum(gen(start, 272)))
        print("Part 2:", checksum(gen(start, 35651584)))


if __name__ == "__main__":
    main()
