with open("input.txt", "r") as f:
    to = []
    for line in f:
        to.append([int(x.strip(",")) for x in line.strip().split(" ")[2:]])
    groups = []
    todo = set(range(len(to)))
    while todo:
        stack = [todo.pop()]
        group = set()
        while stack:
            element = stack.pop(0)
            for n in to[element]:
                if n not in group:
                    group.add(n)
                    stack.append(n)
                    if n in todo:
                        todo.remove(n)
        groups.append(group)
    for g in groups:
        if 0 in g:
            print("Group 0:", len(g))
    print("Total groups:", len(groups))
        
