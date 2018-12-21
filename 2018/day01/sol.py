#!/usr/bin/env python3


def main():
    values = []
    with open("input.txt") as f:
        for line in f:
            values.append(int(line))

    print("Part 1:", sum(values))

    seen = set([0])
    value = 0
    while True:
        for val in values:
            value += val
            if value in seen:
                print("Part 2:", value)
                return
            seen.add(value)


if __name__ == "__main__":
    main()
