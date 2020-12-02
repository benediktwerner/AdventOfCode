.intel_syntax noprefix

.text
.globl asm_solve_day01
.extern rust_memset

/*
    inp: rdi = input: *const u8
    inp: rsi = length: usize
    out: rax = part2 << 32 | part1
*/

asm_solve_day01:
    push rbp
    push rbx
    push r10
    push r15
    mov rbp, rsp

    mov r10, rdi        /* r10 = input */
    lea r15, [rdi+rsi]  /* r15 = input+length */

    /* rsp = nums = [false; 2020]; */
    sub rsp, 2024
    mov rdi, rsp
    mov edx, 2020
    xor esi, esi
    call rust_memset

    xor eax, eax    /* eax = num = 0 */
    xor ebx, ebx    /* ebx = count = 0 */

    /* for &c in input.as_bytes() */
    char_loop:
        /* if c == b'\n' */
        movzx ecx, byte ptr [r10]
        cmp cl, 10
        je newline

            /* num = num * 10 + (c - '0') */
            lea eax, [eax + 4*eax]
            /* add cl, -48 */
            lea eax, [ecx + 2*eax - 48]

            inc r10
            cmp r10, r15
            jl char_loop
            jmp char_loop_end

        /* else 
            nums[num] = true;
            count += 1;
            num = 0;
        */
        newline:
            mov byte ptr [rsp + rax], 1
            inc ebx
            xor eax, eax

            inc r10
            cmp r10, r15
            jl char_loop

    char_loop_end:

    /* ebx = count */
    xor eax, eax    /* output = (0, 0) */
    mov r8, rsp     /* r8 = nums */
    lea ecx, [ebx*4]
    sub rsp, rcx    /* rsp = nums_list = [undefined_u32; count] */
    xor esi, esi    /* rsi = n = 0 */
    xor ecx, ecx    /* rcx = i = 0 */

    /* for (n, b) in nums.iter().enumerate() */
    first_loop:
        /* if b */
        movzx edx, byte ptr [r8 + rsi]
        test edx, edx
        jz not_set

            /*
                nums_list[i] = n
                i += 1;
            */
            mov dword ptr [rsp + 4*rcx], esi
            inc ecx

            mov edi, 2020
            sub edi, esi    /* edi = opp = 2020 - n */

            /* if nums[opp] */
            movzx edx, byte ptr [r8 + rdi]
            test edx, edx
            jz not_set

                /* output.0 = a * opp */
                mov eax, edi
                imul eax, esi

        not_set:
            inc esi
            cmp esi, 2020
            jl first_loop

    /*
        rax = output
        r8 = nums
        rsp = nums_list
        ebx = count
    */

    /* for (i, &a) in nums_list.iter().enumerate() */
    xor esi, esi    /* rsi = i = 0 */
    outer_loop:
        mov ecx, dword ptr [rsp + 4*rsi]  /* ecx = a */
        mov edi, 2020
        sub edi, ecx    /* edi = opp = 2020 - a */

        /* for &b in nums_list.get_unchecked(i + 1..) */
        inc esi         /* i needs to be incremented at the end of the loop anyway */
        mov r9d, esi    /* r9 = j = inner loop variable = i + 1*/
        inner_loop:
            mov r10d, dword ptr [rsp + 4*r9] /* r10 = b */
            /* if 2*b > opp: break */
            lea r15d, [2*r10d]
            cmp r15d, edi
            jg outer_loop

            mov r15d, edi
            sub r15d, r10d /* r15 = opp2 = opp - b */

            /* if nums[opp2] */
            movzx edx, byte ptr [r8 + r15]
            test edx, edx
            jz inner_not_found

                /*
                    output.1 = a * b * opp2
                    return
                */
                imul ecx, r10d
                imul ecx, r15d
                shl rcx, 32
                or rax, rcx

                /* return */
                mov rsp, rbp
                pop r15
                pop r10
                pop rbx
                pop rbp
                ret

            inner_not_found:
                inc r9d
                cmp r9d, ebx
                jl inner_loop
                jmp outer_loop
