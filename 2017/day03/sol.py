INPUT = 325489

def dist(x):
    for i in range(1, 1000, 2):
        if i*i >= x:
            section = i
            break
    start = (i-2)**2 + 1
    if start + section - 2 > x:
        print("Not implemented")
        return -1
    start += section - 2
    while x >= start + section - 1:
        start += section - 1
    distToStart = x - start
    if distToStart > section // 2:
        distToStart -= (distToStart - (section // 2))*2
    return section - 1 - distToStart

print(dist(23))
print(dist(1024))
print(dist(INPUT))

def sum_around(x, y):
    result = 0
    for xd in range(-1, 2):
        for yd in range(-1, 2):
            if xd == 0 and yd == 0:
                continue
            result += ram[x+xd][y+yd]
    return result

ram = []
SIZE = 11
for i in range(SIZE):
    ram.append([0]*SIZE)

x = y = (SIZE - 1) // 2

ram[x][y] = 1
x += 1

phase = 0
MAPPING = ((0, -1), (-1, 0), (0, 1), (1, 0))
section = 3
steps = 2

while True:
##    print(x, y, section, phase)
    ram[x][y] = sum_around(x, y)
    if ram[x][y] > INPUT:
        print(ram[x][y])
        break
    steps -= 1
    if steps == 0:
        phase += 1
        if phase == 4:
            phase = 0
            section += 2
            x += 1
            steps = section - 1
            continue
        steps = section - 1
    x += MAPPING[phase][0]
    y += MAPPING[phase][1]

##for i in ram:
##    print(i)
