def isvalid1(pwd):
    s = set()
    for word in pwd.split(" "):
        if word in s:
            return False
        s.add(word)
    return True

def isvalid2(pwd):
    s = set()
    for word in pwd.split(" "):
        w = "".join(sorted(word))
        if w in s:
            return False
        s.add(w)
    return True
    

with open("input.txt", "r") as f:
    result = 0
    for line in f:
        if isvalid2(line.strip()):
            result += 1
    print(result)
