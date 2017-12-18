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

def part2(instructions):
    def get(x):
        try:
            return int(x)
        except ValueError:
            return registers[program][x]

    program = 0
    bz = [0, 0]
    length = len(instructions)
    registers = [defaultdict(lambda: 0), defaultdict(lambda: 0)]
    registers[1]["p"] = 1
    queue = [[],[]]
    result = 0
    terminated = [False]*2
    while True:
        while 0 <= bz[program] < length:
            instr = instructions[bz[program]].split(" ")
            if instr[0] == "snd":
                queue[(program+1)%2].append(get(instr[1]))
                if program == 1:
                    result += 1
            elif instr[0] == "set":
                registers[program][instr[1]] = get(instr[2])
            elif instr[0] == "add":
                registers[program][instr[1]] += get(instr[2])
            elif instr[0] == "mul":
                registers[program][instr[1]] *= get(instr[2])
            elif instr[0] == "mod":
                registers[program][instr[1]] %= get(instr[2])
            elif instr[0] == "rcv":
                if queue[program]:
                    registers[program][instr[1]] = queue[program].pop(0)
                elif terminated[(program+1)%2] or not queue[(program+1)%2]:
                    return result
                else:
                    program = (program+1)%2
                    continue
            elif instr[0] == "jgz":
                if get(instr[1]) > 0:
                    bz[program] += get(instr[2])
                    continue
            bz[program] += 1
        terminated[program] = True
        if terminated[(program + 1)%2]:
            return result
        program = (program+1)%2

with open("input.txt", "r") as f:
    instructions = [line.strip() for line in f]
    print(last_recovered_sound(instructions))
    print(part2(instructions))
