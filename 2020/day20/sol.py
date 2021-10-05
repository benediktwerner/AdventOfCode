#!/usr/bin/env python3

from os import path
from operator import mul
from functools import reduce
from collections import defaultdict
import re


MONSTER_PATTERN = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
MONSTER = []
for y, row in enumerate(MONSTER_PATTERN):
    for x, c in enumerate(row):
        if c == "#":
            MONSTER.append((x, y))
MONSTER_WIDTH = len(MONSTER_PATTERN[0])
MONSTER_HEIGHT = len(MONSTER_PATTERN)


def orientate(border):
    b = border.replace("#", "1").replace(".", "0")
    flipped = "".join(reversed(b))
    if int(b, 2) > int(flipped, 2):
        return "".join(reversed(border)), True
    return border, False


def find_monsters(pic):
    monsters = []
    for y in range(len(pic) - MONSTER_HEIGHT):
        for x in range(len(pic[0]) - MONSTER_WIDTH):
            for xd, yd in MONSTER:
                if pic[y + yd][x + xd] != "#":
                    break
            else:
                monsters.append((x, y))
    return monsters


def rotate(pic):
    result = []
    for y in range(len(pic)):
        row = ""
        for x in range(len(pic)):
            row += pic[len(pic) - x - 1][y]
        result.append(row)
    return result


def flip_pic(pic):
    result = []
    for y in range(len(pic)):
        row = ""
        for x in range(len(pic)):
            row += pic[y][len(pic) - x - 1]
        result.append(row)
    return result


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = (line.strip() for line in f)
    tiles = defaultdict(list)
    for line in lines:
        id = int(re.findall(r"[0-9]+", line)[0])
        for line in lines:
            if not line:
                break
            tiles[id].append(line)

    tile_borders = {}
    for id, tile in tiles.items():
        bs = [tile[0], "", "".join(reversed(tile[-1])), ""]
        for line in tile:
            bs[1] += line[-1]
            bs[3] = line[0] + bs[3]
        tile_borders[id] = list(map(orientate, bs))

    borders = defaultdict(list)
    for id, bs in tile_borders.items():
        for i, (b, flip) in enumerate(bs):
            borders[b].append((id, i, flip))

    edge_count = defaultdict(int)
    for occ in borders.values():
        if len(occ) == 1:
            edge_count[occ[0][0]] += 1

    corners = [k for k, v in edge_count.items() if v == 2]
    print("Part 1:", reduce(mul, corners, 1))

    corner = corners[0]
    up = {"1001": 0, "1100": 1, "0110": 2, "0011": 3}[
        "".join(str(int(len(borders[b]) == 1)) for b, *_ in tile_borders[corner])
    ]
    pattern = []
    size = int(len(tiles) ** 0.5)

    while len(pattern) < size:
        if not pattern:
            row = [(corner, up, False)]
        else:
            id, up, flipped = pattern[-1][0]
            b, b_flipped = tile_borders[id][(up + 2) % 4]
            same = borders[b]
            new_id, new_b_index, new_b_flipped = same[same[0][0] == id]
            flip = (flipped ^ b_flipped) == new_b_flipped
            row = [(new_id, new_b_index, flip)]

        pattern.append(row)

        while len(row) < size:
            id, up, flipped = row[-1]
            b, b_flipped = tile_borders[id][(up + (not flipped) - flipped) % 4]
            same = borders[b]
            new_id, new_b_index, new_b_flipped = same[same[0][0] == id]
            flip = (flipped ^ b_flipped) == new_b_flipped
            row.append((new_id, (new_b_index + (not flip) - flip) % 4, flip))

    picture = [""] * size * 8
    for i, row in enumerate(pattern):
        for id, up, flipped in row:
            x, y = [(1, 1), (8, 1), (8, 8), (1, 8), (8, 1), (8, 8), (1, 8), (1, 1)][
                up + flipped * 4
            ]
            delta_x = [
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
            ][up + flipped * 4]
            delta_y = [(0, 1), (-1, 0), (0, -1), (1, 0)][up]

            for yd in range(8):
                for xd in range(8):
                    picture[i * 8 + yd] += tiles[id][
                        y + delta_x[1] * xd + delta_y[1] * yd
                    ][x + delta_x[0] * xd + delta_y[0] * yd]

    for _ in range(2):
        for _ in range(4):
            monsters = find_monsters(picture)
            if monsters:
                sharps = set()
                for y, row in enumerate(picture):
                    for x, c in enumerate(row):
                        if c == "#":
                            sharps.add((x, y))
                for x, y in monsters:
                    for xd, yd in MONSTER:
                        sharps.remove((x + xd, y + yd))
                print("Part 2:", len(sharps))
            picture = rotate(picture)
        picture = flip_pic(picture)
