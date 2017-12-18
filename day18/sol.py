from collections import defaultdict

def last_recovered_sound(instructions):
    def get(x):
        try:
            return int(x)
        except ValueError:
            return registers[x]

    bz = 0
    length = len(instructions)
    registers = defaultdict(lambda: 0)
    last_sound = None
    while 0 <= bz < length:
        instr = instructions[bz].split(" ")
        if instr[0] == "snd":
            last_sound = registers[instr[1]]
        elif instr[0] == "set":
            registers[instr[1]] = get(instr[2])
        elif instr[0] == "add":
            registers[instr[1]] += get(instr[2])
        elif instr[0] == "mul":
            registers[instr[1]] *= get(instr[2])
        elif instr[0] == "mod":
            registers[instr[1]] %= get(instr[2])
        elif instr[0] == "rcv":
            if registers[instr[1]] != 0:
##                registers[instr[1]] = last_sound
                return last_sound
        elif instr[0] == "jgz":
            if registers[instr[1]] > 0:
                bz += get(instr[2])
                continue
        bz += 1

with open("input.txt", "r") as f:
    print(last_recovered_sound([line.strip() for line in f]))
