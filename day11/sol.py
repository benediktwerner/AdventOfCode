#!/usr/bin/env python3


def max_power(cells, size):
    size -= 1
    max_level = float("-inf")
    max_cord = None

    for y in range(300 - size):
        for x in range(300 - size):
            left = cells[y+size][x-1] if x > 0 else 0
            up = cells[y-1][x+size] if y > 0 else 0
            left_up = cells[y-1][x-1] if x > 0 and y > 0 else 0
            right_down = cells[y + size][x+size]
            power_level = left_up + right_down - left - up
            if power_level > max_level:
                max_level = power_level
                max_cord = (x+1, y+1, size+1)
    return max_level, max_cord


def main():
    with open("input.txt") as f:
        grid_id = int(f.readline().strip())

    cells = []

    for y in range(300):
        row = []
        for x in range(300):
            rack_id = x + 11
            power_level = (rack_id * (y+1) + grid_id) * rack_id
            power_level = (power_level // 100) % 10
            power_level -= 5
            left = row[-1] if x > 0 else 0
            up = cells[y-1][x] if y > 0 else 0
            left_up = cells[y-1][x-1] if y > 0 and x > 0 else 0
            row.append(power_level + left + up - left_up)
        cells.append(row)

    max_level, (x, y, _) = max_power(cells, 3)
    print("Part 1: {},{} with power {}".format(x, y, max_level))

    max_level, max_cord = max((max_power(cells, size) for size in range(1, 301)), key=lambda x: x[0])
    print("Part 2: {},{},{} with power {}".format(*max_cord, max_level))


if __name__ == "__main__":
    main()
