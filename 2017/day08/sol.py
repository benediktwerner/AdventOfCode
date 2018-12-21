from collections import *

M = {"inc": 1, "dec": -1}

with open("input.txt", "r") as f:
    max_val = 0
    memory = defaultdict(lambda: 0)
    for line in f:
        s = line.strip().split()
        if eval(str(memory[s[4]]) + s[5] + s[6]):
            memory[s[0]] += M[s[1]] * int(s[2])
            max_val = max(memory[s[0]], max_val)
    print(max(memory.values()))
    print(max_val)
