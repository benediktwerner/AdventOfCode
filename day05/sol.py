def find_exit(maze):
    index = 0
    counter = 0
    length = len(maze)
    while True:
        counter += 1
        x = maze[index]
        if index + x < 0 or index + x >= length:
            return counter
        maze[index] += 1 if maze[index] < 3 else -1
        index += x

print(find_exit([0, 3, 0, 1, -3]))

with open("input.txt", "r") as f:
    maze = []
    for line in f:
        maze.append(int(line.strip()))
    print(find_exit(maze))
