from collections import defaultdict

PROGRAM = {
    "A": (
        (1, 1, "B"),
        (0, -1, "E")
    ),
    "B": (
        (1, -1, "C"),
        (0, 1, "A")
    ),
    "C": (
        (1, -1, "D"),
        (0, 1, "C")
    ),
    "D": (
        (1, -1, "E"),
        (0, -1, "F")
    ),
    "E": (
        (1, -1, "A"),
        (1, -1, "C")
    ),
    "F": (
        (1, -1, "E"),
        (1, 1, "A")
    )
}

STEPS = 12386363

def main():
    state = "A"
    pos = 0
    memory = defaultdict(lambda: 0)
    for i in range(STEPS):
        write, move, new_state = PROGRAM[state][memory[pos]]
        memory[pos] = write
        pos += move
        state = new_state
    print(sum(memory.values()))
    

if __name__ == '__main__':
    main()
