from collections import defaultdict

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
DIR_CHANGE = (3, 0, 1, 2)

def main():
    cells = defaultdict(lambda: 0)
    width = None
    height = None
    with open("input.txt", "r") as f:
        for y, line in enumerate(f):
            if width is None:
                width = len(line.strip())
            height = y+1
            for x, c in enumerate(line.strip()):
                cells[(x, y)] = 2 if c == "#" else 0
    x = width // 2
    y = height // 2
    d = 0
    infections = 0
    for _ in range(10000000):
        d = (d + DIR_CHANGE[cells[(x, y)]]) % 4
        if cells[(x, y)] == 1:
            infections += 1
        cells[(x, y)] = (cells[(x, y)] + 1) % 4
        x += DIRS[d][0]
        y += DIRS[d][1]
    print(infections)

if __name__ == '__main__':
    main()
