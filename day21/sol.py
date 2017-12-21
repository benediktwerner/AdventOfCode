def to1d(grid):
    return "/".join(["".join(line) for line in grid])

def to2d(line):
    return [list(x) for x in line.split("/")]

def flip(grid):
    return [line[::-1] for line in grid]

def rotate(grid):
    result = []
    for x in range(len(grid[0])):
        tmp = []
        for line in reversed(grid):
            tmp.append(line[x])
        result.append(tmp)
    return result

def get(grid, size, x, y):
    result = []
    x *= size
    y *= size
    for i in range(size):
        tmp = []
        for j in range(size):
            tmp.append(grid[x+i][y+j])
        result.append(tmp)
    return result

def main():
    e = {}
    with open("input.txt", "r") as f:
        for line in f:
            parts = line.strip().split(" => ")
            a = to2d(parts[0])
            b = flip(to2d(parts[0]))
            e[to1d(a)] = parts[1]
            e[to1d(b)] = parts[1]
            for i in range(3):
                a = rotate(a)
                b = rotate(b)
                e[to1d(a)] = parts[1]
                e[to1d(b)] = parts[1]
    grid = [[".", "#", "."],[".", ".", "#"], ["#", "#", "#"]]
    for i in range(18):
        print(i)
        if len(grid) % 2 == 0:
            size = 2
            parts = len(grid) // 2
        elif len(grid) % 3 == 0:
            size = 3
            parts = len(grid) // 3
        else:
            print("Error: Not divisible by 2 or 3!")
            return
        squares = []
        for x in range(parts):
            tmp = []
            for y in range(parts):
                tmp.append(get(grid, size, x, y))
            squares.append(tmp)
        for x, line in enumerate(squares):
            for y, square in enumerate(line):
                squares[x][y] = to2d(e[to1d(square)])
        grid = []
        for xs in range(parts):
            lines = [[] for _ in range(size+1)]
            for square in squares[xs]:
                for y, line in enumerate(square):
                    lines[y] += line
            grid += lines
    on_count = 0
    for line in grid:
        for p in line:
            if p == "#":
                on_count += 1
    print(on_count)


if __name__ == "__main__":
    main()
