section .text
global _start

_start:
    mov rax, [rsp] ; argc
    cmp rax, 2
    jl bad_exit

    mov rdi, [rsp+0x10] ; argv[1] = input.txt
    mov eax, 2      ; sys_open
    xor esi, esi    ; O_RDONLY
    syscall         ; open(input.txt, "r")

    cmp rax, -1
    je bad_exit

    sub rsp, 144
    mov edi, eax    ; fd
    mov eax, 5      ; sys_fstat
    mov rsi, rsp
    syscall         ; fstat(fd, rsp)

    cmp rax, -1
    je bad_exit

    mov rax, 9          ; sys_mmap
    mov r8, rdi         ; fd
    xor edi, edi        ; addr = 0
    mov rsi, [rsp+48]   ; len = fstat.st_size
    mov edx, 1          ; PROT_READ
    mov r10, 0x08001    ; MAP_SHARED | MAP_POPULATE
    xor r9, r9          ; offset = 0
    syscall             ; mmap(0, fstat.st_size, PROT_READ, MAP_SHARED | MAP_POPULATE, fd, 0)

    cmp rax, -1
    je bad_exit

    ; rsi = len
    ; rax = input
    ; r8, r9, r10, r11 = last 4 numbers

    ; exit 0
    xor edi, edi
    mov eax, 60
    syscall

    bad_exit:
        ; exit -1
        mov edi, -1
        mov eax, 60
        syscall
