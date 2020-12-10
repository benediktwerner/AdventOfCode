#!/usr/bin/env python3

from collections import defaultdict

COLORS = [
    "aqua",
    "beige",
    "black",
    "blue",
    "bronze",
    "brown",
    "chartreuse",
    "coral",
    "crimson",
    "cyan",
    "fuchsia",
    "gold",
    "gray",
    "green",
    "indigo",
    "lavender",
    "lime",
    "magenta",
    "maroon",
    "olive",
    "orange",
    "plum",
    "purple",
    "red",
    "salmon",
    "silver",
    "tan",
    "teal",
    "tomato",
    "turquoise",
    "violet",
    "white",
    "yellow",
]

ATTRIBUTES = [
    "bright",
    "clear",
    "dark",
    "dim",
    "dotted",
    "drab",
    "dull",
    "faded",
    "light",
    "mirrored",
    "muted",
    "pale",
    "plaid",
    "posh",
    "shiny",
    "striped",
    "vibrant",
    "wavy",
]


def group_by(i, options):
    groups = defaultdict(list)
    for word in options:
        groups[word[i]].append(word)
    return list(groups.items())


def group_optimal(options, used=None):
    if used is None:
        used = set()

    if len(options) == 1:
        return (None, options[0]), 0

    length = min(map(len, options))
    min_depth = float("inf")
    min_grouping = None
    for i in range(length):
        if i in used:
            continue
        groups = group_by(i, options)
        max_depth = 0
        used.add(i)
        for j, (letter, group) in enumerate(groups):
            group, depth = group_optimal(group, used)
            groups[j] = (letter, group)
            max_depth = max(max_depth, depth + 1)
        used.remove(i)
        if max_depth < min_depth:
            min_depth = max_depth
            min_grouping = (i, groups)

    assert min_grouping is not None

    return min_grouping, min_depth


def gen(options: list):
    options.sort()
    grouping, depth = group_optimal(options)

    print(f"Found grouping with depth {depth}:")
    print_grouping(grouping)
    print("=" * 40)
    print_grouping_code(grouping)


def print_grouping(grouping, indent=-1, result=0):
    index, groups = grouping
    print("Group by", index)
    indent += 2
    for group in groups:
        letter, group = group
        print(" " * indent, letter, "=>", end=" ")
        if group[0] is None:
            print(group[1], "=", result)
            result += 1
        else:
            result = print_grouping(group, indent, result)
    return result


def print_grouping_code(grouping, indent=0, result=1):
    index, groups = grouping
    print(f"match bytes[{index}] {{", sep="")
    indent += 4
    for i, group in enumerate(groups):
        letter, group = group

        if i < len(groups) - 1:
            print(" " * indent, f"b'{letter}' => ", end="", sep="")
        else:
            print(" " * indent, "_ => ", end="", sep="")

        if group[0] is None:
            word = group[1]
            print(f"({result}, {len(word)}), // {word}")
            result += 1
        else:
            result = print_grouping_code(group, indent, result)

    indent -= 4
    print(" " * indent, "}", sep="")

    return result


# gen(ATTRIBUTES)

import struct
MOD = 215

table = []

for c in COLORS:
    h = struct.unpack("<I", c.ljust(4)[:4].encode())[0]
    h %= MOD
    table.append((h, c))

print("// Colors")

for i, (h, c) in enumerate(table, 1):
    print(f"COLOR_TABLE[{h}] = ({i}, {len(c)}); // {c}")

table = []

for attr in ATTRIBUTES:
    a = ord(attr[0]) & 0b11111
    b = ord(attr[1]) & 0b11111
    h = (a << 5) | b
    table.append((h, attr))

print("// Attributes")

for i, (h, c) in enumerate(table, 1):
    print(f"ATTRIBUTES_TABLE[{h}] = ({i}, {len(c)}); // {c}")
