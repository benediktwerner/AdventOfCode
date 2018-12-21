#!/usr/bin/env python3


MOVES = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


def main():
    with open("input.txt") as f:
        instructions = f.readline().strip().split(", ")

    x = 0
    y = 0
    angle = 0
    seen = set()
    part1_solved = False
    part2_solved = False

    while True:
        for instr in instructions:
            turn, steps = instr[0], int(instr[1:])
            angle = (angle + (1 if turn == "R" else -1)) % 4
            xd, yd = MOVES[angle]

            for _ in range(steps):
                if not part2_solved and (x, y) in seen:
                    part2_solved = True
                    print("Part 2:", abs(x) + abs(y))
                else:
                    seen.add((x, y))

                x += xd
                y += yd

        if not part1_solved:
            part1_solved = True
            print("Part 1:", abs(x) + abs(y))
        elif part2_solved:
            return


if __name__ == "__main__":
    main()
