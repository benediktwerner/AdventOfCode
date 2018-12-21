import turtle
# Visualization
turtle.shape("circle")
turtle.shapesize(0.1, 0.1)
turtle.speed(0)

MOVES = {
    "n":  ( 2,  0),
    "ne": ( 1,  1),
    "se": (-1,  1),
    "s":  (-2,  0),
    "sw": (-1, -1),
    "nw": ( 1, -1)
}

def dist(x, y):
    x = abs(x)
    y = abs(y)
    ma = max(x,y)
    mi = min(x,y)
    return mi+((ma-mi)//2)

def find_pos(line):
    moves = line.strip().lower().split(",")
    x = 0
    y = 0
    max_dist = 0
    for m in moves:
        x += MOVES[m][0]
        y += MOVES[m][1]
        #turtle.goto(x, y) # Visualize path
        max_dist = max(max_dist, dist(x,y))
    return x, y, dist(x,y), max_dist

with open("input.txt", "r") as f:
    for line in f:
        print(find_pos(line))
        break
