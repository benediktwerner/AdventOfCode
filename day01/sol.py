def solve(line):
    result1 = 0
	result2 = 0
    length = len(line)
    half = length // 2
    for i in range(length):
		if line[i] == line[(i+1)%length]):
			result1 += int(line[i])
        if line[i] == line[(i+half)%length]:
            result2 += int(line[i])
    return result1, result2

with open("input.txt", "r") as f:
    input_text = ""
    for line in f:
        input_text += line.strip()
    print(solve(input_text))

print("Test:")
print(solve("1212"))
print(solve("1221"))
print(solve("123425"))
print(solve("123123"))
print(solve("12131415"))
