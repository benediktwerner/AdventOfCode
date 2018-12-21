def score(line):
    total = 0
    curr = 0
    garbage = False
    ignore = False
    garbage_count = 0
    for c in line:
        if ignore:
            ignore = False
        elif garbage:
            if c == ">":
                garbage = False
            elif c == "!":
                ignore = True
            else:
                garbage_count += 1
        elif c == "<":
            garbage = True
        elif c == "{":
            curr += 1
            total += curr
        elif c == "}":
            curr -= 1
    return total, garbage_count

print(score("{{<a!>},{<a!>},{<a!>},{<ab>}}"))

with open("input.txt", "r") as f:
    for line in f:
        print(score(line))
        break
