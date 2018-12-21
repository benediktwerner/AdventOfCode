#!/usr/bin/env python3


MOVES = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0)
}

BUTTONS = [[
    [0,  0,   0,   0,  0],
    [0, "1", "2", "3", 0],
    [0, "4", "5", "6", 0],
    [0, "7", "8", "9", 0],
    [0,  0,   0,   0,  0],
], [
    [0,  0,   0,   0,   0,   0,  0],
    [0,  0,   0,  "1",  0,   0,  0],
    [0,  0,  "2", "3", "4",  0,  0],
    [0, "5", "6", "7", "8", "9", 0],
    [0,  0,  "A", "B", "C",  0,  0],
    [0,  0,   0,  "D",  0,   0,  0],
    [0,  0,   0,   0,   0,   0,  0],
]]


def main():
    instructions = []

    with open("input.txt") as f:
        instructions = list(f)

    for part in range(2):
        x = len(BUTTONS[part]) // 2 + 1
        y = len(BUTTONS[part]) // 2 + 1
        code = ""

        for line in instructions:
            for c in line.strip():
                xd, yd = MOVES[c]
                if BUTTONS[part][y + yd][x + xd] != 0:
                    x += xd
                    y += yd
            code += BUTTONS[part][y][x]
        print("Part {}: {}".format(part+1, code))


if __name__ == "__main__":
    main()
