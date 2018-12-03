#!/usr/bin/env python3

from collections import Counter


def main():
    two = 0
    three = 0
    ids = []

    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            ids.append(line)

            c = Counter(line)
            if 2 in c.values():
                two += 1
            if 3 in c.values():
                three += 1

    print("Part 1:", two * three)

    for i, val in enumerate(ids):
        for other in ids[i+1:]:
            diff = 0
            for k in range(len(val)):
                if val[k] != other[k]:
                    if diff != 0:
                        break
                    diff = k + 1
            else:
                print("Part 2:", val[:diff-1] + val[diff:])
                return


if __name__ == "__main__":
    main()
