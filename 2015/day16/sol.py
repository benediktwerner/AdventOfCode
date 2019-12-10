#!/usr/bin/env python3

from os import path


def main():
    with open(path.join(path.dirname(__file__), "input.txt")) as f:
        attrs = {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1,
        }

        for line in f:
            line = line.strip()

            x = line.find(":")
            aunt = int(line[4:x])
            aunt_attrs = {
                a.split(": ")[0]: int(a.split(": ")[1])
                for a in line[x + 2 :].split(", ")
            }

            for k, v in attrs.items():
                if k in aunt_attrs and aunt_attrs[k] != v:
                    break
            else:
                print("Part 1:", aunt)

            for k, v in attrs.items():
                if k in aunt_attrs:
                    if k in ("cats", "trees"):
                        if aunt_attrs[k] <= v:
                            break
                    elif k in ("pomeranians", "goldfish"):
                        if aunt_attrs[k] >= v:
                            break
                    elif aunt_attrs[k] != v:
                        break
            else:
                print("Part 2:", aunt)


if __name__ == "__main__":
    main()
