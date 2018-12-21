#!/usr/bin/env python3

from collections import defaultdict


def part1(state, rules):
    plants = defaultdict(bool)
    for i, c in enumerate(state):
        if c == "#":
            plants[i] = True

    min_x = -2
    max_x = len(state) + 1

    for _ in range(20):
        new_plants = defaultdict(bool, plants)
        first_found = False
        for key in range(min_x, max_x + 1):
            area = (plants.get(key-2, False), plants.get(key-1, False),
                    plants[key], plants.get(key+1, False), plants.get(key+2, False))
            new_value = rules[area]
            new_plants[key] = new_value
            if new_value:
                if not first_found:
                    first_found = True
                    min_x = key - 2
                max_x = key + 2
        plants = new_plants

    return sum(c for c in plants if plants[c])


def part2(state, rules):
    plants = defaultdict(bool)
    for i, c in enumerate(state):
        if c == "#":
            plants[i] = True

    min_x = -2
    max_x = len(state) + 1
    found = {}
    count = 0
    pattern_found = False

    while count < 50000000000:
        new_plants = defaultdict(bool, plants)
        pattern = []
        first_found = False
        for key in range(min_x, max_x + 1):
            area = (plants.get(key-2, False), plants.get(key-1, False),
                    plants[key], plants.get(key+1, False), plants.get(key+2, False))
            new_value = rules[area]
            new_plants[key] = new_value
            if new_value:
                if not first_found:
                    first_found = True
                    min_x = key - 2
                max_x = key + 2
            if first_found:
                pattern.append(new_value)

        plants = new_plants
        count += 1

        if pattern_found:
            continue

        while not pattern[-1]:
            pattern.pop()
        pattern = tuple(pattern)

        if pattern in found:
            pattern_found = True
            found_count, found_min_x = found[pattern]

            cycle = count - found_count
            shift = min_x - found_min_x

            total_cycles = (50000000000 - count) // cycle
            total_shift = shift * total_cycles

            count += total_cycles * cycle
            min_x += total_shift
            max_x += total_shift

            new_plants = defaultdict(bool)
            for key in plants:
                if plants[key]:
                    new_plants[key+total_shift] = True
            plants = new_plants
        else:
            found[pattern] = (count, min_x)

    return sum(c for c in plants if plants[c])


def main():
    rules = {}

    with open("input.txt") as f:
        line_count = 0
        for line in f:
            if line_count == 0:
                line_count += 1
                state = line.strip().split(": ")[1]
                continue
            elif line_count == 1:
                line_count += 1
                continue
            left, right = line.strip().split(" => ")
            rules[tuple((c == "#") for c in left)] = (right == "#")

    print("Part 1:", part1(state, rules))
    print("Part 2:", part2(state, rules))


if __name__ == "__main__":
    main()
