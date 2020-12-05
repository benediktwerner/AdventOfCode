print(*{*range(min(f:={int(bytes(c>>2&1^49 for c in t),2)//2 for t in open("t","rb")}),max(f))}-f)
