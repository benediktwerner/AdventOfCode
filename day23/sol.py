from collections import defaultdict

def part1(instructions):
    def get(x):
        try:
            return int(x)
        except ValueError:
            return registers[x]

    bz = 0
    length = len(instructions)
    registers = defaultdict(lambda: 0)
    mul_count = 0
    while 0 <= bz < length:
        instr = instructions[bz].split(" ")
        if instr[0] == "set":
            registers[instr[1]] = get(instr[2])
        elif instr[0] == "sub":
            registers[instr[1]] -= get(instr[2])
        elif instr[0] == "mul":
            mul_count += 1
            registers[instr[1]] *= get(instr[2])
        elif instr[0] == "jnz":
            if get(instr[1]) != 0:
                bz += get(instr[2])
                continue
        bz += 1
    print(mul_count)

def part2(instructions):
    def get(x):
        try:
            return int(x)
        except ValueError:
            return registers[x]

    bz = 0
    length = len(instructions)
    registers = defaultdict(lambda: 0)
    registers["a"] = 1
    while 0 <= bz < length:
        instr = instructions[bz].split(" ")
        if instr[0] == "set":
            registers[instr[1]] = get(instr[2])
        elif instr[0] == "sub":
            registers[instr[1]] -= get(instr[2])
        elif instr[0] == "mul":
            registers[instr[1]] *= get(instr[2])
        elif instr[0] == "jnz":
            if get(instr[1]) != 0:
                bz += get(instr[2])
                continue
        bz += 1
    print(registers["h"])

def main():
    with open("input.txt", "r") as f:
        instructions = [line.strip() for line in f]
        part1(instructions)
    
    with open("input_opt.txt", "r") as f:
        instructions = [line.strip() for line in f]
        part2(instructions)

if __name__ == "__main__":
    main()
