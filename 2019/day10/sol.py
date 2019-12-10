#!/usr/bin/env python3

import os
import math


def dist(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


with open(os.path.dirname(__file__) + "/input.txt") as f:
    astroids = []

    for y, line in enumerate(f):
        for x, c in enumerate(line.strip()):
            if c == "#":
                astroids.append((x, y))

    best_count = 0
    best_pos = None

    for pos in astroids:
        x, y = pos
        count = 0
        angles = {(ax, ay): math.atan2(ay - y, ax - x) for ax, ay in astroids}
        for a in astroids:
            for b in astroids:
                if angles[a] == angles[b] and dist(a, pos) > dist(b, pos):
                    break
            else:
                count += 1
        if count > best_count:
            best_count = count
            best_pos = pos

    print("Part 1:", best_count)

    x, y = best_pos
    laser_angle = math.degrees(math.atan2(-1, 0)) % 360
    angles = {
        (ax, ay): math.degrees(math.atan2(ay - y, ax - x)) % 360 for ax, ay in astroids
    }

    i = 0
    while astroids:
        a = min(
            astroids,
            key=lambda a: ((angles[a] - laser_angle) % 360) * 10000000
            + dist(a, best_pos),
        )

        i += 1
        if i == 200:
            print("Part 2:", a[0] * 100 + a[1])
            break

        laser_angle = (angles[a] + 0.001) % 360
        astroids.remove(a)
