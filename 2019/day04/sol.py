#!/usr/bin/env python3


with open(__file__.rstrip("sol.py") + "input.txt") as f:
    low, high = map(int, f.readline().strip().split("-"))

    count1 = 0
    count2 = 0

    for num in range(low, high + 1):
        last = 0
        last_count = 0
        at_least_double = False
        exactly_double = False

        for digit in str(num):
            digit = int(digit)
            if digit < last:
                break
            elif digit == last:
                at_least_double = True
                last_count += 1
            else:
                if last_count == 2:
                    exactly_double = True
                last_count = 1
            last = digit
        else:
            if at_least_double:
                count1 += 1
            if exactly_double or last_count == 2:
                count2 += 1

    print("Part 1:", count1)
    print("Part 2:", count2)
