#!/usr/bin/env python3

import os

WIDTH = 25
HEIGHT = 6
SIZE = WIDTH * HEIGHT

BLACK = 0
WHITE = 1
TRANSPARENT = 2

with open(os.path.dirname(__file__) + "/input.txt") as f:
    line = f.readline().strip()
    pixels_iter = iter(line)

    min_zeros = float("inf")
    part1 = 0
    image = [[TRANSPARENT] * WIDTH for _ in range(HEIGHT)]

    for _ in range(len(line) // SIZE):
        count = [0] * 3

        for y in range(HEIGHT):
            for x in range(WIDTH):
                pixel = int(next(pixels_iter))
                count[pixel] += 1

                if image[y][x] == TRANSPARENT:
                    image[y][x] = pixel

        if count[0] < min_zeros:
            min_zeros = count[0]
            part1 = count[1] * count[2]

    print("Part 1:", part1)
    print("Part 2:")

    for row in image:
        print("".join("#" if c == WHITE else " " for c in row))
