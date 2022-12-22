#!/usr/bin/env python3

import re

SIZE = 50
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
RIGHT, DOWN, LEFT, UP, OPP, SELF = range(6)
# fmt: off
MAPPING = {
    SELF: {
        RIGHT: (RIGHT, 0),
        LEFT: (LEFT, 0),
        UP: (UP, 0),
        DOWN: (DOWN, 0),
    },
    RIGHT: {
        RIGHT: (OPP, 2),
        LEFT: (SELF, 0),
        UP: (UP, 3),
        DOWN: (DOWN, 1),
    },
    LEFT: {
        RIGHT: (SELF, 0),
        LEFT: (OPP, 2),
        UP: (UP, 1),
        DOWN: (DOWN, 3),
    },
    UP: {
        RIGHT: (RIGHT, 1),
        LEFT: (LEFT, 3),
        UP: (OPP, 0),
        DOWN: (SELF, 0),
    },
    DOWN: {
        RIGHT: (RIGHT, 3),
        LEFT: (LEFT, 1),
        UP: (SELF, 0),
        DOWN: (OPP, 0),
    },
    # rotation 0 is up/down == down/up, right/left == right/left as reached by up+up or down+down
    OPP: {
        RIGHT: (RIGHT, 2),
        LEFT: (LEFT, 2),
        UP: (DOWN, 0),
        DOWN: (UP, 0),
    },
}
# fmt: on

#    D
#   LOR
#  U U U
# ROLSROL
#  D D D
#   LOR
#    U


def find_face(face, target_rel):
    visited = {face}
    todo = [(face, SELF, 0)]

    while todo:
        (fx, fy), rel, rot = todo.pop()
        # if face == (0, 150) and target_rel == 2:
        #     print(fx, fy, rel, rot)
        for d, (dx, dy) in enumerate(DIRS):
            new_face = fx + dx * 50, fy + dy * 50
            if new_face not in faces or new_face in visited:
                continue
            visited.add(new_face)
            new_rel, new_rot = MAPPING[rel][(d + rot) % 4]
            new_rot = (new_rot + rot) % 4
            if new_rel == target_rel:
                return new_face, new_rot
            todo.append((new_face, new_rel, new_rot))
    assert False, (face, target_rel)


with open("input.txt") as f:
    lines = f.read().splitlines()

grid = {}
faces = set()
path = re.findall("\d+|L|R", lines[-1])

for y, line in enumerate(lines[:-2]):
    for x, c in enumerate(line):
        if c != " ":
            if x % 50 == 0 and y % 50 == 0:
                faces.add((x, y))
            grid[x, y] = c

mx = min(x for x, y in grid if y == 0)
my = 0
d = 0

for p in path:
    if p == "L":
        d = (d - 1) % 4
        continue
    if p == "R":
        d = (d + 1) % 4
        continue
    for _ in range(int(p)):
        dx, dy = DIRS[d]
        nd = d
        nx, ny = mx + dx, my + dy

        if (nx, ny) not in grid:
            fx, fy = mx % 50, my % 50
            nface, rot = find_face((mx - fx, my - fy), d)
            nd = (d - rot) % 4
            if d == RIGHT:
                nx, ny = 0, fy
            elif d == LEFT:
                nx, ny = 49, fy
            elif d == DOWN:
                nx, ny = fx, 0
            else:
                nx, ny = fx, 49
            if rot == 1:
                nx, ny = ny, 49 - nx
            elif rot == 2:
                nx, ny = 49 - nx, 49 - ny
            elif rot == 3:
                nx, ny = 49 - ny, nx
            nx += nface[0]
            ny += nface[1]
            print(nx, ny, nd)

        if grid[nx, ny] == "#":
            break

        mx, my = nx, ny
        d = nd

print(1000 * (my + 1) + 4 * (mx + 1) + d)
