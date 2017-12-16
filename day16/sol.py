def find(x, programs):
    for i, p in enumerate(programs):
        if p == x:
            return i
    return -1

def do_move(move, programs):
    if move[0] == "s":
        x = int(move[1:])
        programs = programs[-x:] + programs[:-x]
    elif move[0] == "x":
        a, b = map(int, move[1:].split("/"))
        x = programs[a]
        programs[a] = programs[b]
        programs[b] = x
    elif move[0] == "p":
        a, b = map(lambda x: find(x, programs), move[1:].split("/"))
        x = programs[a]
        programs[a] = programs[b]
        programs[b] = x
    return programs

def dance(moves, number_of_programs=16):
    programs = [chr(c+ord("a")) for c in range(number_of_programs)]
    for move in moves:
        programs = do_move(move, programs)
    return "".join(programs)

def dance2(moves, number_of_programs=16, repeats=1000000000):
    programs = [chr(c+ord("a")) for c in range(number_of_programs)]
    known_states = {}
    for i in range(repeats):
        state = "".join(programs)   
        if state in known_states:
            cycle = i - known_states[state]
            todo = (repeats-i) % cycle
            print("Found cylcle at:", state)
            print("Last seen:", known_states[state])
            print("Now:", i)
            print("Cycle length:", cycle)
            print("Todo:", todo)
            for i in range(todo):
                for move in moves:
                    programs = do_move(move, programs)
            return "".join(programs)
        known_states[state] = i
        for move in moves:
            programs = do_move(move, programs)
    return "".join(programs)

with open("input.txt", "r") as f:
    for line in f:
        moves = line.strip().split(",")
        print(dance(moves))
        print(dance2(moves))
        break
