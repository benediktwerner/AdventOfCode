with open("input.txt") as f:
    result1 = 0
	result2 = 0
    for line in f:
        numbers = list(map(int, line.strip().split("\t")))
        result1 += max(numbers) - min(numbers)
		
        found = False
        for i in numbers:
            for j in numbers:
                if i == j:
                    continue
                if i % j == 0:
                    found = True
                    result2 += i // j
                    break
            if found:
                break
    print(result1, result2)
