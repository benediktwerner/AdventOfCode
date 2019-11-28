#!/usr/bin/env python3

WIDTH = 50
HEIGHT = 6


def main():
    with open(__file__.rstrip("sol.py") + "input.txt") as f:
        screen = [[False] * WIDTH for _ in range(HEIGHT)]

        for line in f:
            line = line.strip()
            parts = line.split()

            if parts[0] == "rect":
                w, h = map(int, parts[1].split("x"))
                for x in range(w):
                    for y in range(h):
                        screen[y][x] = True
            elif parts[1] == "row":
                y = int(parts[2][2:])
                amount = int(parts[4])
                new = []
                for x in range(WIDTH):
                    new.append(screen[y][(x - amount) % WIDTH])
                for x in range(WIDTH):
                    screen[y][x] = new[x]
            else:
                x = int(parts[2][2:])
                amount = int(parts[4])
                new = []
                for y in range(HEIGHT):
                    new.append(screen[(y - amount) % HEIGHT][x])
                for y in range(HEIGHT):
                    screen[y][x] = new[y]

        print("Part 1:", sum(sum(row) for row in screen))
        print("Part 2:")
        for row in screen:
            print("".join("#" if c else " " for c in row))


if __name__ == "__main__":
    main()
