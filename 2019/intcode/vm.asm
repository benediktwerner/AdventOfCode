jnz init :init  # jmp :init
array 0 500

init:
    in len
    mov 0 index

loop:
    lt index len tmp
    jfalse tmp 0

    in tmp
    store tmp index
    add index 1 index

    jnz loop :loop      # jmp :loop
