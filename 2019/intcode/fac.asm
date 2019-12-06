in n

loop:
    lt n 2 tmp
    jnz tmp :end

    mul result n result
    add n -1 n

    add 0 0 tmp
    jz tmp :loop

end:
    out result
    hlt

result: data 1
