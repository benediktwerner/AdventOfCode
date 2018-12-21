INPUT = "ljoxqyyw"

def reverse(numbers, curr_pos, length):
    if curr_pos+length <= len(numbers):
        numbers[curr_pos:curr_pos+length] = reversed(numbers[curr_pos:curr_pos+length])
    else:
        leftover = length-(len(numbers)-curr_pos)
        sublist = list(reversed(numbers[curr_pos:] + numbers[:leftover]))
        numbers[curr_pos:] = sublist[:-leftover]
        numbers[:leftover] = sublist[-leftover:]
        
def sparse_hash(line, list_length=256):
    lengths = from_ascii(line) + [17,31,73,47,23]
    numbers = list(range(list_length))
    curr_pos = 0
    skip_size = 0
    for i in range(64):
        for length in lengths:
            reverse(numbers, curr_pos, length)
            curr_pos = (curr_pos + length + skip_size) % len(numbers)
            skip_size += 1
    return numbers

def from_ascii(line):
    ret = []
    for c in line:
        ret.append(ord(c))
    return ret

def dense_hash(numbers):
    ret = []
    for i in range(16):
        tmp = 0
        for j in range(16):
            tmp ^= numbers[i*16+j]
        ret.append(tmp)
    return ret

def to_hex(numbers):
    ret = ""
    for i in numbers:
        x = hex(i)[2:]
        if len(x) == 1:
            ret += "0" + x
        else:
            ret += x
    return ret

def knot_hash(line):
    return to_hex(dense_hash(sparse_hash(line)))

def to_bits(line):
    res = ""
    for c in line:
        res += "{:04b}".format(int(c, 16))
    return res

def count_used(code):
    res = 0
    for i in range(128):
        res += sum(map(int, to_bits(knot_hash("{}-{}".format(code, i)))))
    return res

def check_xy(x, y):
    return 0 <= x < 128 and 0 <= y < 128

def flood_fill(grid, x, y):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop(0)
        if grid[cx][cy] == 0:
            continue
        grid[cx][cy] = 0
        for xDiff, yDiff in ((-1, 0),(1, 0),(0, -1),(0, 1)):
            if not check_xy(cx+xDiff, cy+yDiff):
                continue
            if grid[cx+xDiff][cy+yDiff] == 1:
                stack.append((cx+xDiff, cy+yDiff))

def count_regions(code):
    grid = []
    for i in range(128):
        grid.append(list(map(int, to_bits(knot_hash("{}-{}".format(code, i))))))
    regions = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 1:
                regions += 1
                flood_fill(grid, x, y)
    return regions

print(count_used(INPUT))
print(count_regions(INPUT))
