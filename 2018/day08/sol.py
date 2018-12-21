#!/usr/bin/env python3


from collections import defaultdict


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def sum_metadata(self):
        total = sum(self.metadata)
        for child in self.children:
            total += child.sum_metadata()
        return total

    def value(self):
        if not self.children:
            return sum(self.metadata)

        total = 0
        for m in self.metadata:
            if 0 < m <= len(self.children):
                total += self.children[m-1].value()
        return total


def parse(line, start=0):
    children_count, metadata_count = line[start:start+2]
    children = []
    start += 2
    for _ in range(children_count):
        start, child = parse(line, start)
        children.append(child)
    metadata = line[start:start+metadata_count]
    return start+metadata_count, Node(children, metadata)


def main():
    with open("input.txt") as f:
        numbers = [int(x) for x in f.readline().strip().split(" ")]
        _, root = parse(numbers)

    print("Part 1:", root.sum_metadata())
    print("Part 2:", root.value())


if __name__ == "__main__":
    main()
