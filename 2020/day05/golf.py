f={int(bytes(c>>2&1^49 for c in t[:-1]),2)for t in open("i","rb")}
print(min({*range(min(f),max(f))}-f))
