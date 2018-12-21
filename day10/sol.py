def reverse(numbers, curr_pos, length):
    if curr_pos+length <= len(numbers):
        numbers[curr_pos:curr_pos+length] = reversed(numbers[curr_pos:curr_pos+length])
    else:
        leftover = length-(len(numbers)-curr_pos)
        sublist = list(reversed(numbers[curr_pos:] + numbers[:leftover]))
        numbers[curr_pos:] = sublist[:-leftover]
        numbers[:leftover] = sublist[-leftover:]

def do(lengths, list_length=256):
    numbers = list(range(list_length))
    curr_pos = 0
    skip_size = 0
    for length in lengths:
        reverse(numbers, curr_pos, length)
        curr_pos = (curr_pos + length + skip_size) % len(numbers)
        skip_size += 1
##        print(numbers, curr_pos)
    return numbers

def from_ascii(line):
    ret = []
    for c in line:
        ret.append(ord(c))
    return ret

def do2(line, list_length=256):
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


print(do([3,4,1,5], 5))
print(to_hex(dense_hash(do2(""))))

with open("input.txt", "r") as f:
    for line in f:
        numbers = do([int(x) for x in line.strip().split(",")])
        print(numbers[0]*numbers[1])
        print(to_hex(dense_hash(do2(line.strip()))))
