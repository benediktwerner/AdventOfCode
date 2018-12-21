from collections import defaultdict
import sys

NO_CHANGE_STEPS = 1000


def add(a, b):
    for i, x in enumerate(a):
        a[i] += b[i]


def part1(particles):
    t = 0
    last_change = 0
    last_value = None

    while True:
        min_dist = float("inf")
        min_i = None

        for i, p in particles.items():
            add(p[1], p[2])
            add(p[0], p[1])

            dist = sum(map(abs, p[0]))
            if dist < min_dist:
                min_dist = dist
                min_i = i

        if min_i != last_value:
            last_change = t
            last_value = min_i
        elif t - last_change >= NO_CHANGE_STEPS:
            break
        t += 1
    print(last_value)


def part2(particles):
    t = 0
    last_change = 0
    last_value = None

    while True:
        c = defaultdict(set)

        for i, p in particles.items():
            add(p[1], p[2])
            add(p[0], p[1])
            c[",".join(map(str, p[0]))].add(i)

        for i in c:
            if len(c[i]) > 1:
                for j in c[i]:
                    del particles[j]

        value = len(particles)
        if value != last_value:
            last_change = t
            last_value = value
        elif t - last_change >= NO_CHANGE_STEPS:
            break
        t += 1
    print(last_value)


def main():
    with open("input.txt", "r") as f:
        particles = {}
        for i, line in enumerate(f):
            line = line.strip().split(", ")
            line = [x[3:-1] for x in line]
            particles[i] = [list(map(int, x.split(","))) for x in line]
        if len(sys.argv) > 1 and sys.argv[1] == "1":
            part1(particles)
        else:
            part2(particles)


if __name__ == "__main__":
    main()
