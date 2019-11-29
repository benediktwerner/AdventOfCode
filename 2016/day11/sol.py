#!/usr/bin/env python3

from collections import deque

THULIUM_GENERATOR = 1 << 0
PLUTONIUM_GENERATOR = 1 << 1
STRONTIUM_GENERATOR = 1 << 2
PROMETHIUM_GENERATOR = 1 << 3
RUTHENIUM_GENERATOR = 1 << 4
ELERIUM_GENERATOR = 1 << 5
DILITHIUM_GENERATOR = 1 << 6
THULIUM_CHIP = 1 << 7
PLUTONIUM_CHIP = 1 << 8
STRONTIUM_CHIP = 1 << 9
PROMETHIUM_CHIP = 1 << 10
RUTHENIUM_CHIP = 1 << 11
ELERIUM_CHIP = 1 << 12
DILITHIUM_CHIP = 1 << 13

GENERATORS = [1 << i for i in range(7)]
CHIPS = [1 << i for i in range(7, 14)]
ALL = [1 << i for i in range(14)]


def is_safe(f):
    if f & 0b11111110000000 == 0 or f & 0b1111111 == 0:
        return True
    for c in CHIPS:
        if f & c != 0 and f & (c >> 7) == 0:
            return False
    return True


def replace(old, i1, i2, new1, new2):
    if i1 == 0:
        return (new1, new2, old[2], old[3], i2)
    if i1 == 1:
        if i2 == 0:
            return (new2, new1, old[2], old[3], i2)
        return (old[0], new1, new2, old[3], i2)
    if i1 == 2:
        if i2 == 1:
            return (old[0], new2, new1, old[3], i2)
        return (old[0], old[1], new1, new2, i2)
    return (old[0], old[1], new2, new1, i2)


def min_steps(start):
    found = set()
    todo = deque([(start, 0)])
    target = start[0] | start[1] | start[2] | start[3]

    while todo:
        curr, steps = todo.popleft()

        if curr[3] == target:
            return steps

        floor = curr[4]
        f = curr[floor]
        if f == 0:
            continue

        objs = [o for o in ALL if f & o != 0]
        for i, o in enumerate(objs):
            new_f = f & ~o
            if floor < 3:
                next_f = curr[floor + 1] | o
                new = replace(curr, floor, floor + 1, new_f, next_f)
                if new not in found and is_safe(new_f) and is_safe(next_f):
                    found.add(new)
                    todo.append((new, steps + 1))
            if floor > 0:
                next_f = curr[floor - 1] | o
                new = replace(curr, floor, floor - 1, new_f, next_f)
                if new not in found and is_safe(new_f) and is_safe(next_f):
                    found.add(new)
                    todo.append((new, steps + 1))
            for o2 in objs[i + 1 :]:
                if o & 0b1111111 != 0 and o2 & 0b11111110000000 != 0 and o << 7 != o2:
                    continue
                new_new_f = new_f & ~o2
                if floor < 3:
                    next_f = curr[floor + 1] | o | o2
                    new = replace(curr, floor, floor + 1, new_new_f, next_f)
                    if new not in found and is_safe(new_new_f) and is_safe(next_f):
                        found.add(new)
                        todo.append((new, steps + 1))
                if floor > 0:
                    next_f = curr[floor - 1] | o | o2
                    new = replace(curr, floor, floor - 1, new_new_f, next_f)
                    if new not in found and is_safe(new_new_f) and is_safe(next_f):
                        found.add(new)
                        todo.append((new, steps + 1))

    raise Exception("No way found")


def main():
    # The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
    # The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
    # The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
    # The fourth floor contains nothing relevant.
    start = [
        THULIUM_GENERATOR
        | THULIUM_CHIP
        | PLUTONIUM_GENERATOR
        | STRONTIUM_GENERATOR,  # floor 0
        PLUTONIUM_CHIP | STRONTIUM_CHIP,  # floor 1
        PROMETHIUM_GENERATOR
        | PROMETHIUM_CHIP
        | RUTHENIUM_GENERATOR
        | RUTHENIUM_CHIP,  # floor 2
        0,  # floor 3
        0,  # elevator position
    ]

    print("Part 1:", min_steps(tuple(start)))

    start[0] |= ELERIUM_GENERATOR | ELERIUM_CHIP | DILITHIUM_GENERATOR | DILITHIUM_CHIP
    print("Part 2:", min_steps(tuple(start)))


if __name__ == "__main__":
    main()
