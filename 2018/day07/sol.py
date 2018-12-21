#!/usr/bin/env python3

from collections import defaultdict


def parse(line):
    parts = line.split(" ")
    return parts[1], parts[7]


def part1():
    prereqs = defaultdict(set)
    postreqs = defaultdict(set)
    todo = set()

    with open("input.txt") as f:
        for line in f:
            a, b = parse(line)
            prereqs[b].add(a)
            postreqs[a].add(b)
            todo.add(a)
            todo.add(b)

    output = ""

    while todo:
        node = sorted(node for node in todo if not prereqs[node])[0]
        output += node
        todo.remove(node)

        for a in postreqs[node]:
            prereqs[a].remove(node)

    print("Part 1:", output)


def part2():
    prereqs = defaultdict(set)
    postreqs = defaultdict(set)
    todo = set()

    with open("input.txt") as f:
        for line in f:
            a, b = parse(line)
            prereqs[b].add(a)
            postreqs[a].add(b)
            todo.add(a)
            todo.add(b)

    workers = [False] * 5
    steps = 0

    while todo:
        steps += 1
        for i, worker in enumerate(workers):
            if not worker:
                next_nodes = sorted(node for node in todo if not prereqs[node])
                if next_nodes:
                    node = next_nodes[0]
                    workers[i] = [node, ord(node) + 61 - ord("A")]
                    todo.remove(node)
            else:
                node, time = worker
                if time == 1:
                    for a in postreqs[node]:
                        prereqs[a].remove(node)
                    next_nodes = sorted(node for node in todo if not prereqs[node])
                    if next_nodes:
                        node = next_nodes[0]
                        workers[i] = [node, ord(node) + 61 - ord("A")]
                        todo.remove(node)
                    else:
                        workers[i] = False
                else:
                    workers[i][1] -= 1

    steps += max(worker[1] for worker in workers if worker) - 1
    print("Part 2:", steps)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
