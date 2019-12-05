start:
    in x
    eq x 0 tmp
    jtrue tmp :end
    div x 3 x
    sub x 2 x
    add total x total
    jmp :start

end:
    out total
    hlt
