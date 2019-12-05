in low
in high
add low -1 curr

loop:
    add curr 1 curr
    gt curr high tmp
    jtrue tmp :end

    out curr

    mov curr curr_tmp
    mov 10 last
    mov 0 last_count
    mov 0 has_part1
    mov 0 has_part2

    inner_loop:
        eq curr_tmp 0 tmp
        jtrue tmp :inner_end

        divmod curr_tmp 10 curr_tmp digit
        eq digit last tmp
        jfalse tmp :not_eq

        eq:
            add last_count 1 last_count
            mov 1 has_part1
            jmp :inner_loop

        not_eq:
            gt digit last tmp
            jfalse tmp :inc_order
            loop_next_curr:
                mul curr_tmp 10 curr_tmp
                add curr_tmp digit curr_tmp
                lt curr_tmp 100000 tmp
                jtrue tmp :loop_next_curr
                add curr_tmp -1 curr
                jmp :loop

            inc_order:
                eq last_count 2 tmp
                jfalse tmp :not_eq_end
                mov 1 has_part2

            not_eq_end:
                mov digit last
                mov 1 last_count
                jmp :inner_loop

    inner_end:
        eq last_count 2 tmp
        jfalse tmp :inner_end_check
        mov 1 has_part2

        inner_end_check:
            jfalse has_part1 :no_part1
            add count1 1 count1

            no_part1:
            jfalse has_part2 :loop
            add count2 1 count2
            jmp :loop

end:
    out count1
    out count2
    hlt
