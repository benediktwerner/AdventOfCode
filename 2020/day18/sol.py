#!/usr/bin/env python3

from os import path


class Parser:
    def __init__(self, inp, part2):
        self.i = 0
        self.inp = inp
        self.part2 = part2

    def c(self):
        return self.inp[self.i]

    def parse_atom(self):
        if self.c() == "(":
            self.i += 1
            val = self.parse_expr()
            self.i += 1
            return val
        return self.parse_int()

    def parse_expr(self):
        result = self.parse_atom()
        while self.i < len(self.inp) and self.c() != ")":
            op = self.inp[self.i + 1]
            self.i += 3
            if op == "*":
                result *= self.parse_sum() if self.part2 else self.parse_atom()
            else:
                result += self.parse_atom()
        return result

    def parse_sum(self):
        result = self.parse_atom()
        while self.i < len(self.inp) and self.c() != ")":
            op = self.inp[self.i + 1]
            if op == "+":
                self.i += 3
                result += self.parse_atom()
            else:
                return result
        return result

    def parse_int(self):
        start = self.i
        while self.i < len(self.inp) and self.c().isdigit():
            self.i += 1
        return int(self.inp[start : self.i])


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    part1 = 0
    part2 = 0

    for line in f:
        part1 += Parser(line.strip(), False).parse_expr()
        part2 += Parser(line.strip(), True).parse_expr()

    print("Part 1:", part1)
    print("Part 2:", part2)
