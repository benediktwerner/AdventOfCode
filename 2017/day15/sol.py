AFAC = 16807
BFAC = 48271

def aGen(p1=False):
    a = 873
    while True:
        a = (a*AFAC) % 2147483647
        if p1 or a % 4 == 0:
            yield a

def bGen(p1=False):
    b = 583
    while True:
        b = (b*BFAC) % 2147483647
        if p1 or b % 8 == 0:
            yield b

part1 = 0
A = aGen(True)
B = bGen(True)
for i in range(40000000):
    if next(A) & 0xFFFF == next(B) & 0xFFFF:
        part1 += 1
print(part1)

part2 = 0
A = aGen()
B = bGen()
for i in range(5000000):
    if next(A) & 0xFFFF == next(B) & 0xFFFF:
        part2 += 1
print(part2)
