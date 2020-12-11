#!/usr/bin/env python3

from os import path

def solve(seats, neighbors, occ):
    neighbor_count = {}
    change = True

    while change:
        change = False

        for seat in seats.keys():
            neighbor_count[seat] = sum(seats[n] == "#" for n in neighbors[seat])

        for c, seat in seats.items():
            if seat == "L":
                if neighbor_count[c] == 0:
                    seats[c] = "#"
                    change = True
            elif seat == "#":
                if neighbor_count[c] >= occ:
                    seats[c] = "L"
                    change = True

    return sum(seat == "#" for seat in seats.values())

with open(path.join(path.dirname(__file__), "input.txt")) as f:
    grid = [list(line.strip()) for line in f]
    seats = {}
    neighbors1 = {}
    neighbors2 = {}

    for y, line in enumerate(grid):
        for x, seat in enumerate(line):
            if seat == ".":
                continue

            seats[x, y] = seat
            curr_neighbors1 = []
            curr_neighbors2 = []

            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    if dx == 0 and dy == 0:
                        continue

                    nx = x+dx
                    ny = y+dy

                    if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                        if grid[ny][nx] in ("#", "L"):
                            curr_neighbors1.append((nx, ny))

                    while 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                        if grid[ny][nx] in ("#", "L"):
                            curr_neighbors2.append((nx, ny))
                            break

                        nx += dx
                        ny += dy

            neighbors1[x, y] = curr_neighbors1
            neighbors2[x, y] = curr_neighbors2
    
    print("Part 1:", solve(seats.copy(), neighbors1, 4))
    print("Part 2:", solve(seats, neighbors2, 5))
