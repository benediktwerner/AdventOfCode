def solve(line):
    result = 0
    length = len(line)
    half = length // 2
    for i in range(length):
        if line[i] == line[(i+half)%length]:
            result += int(line[i])
    return result

with open("input.txt", "r") as f:
    input_text = ""
    for line in f:
        input_text += line.strip()
    print(solve(input_text))

print(solve("1212"))
print(solve("1221"))
print(solve("123425"))
print(solve("123123"))
print(solve("12131415"))
