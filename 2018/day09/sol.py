#!/usr/bin/env python3

from collections import deque


def simulate(players, max_marble):
    circle = deque([0, 1])
    points = [0]*players
    player = 1

    for marble in range(2, max_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            points[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

        player = (player + 1) % players

    return max(points)


def main():
    with open("input.txt") as f:
        parts = f.readline().strip().split(" ")
        players = int(parts[0])
        max_marble = int(parts[6])

    print("Part 1:", simulate(players, max_marble))
    print("Part 2:", simulate(players, max_marble*100))


if __name__ == "__main__":
    main()
