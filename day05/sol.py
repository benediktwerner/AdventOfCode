#!/usr/bin/env python3

from string import ascii_lowercase


def retract(poly, exclude=None):
    poly = (ord(c) for c in poly if c != exclude and c.lower() != exclude)
    stack = []

    for c in poly:
        if stack and abs(stack[-1] - c) == 32:
            stack.pop()
        else:
            stack.append(c)

    return len(stack)


def main():
    with open("input.txt") as f:
        poly = f.readline().strip()

    print("Part 1:", retract(poly))

    reduced = [retract(poly, c) for c in ascii_lowercase]

    print("Part 2:", min(reduced))


if __name__ == "__main__":
    main()
