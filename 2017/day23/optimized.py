b = 105700
c = 122700
g = 1
h = 0

while g != 0:
    f = False
    d = 2

    while g != 0:
#        e = 2
        if b % d == 0:
            f = True
            break
#        while g != 0:
#            if d * e == b:
#                f = True
#            e += 1
#            g = e - b
        d += 1
        g = d - b

    if f:
        h += 1
    g = b - c
    b += 17
print(h)
