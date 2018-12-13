#!/usr/bin/env python3

from collections import defaultdict

POS_CHANGE_BY_DIRECTION = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


class Cart:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.direction = ("^", ">", "v", "<").index(c)
        self.direction_change = -1


def main():
    track = []
    carts = []
    with open("input.txt") as f:
        for y, line in enumerate(f):
            row = []
            for x, c in enumerate(line.strip("\n")):
                if c in ("-", "|", "+", "/", "\\", " "):
                    row.append(c)
                else:
                    carts.append(Cart(x, y, c))
                    if c in ("v", "^"):
                        row.append("|")
                    else:
                        row.append("-")
            track.append(row)

    first_removed = False
    while True:
        to_remove = []

        if len(carts) == 1:
            print("Part 2:", "{},{}".format(carts[0].x, carts[0].y))
            return

        for cart in sorted(carts, key=lambda c: c.y * 1000 + c.x):
            xd, yd = POS_CHANGE_BY_DIRECTION[cart.direction]
            cart.x += xd
            cart.y += yd

            t = track[cart.y][cart.x]
            if t == "+":
                cart.direction = (cart.direction + cart.direction_change) % 4
                cart.direction_change += 1
                if cart.direction_change == 2:
                    cart.direction_change = -1
            elif t == "/":
                cart.direction = (1, 0, 3, 2)[cart.direction]
            elif t == "\\":
                cart.direction = (3, 2, 1, 0)[cart.direction]

            for c in carts:
                if c != cart and c.x == cart.x and c.y == cart.y:
                    if not first_removed:
                        first_removed = True
                        print("Part 1:", "{},{}".format(c.x, c.y))
                    to_remove.append(c)
                    to_remove.append(cart)

        for c in to_remove:
            carts.remove(c)


if __name__ == "__main__":
    main()
