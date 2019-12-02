#!/usr/bin/env python3


def run_program(memory, noun, verb):
    ip = 0
    memory = list(memory)
    memory[1] = noun
    memory[2] = verb

    while memory[ip] != 99:
        opcode, a, b, c = memory[ip : ip + 4]
        ip += 4

        if opcode == 1:
            memory[c] = memory[a] + memory[b]
        elif opcode == 2:
            memory[c] = memory[a] * memory[b]

    return memory[0]


def main():
    with open(__file__.rstrip("sol.py") + "input.txt") as f:
        memory = list(map(int, f.readline().strip().split(",")))

        print("Part 1:", run_program(memory, 12, 2))

        for noun in range(100):
            for verb in range(100):
                if run_program(memory, noun, verb) == 19690720:
                    print("Part 2:", noun * 100 + verb)
                    return


if __name__ == "__main__":
    main()
