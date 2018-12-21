def check(memory):
    counter = 0
    known_states = {}
    length = len(memory)
    while True:
        s = ";".join(map(str, memory))
        if s in known_states.keys():
            return counter, counter - known_states[s]
        known_states[s] = counter
        counter += 1
        index = 0
        blocks = memory[0]
        for i in range(1, length):
            if memory[i] > blocks:
                blocks = memory[i]
                index = i
        memory[index] = 0
        index += 1
        while blocks > 0:
            memory[index % length] += 1
            blocks -= 1
            index += 1

print(check([0, 2, 7, 0]))

with open("input.txt", "r") as f:
    for line in f:
        print(check([int(x) for x in line.strip().split("\t")]))
        break
