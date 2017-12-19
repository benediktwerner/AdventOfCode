#DIRS = ((0, 1), (-1, 0), (0, -1), (1, 0))
DIRS = ((1, 0), (0, -1), (-1, 0), (0, 1), )

with open("input.txt", "r") as f:
    maze = []
    for line in f:
        maze.append([c for c in line])
    x = 0
    y = 0
    direction = 0
    steps = 0
    letters = []
    for i, c in enumerate(maze[0]):
        if c == "|":
            y = i
            break
    while True:
        curr = maze[x][y]
        #print(x, y, curr)
        if curr == "+":
            for i, d in enumerate(DIRS):
                if i == (direction+2)%4:
                    continue
                if maze[x+d[0]][y+d[1]] != " ":
                    direction = i
                    break
        elif curr == " ":
            print("Landed on empty space", x, y)
            break
        elif curr != "|" and curr != "-":
            letters.append(curr)

        steps += 1
        x += DIRS[direction][0]
        y += DIRS[direction][1]
    print(*letters, sep="")
    print("Steps:", steps)
