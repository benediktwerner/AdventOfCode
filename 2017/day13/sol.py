def severity(r, start=0):
    severity = 0
    for i in r:
        if (start + i) % (r[i]*2 - 2) == 0:
            severity += (start + i)*r[i]
    return severity

with open("input.txt", "r") as f:
    r = {}
    for line in f:
        i, ra = line.strip().split(": ")
        r[int(i)] = int(ra)
    print(severity(r))
    for i in range(10000000):
        if severity(r, i) == 0:
            print(i)
            break
