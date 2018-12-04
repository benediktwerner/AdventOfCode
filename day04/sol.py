#!/usr/bin/env python3

from collections import defaultdict


def parse(line):
    timestamp, action = line.strip().split("] ")
    date, time = timestamp[1:].split(" ")
    hour, minute = time.split(":")
    total_minutes = int(hour) * 60 + int(minute)
    return date, total_minutes, action


def main():
    times = []

    with open("input.txt") as f:
        for line in f:
            times.append(parse(line))

    guards = defaultdict(lambda: defaultdict(int))
    guard = None
    last_time = None

    for _, time, action in sorted(times):
        if "#" in action:
            guard = int(action.split(" ")[1][1:])
        elif action == "falls asleep":
            last_time = time
        elif action == "wakes up":
            guards[guard][-1] += time - last_time
            for i in range(last_time, time):
                guards[guard][i] += 1
        else:
            print("Invalid action:", action)

    max_guard = max(guards, key=lambda g: guards[g][-1])
    max_minute = {}

    for guard in guards:
        max_minute[guard] = max(guards[guard], key=lambda m: 0 if m == -1 else guards[guard][m])

    print("Part 1:", max_guard * max_minute[max_guard])

    max_guard = max(guards, key=lambda g: guards[g][max_minute[g]])

    print("Part 2:", max_guard * max_minute[max_guard])


if __name__ == "__main__":
    main()
