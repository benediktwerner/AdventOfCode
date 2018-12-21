#!/usr/bin/env python3

import re
from collections import Counter


def decrypt(name, shift):
    result = ""
    for c in name:
        if c == "-":
            result += " "
        else:
            c = (ord(c) + shift % 26)
            if c > ord("z"):
                c -= 26
            result += chr(c)
    return result


def main():
    rooms = []

    with open("input.txt") as f:
        for line in f:
            name, room_id, checksum = re.findall(r"(.*?)-(\d+?)\[(.*?)\]", line.strip())[0]
            rooms.append((name, int(room_id), checksum))

    count = 0
    for name, room_id, checksum in rooms:
        c = Counter(name.replace("-", ""))
        most_common = sorted(c.most_common(), key=lambda x: -x[1] * 1000 + ord(x[0]))
        most_common = "".join(x[0] for x in most_common[:5])
        if most_common == checksum:
            count += room_id

        name = decrypt(name, room_id)
        if "north" in name:
            print("Part 2:", name, room_id)

    print("Part 1:", count)


if __name__ == "__main__":
    main()
