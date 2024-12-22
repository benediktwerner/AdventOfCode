#!/usr/bin/env python3

from collections import defaultdict, deque
from os import path

MOD = 16777216


def iterate(n: int) -> int:
    n ^= n * 64
    n %= MOD
    n ^= n // 32
    n %= MOD
    n ^= n * 2048
    n %= MOD
    return n


with open(path.join(path.dirname(__file__), "input.txt")) as file:
    numbers = list(map(int, file.read().splitlines()))

part1 = 0
for n in numbers:
    for _ in range(2000):
        n = iterate(n)
    part1 += n
print("Part 1:", part1)

seq_to_income = defaultdict(int)

for n in numbers:
    seen_seqs = set()
    seq = deque()
    prev_price = n % 10
    for _ in range(2000):
        n = iterate(n)
        price = n % 10
        seq.append(price - prev_price)
        if len(seq) == 4:
            s = tuple(seq)
            if s not in seen_seqs:
                seq_to_income[s] += price
                seen_seqs.add(s)
            seq.popleft()
        prev_price = price

print("Part 2:", max(seq_to_income.values()))
