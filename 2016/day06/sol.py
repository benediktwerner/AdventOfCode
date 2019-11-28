#!/usr/bin/env python3


def main():
    with open("input.txt") as f:
        x = list(zip(*(line.strip() for line in f)))

        print("Part 1:", "".join(max(c, key=c.count) for c in x))
        print("Part 2:", "".join(min(c, key=c.count) for c in x))


if __name__ == "__main__":
    main()
