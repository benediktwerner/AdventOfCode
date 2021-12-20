#!/usr/bin/env python3

from os import path


def simulate(pixels, outside_lit):
    minx = min(x for x, y in pixels)
    maxx = max(x for x, y in pixels)
    miny = min(y for x, y in pixels)
    maxy = max(y for x, y in pixels)
    new_pixels = set()

    for x in range(minx - 1, maxx + 2):
        for y in range(miny - 1, maxy + 2):
            l = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    l <<= 1
                    l |= ((nx, ny) in pixels) or (
                        outside_lit and not (minx <= nx <= maxx and miny <= ny <= maxy)
                    )
            if lookup[l] == "#":
                new_pixels.add((x, y))

    return new_pixels, lookup[-outside_lit] == "#"


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()
    lookup = lines[0]
    pixels = set()
    for y, line in enumerate(lines[2:]):
        for x, c in enumerate(line):
            if c == "#":
                pixels.add((x, y))

    outside_lit = False
    for _ in range(2):
        pixels, outside_lit = simulate(pixels, outside_lit)

    print("Part 1:", len(pixels))

    for _ in range(48):
        pixels, outside_lit = simulate(pixels, outside_lit)

    print("Part 2:", len(pixels))
