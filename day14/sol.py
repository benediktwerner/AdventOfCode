#!/usr/bin/env python3

from collections import defaultdict


def compare(recepies, seq, space_from_behind):
    if len(recepies) < len(seq) + space_from_behind:
        return False

    for i, x in enumerate(seq):
        if recepies[-len(seq) - space_from_behind + i] != x:
            return False

    print("Part 2:", len(recepies) - len(seq) - space_from_behind)
    return True


def main():
    recepies = [3, 7]
    one = 0
    two = 1

    with open("input.txt") as f:
        line = f.readline().strip()
        count = int(line)
        seq = tuple(int(c) for c in line)

    part1 = False
    part2 = False

    while not part1 or not part2:
        new = recepies[one] + recepies[two]
        if new >= 10:
            recepies.append(new // 10)
            recepies.append(new % 10)
            if not part2 and compare(recepies, seq, 1):
                part2 = True
        else:
            recepies.append(new)

        if not part2 and compare(recepies, seq, 0):
            part2 = True

        one = (one + 1 + recepies[one]) % len(recepies)
        two = (two + 1 + recepies[two]) % len(recepies)

        if not part1 and len(recepies) >= count + 10:
            print("Part 1:", "".join(str(x) for x in recepies[count:count+10]))
            part1 = True


if __name__ == "__main__":
    main()
