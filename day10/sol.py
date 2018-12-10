#!/usr/bin/env python3

from collections import defaultdict


class Vector:
    def __init__(self, cords):
        self.x, self.y = map(int, cords.split(","))

    def move(self, velocity):
        self.x += velocity.x
        self.y += velocity.y


class Light:
    def __init__(self, line):
        position, velocity = line.split("> ")
        self.pos = Vector(position.split("<")[1])
        self.velocity = Vector(velocity.split("<")[1][:-1])

    def move(self):
        self.pos.move(self.velocity)


def print_lights(lights):
    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")
    positions = defaultdict(bool)

    for light in lights:
        if light.pos.x < min_x:
            min_x = light.pos.x
        if light.pos.y < min_y:
            min_y = light.pos.y
        if light.pos.x > max_x:
            max_x = light.pos.x
        if light.pos.y > max_y:
            max_y = light.pos.y
        positions[(light.pos.x, light.pos.y)] = True

    if (max_x - min_x) > 100 or (max_y - min_y) > 10:
        return False

    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x+1):
            line += "#" if positions[(x, y)] else "."
        print(line)

    return True


def main():
    lights = []

    with open("input.txt") as f:
        for line in f:
            lights.append(Light(line.strip()))

    seconds = 0

    while True:
        for light in lights:
            light.move()

        seconds += 1

        if print_lights(lights):
            print("Part 2:", seconds)
            break


if __name__ == "__main__":
    main()
