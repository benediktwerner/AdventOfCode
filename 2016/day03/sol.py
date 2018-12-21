#!/usr/bin/env python3

import re


def main():
    numbers = []

    with open("input.txt") as f:
        for line in f:
            numbers.append(tuple(map(int, re.findall(r"(\d+) +(\d+) +(\d+)", line.strip())[0])))

    count = 0
    for vals in numbers:
        a, b, c = sorted(vals)
        if a + b > c:
            count += 1

    print("Part 1:", count)

    count = 0
    for i in range(len(numbers)):
        vals = (
            (numbers[(i // 3) * 3][i % 3]),
            (numbers[(i // 3) * 3 + 1][i % 3]),
            (numbers[(i // 3) * 3 + 2][i % 3])
        )

        a, b, c = sorted(vals)
        if a + b > c:
            count += 1

    print("Part 2:", count)


if __name__ == "__main__":
    main()
