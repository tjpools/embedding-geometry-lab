; ------------------------------------------------------------
; easter_linux.asm -- Pure Computation (Linux NASM port)
; Gauss's Easter algorithm, ported from Windows MASM EasterDate.asm.
;
; ABI: System V x86-64
;   Input:  EDI = year
;   Output: EAX = month * 100 + day  (standard C int return)
;           e.g. Easter 2025 -> 4*100+20 = 420
;
; Register map:
;   R15D = year (saved)   R11D = a    R14D = g -> h
;   R12D = e              R13D = f -> m
;   R8D, R9D, R10D = working (b/c/d/i/k/l)
; ------------------------------------------------------------

section .text
global EasterDate

EasterDate:
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15

    mov     r15d, edi               ; save year

    ; a = year % 19
    mov     eax, r15d
    cdq
    mov     ebx, 19
    idiv    ebx
    mov     r11d, edx               ; r11d = a

    ; b = year / 100,  c = year % 100
    mov     eax, r15d
    xor     edx, edx
    mov     ebx, 100
    div     ebx
    mov     r8d, eax                ; r8d = b
    mov     r9d, edx                ; r9d = c

    ; d = b / 4
    mov     eax, r8d
    shr     eax, 2
    mov     r10d, eax               ; r10d = d

    ; e = b % 4
    mov     eax, r8d
    and     eax, 3
    mov     r12d, eax               ; r12d = e

    ; f = (b + 8) / 25
    mov     eax, r8d
    add     eax, 8
    xor     edx, edx
    mov     ebx, 25
    div     ebx
    mov     r13d, eax               ; r13d = f

    ; g = (b - f + 1) / 3
    mov     eax, r8d
    sub     eax, r13d
    add     eax, 1
    xor     edx, edx
    mov     ebx, 3
    div     ebx
    mov     r14d, eax               ; r14d = g

    ; h = (19a + b - d - g + 15) % 30
    mov     eax, r11d
    imul    eax, 19
    add     eax, r8d
    sub     eax, r10d
    sub     eax, r14d
    add     eax, 15
    cdq
    mov     ebx, 30
    idiv    ebx
    mov     r14d, edx               ; r14d = h

    ; i = c / 4
    mov     eax, r9d
    shr     eax, 2
    mov     r8d, eax                ; r8d = i

    ; k = c % 4
    mov     eax, r9d
    and     eax, 3
    mov     r9d, eax                ; r9d = k

    ; l = (32 + 2e + 2i - h - k) % 7
    mov     eax, 32
    add     eax, r12d
    add     eax, r12d
    add     eax, r8d
    add     eax, r8d
    sub     eax, r14d
    sub     eax, r9d
    cdq
    mov     ebx, 7
    idiv    ebx
    mov     r10d, edx               ; r10d = l

    ; m = (a + 11h + 22l) / 451
    imul    eax, r14d, 11
    imul    ebx, r10d, 22
    add     eax, ebx
    add     eax, r11d               ; + a (r11d still = a)
    xor     edx, edx
    mov     ebx, 451
    div     ebx
    mov     r13d, eax               ; r13d = m

    ; month = (h + l - 7m + 114) / 31
    mov     eax, r14d
    add     eax, r10d
    imul    ebx, r13d, 7
    sub     eax, ebx
    add     eax, 114
    xor     edx, edx
    mov     ebx, 31
    div     ebx
    mov     r8d, eax                ; r8d = month

    ; day = remainder + 1
    inc     edx                     ; edx = day

    ; Pack: EAX = month * 100 + day
    imul    eax, r8d, 100
    add     eax, edx

    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    ret
