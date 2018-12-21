def calc_weight(memory, name):
    weight = 0
    subweight_one = None
    for s in memory[name]["next"]:
        if "subweight" not in memory[s]:
            calc_weight(memory, s)
        s_weight = memory[s]["subweight"] + memory[s]["weight"]
        if subweight_one is None:
            subweight_one = s_weight
        elif subweight_one != s_weight:
            print(s, "has", s_weight, "while others have", subweight_one)
        weight += s_weight
    memory[name]["subweight"] = weight

def find_wrong(memory, name):
    calc_weight(memory, name)

with open("input.txt", "r") as f:
    memory = {}
    for line in f:
        parts = line.strip().split(" ")
        name = parts[0]
        new = memory.get(name, {"next": [], "prev": None})
        new["weight"] = int(parts[1][1:-1])
        if len(parts) > 2:
            for s in parts[3:]:
                s = s.replace(",", "")
                if s in memory:
                     memory[s]["prev"] = name
                else:
                    memory[s] = {"next": [], "prev": name}
                new["next"].append(s)
        memory[name] = new
    for name in memory:
        if memory[name]["prev"] is None:
            print("Bottom:", name)
            print(find_wrong(memory, name))
            break
