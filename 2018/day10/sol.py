#!/usr/bin/env python3

import re
from collections import defaultdict


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, velocity):
        self.x += velocity.x
        self.y += velocity.y


class Light:
    def __init__(self, line):
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        self.pos = Vector(x, y)
        self.velocity = Vector(vx, vy)

    def move(self):
        self.pos.move(self.velocity)


def print_lights(lights):
    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")

    for light in lights:
        if light.pos.x < min_x:
            min_x = light.pos.x
        if light.pos.y < min_y:
            min_y = light.pos.y
        if light.pos.x > max_x:
            max_x = light.pos.x
        if light.pos.y > max_y:
            max_y = light.pos.y

    if (max_y - min_y) > 10:
        return False

    positions = defaultdict(bool)
    for light in lights:
        positions[(light.pos.x, light.pos.y)] = True

    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x+1):
            line += "#" if positions[(x, y)] else " "
        print(line)

    return True


def main():
    lights = []

    with open("input.txt") as f:
        for line in f:
            lights.append(Light(line))

    seconds = 0

    while True:
        for light in lights:
            light.move()

        seconds += 1

        if print_lights(lights):
            print("\nPart 2:", seconds)
            break


if __name__ == "__main__":
    main()
