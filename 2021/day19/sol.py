#!/usr/bin/env python3

from os import path
import itertools
import re


def ints(string):
    return map(int, re.findall(r"-?[0-9]+", string))


def convert(x, y, z, ori):
    xneg, xaxis, yneg, yaxis, zneg = ori
    out = [0, 0, 0]
    axis = [0, 1, 2]
    out[axis.pop(xaxis)] = x * xneg
    out[axis.pop(yaxis)] = y * yneg
    out[axis.pop()] = z * zneg
    return tuple(out)


def convert_reverse(x, y, z, ori):
    xneg, xaxis, yneg, yaxis, zneg = ori
    ins = [x, y, z]
    axis = [0, 1, 2]
    x = ins[axis.pop(xaxis)] * xneg
    y = ins[axis.pop(yaxis)] * yneg
    z = ins[axis.pop()] * zneg
    return x, y, z


def match(main, other):
    for ori in itertools.product((-1, 1), (0, 1, 2), (-1, 1), (0, 1), (-1, 1)):
        for x, y, z in main:
            for xx, yy, zz in other:
                match_count = 0
                for xxx, yyy, zzz in main:
                    if (x, y, z) == (xxx, yyy, zzz):
                        continue
                    dx = xxx - x
                    dy = yyy - y
                    dz = zzz - z
                    dxx, dyy, dzz = convert(dx, dy, dz, ori)
                    if (xx + dxx, yy + dyy, zz + dzz) in other:
                        match_count += 1
                if match_count >= 11:
                    x, y, z = convert(x, y, z, ori)
                    dx, dy, dz = x - xx, y - yy, z - zz
                    return (
                        set(
                            convert_reverse(x + dx, y + dy, z + dz, ori)
                            for x, y, z in other
                        ),
                        convert_reverse(dx, dy, dz, ori),
                    )


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    inp2 = f.read().strip().split("\n\n")
    scanners = []
    for lines in inp2:
        scanner = set()
        for line in lines.splitlines()[1:]:
            scanner.add(tuple(ints(line)))
        scanners.append(scanner)

    todo = [0]
    matched = set([0])
    beacons = set(scanners[0])
    scanners_pos = set([(0, 0, 0)])
    while todo:
        new = []
        for main in todo:
            for i, other in enumerate(scanners):
                if i in matched:
                    continue
                res = match(scanners[main], other)
                if res:
                    m, s = res
                    new.append(i)
                    matched.add(i)
                    scanners[i] = m
                    scanners_pos.add(s)
                    beacons |= m
        todo = new

    print("Part 1:", len(beacons))
    print(
        "Part 2:",
        max(
            abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            for (x1, y1, z1), (x2, y2, z2) in itertools.combinations(scanners_pos, 2)
        ),
    )
