#!/usr/bin/env python3

import os


def decompressed_length(line, start=0, end=None, recurse=True):
    count = 0
    i = start
    if end is None:
        end = len(line)

    while i < end:
        if line[i] == "(":
            marker = ""
            while True:
                i += 1
                if line[i] == ")":
                    break
                marker += line[i]
            i += 1
            length, repeat = map(int, marker.split("x"))
            if recurse:
                total_length = decompressed_length(line, i, i + length)
            else:
                total_length = length
            count += total_length * repeat
            i += length
        else:
            count += 1
            i += 1

    return count


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        line = f.readline().strip()

        print("Part 1:", decompressed_length(line, recurse=False))
        print("Part 2:", decompressed_length(line))


if __name__ == "__main__":
    main()
