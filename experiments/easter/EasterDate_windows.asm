; ------------------------------------------------------------
; EasterDate_windows.asm -- Original Windows MASM source
; Preserved verbatim as artifact.
;
; This is the original x64 Windows MASM implementation of the
; Gauss Easter algorithm, using the Windows x64 ABI:
;   Input:  RCX = year
;   Output: EAX = day, ECX = month, EDX = weekday (placeholder)
;
; Ported to Linux NASM as easter_linux.asm for runtime use.
; ------------------------------------------------------------

include common.inc

.code main$B

public EasterDate
EasterDate proc
    ; -------------------------------------------
    ; Prologue: Preserve Non-Volatile Registers
    ; Required by Windows x64 ABI because we use RBX, R12-R15
    ; -------------------------------------------
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15

    ; a = year % 19
    mov     eax, ecx
    cdq
    mov     ebx, 19
    div     ebx
    mov     r8d, edx                ; a

    ; b = year / 100
    mov     eax, ecx
    mov     ebx, 100
    xor     edx, edx
    div     ebx
    mov     r9d, eax                ; b
    mov     r10d, edx               ; c = year % 100

    ; d = b / 4
    mov     eax, r9d
    shr     eax, 2                  ; Divide by 4 (2 bits right)
    mov     r11d, eax               ; d

    ; e = b % 4
    mov     eax, r9d
    and     eax, 3                  ; Modulo 4 (keep last 2 bits)
    mov     r12d, eax               ; e

    ; f = (b + 8) / 25
    mov     eax, r9d
    add     eax, 8
    mov     ebx, 25
    xor     edx, edx
    div     ebx
    mov     r13d, eax               ; f

    ; g = (b - f + 1) / 3
    mov     eax, r9d
    sub     eax, r13d
    add     eax, 1
    mov     ebx, 3
    xor     edx, edx
    div     ebx
    mov     r14d, eax               ; g

    ; h = (19a + b - d - g + 15) % 30
    mov     eax, r8d
    imul    eax, 19
    add     eax, r9d
    sub     eax, r11d
    sub     eax, r14d
    add     eax, 15
    mov     ebx, 30
    cdq
    div     ebx
    mov     r15d, edx               ; h

    ; i = c / 4
    mov     eax, r10d
    shr     eax, 2                  ; Divide by 4
    mov     r8d, eax                ; i

    ; k = c % 4
    mov     eax, r10d
    and     eax, 3                  ; Modulo 4
    mov     r9d, eax                ; k

    ; l = (32 + 2e + 2i - h - k) % 7
    mov     eax, 32
    add     eax, r12d
    add     eax, r12d               ; 2e
    add     eax, r8d
    add     eax, r8d                ; 2i
    sub     eax, r15d               ; -h
    sub     eax, r9d                ; -k
    mov     ebx, 7
    cdq
    div     ebx
    mov     r10d, edx               ; l

    ; m = (a + 11h + 22l) / 451
    ; Broken logic fixed here:
    ; scale factors *11 and *22 must be calculated via IMUL first.
    
    imul    eax, r15d, 11           ; eax = 11 * h
    imul    ebx, r10d, 22           ; ebx = 22 * l
    add     eax, ebx                ; eax = 11h + 22l
    add     eax, r8d                ; eax = a + 11h + 22l

    mov     ebx, 451
    xor     edx, edx
    div     ebx
    mov     r11d, eax               ; m

    ; month = (h + l - 7m + 114) / 31
    mov     eax, r15d
    add     eax, r10d
    mov     ebx, r11d
    imul    ebx, 7
    sub     eax, ebx
    add     eax, 114
    mov     ebx, 31
    xor     edx, edx
    div     ebx
    mov     ecx, eax                ; month

    ; day = ((h + l - 7m + 114) % 31) + 1
    mov     eax, edx
    inc     eax                     ; day to EAX

    ; Weekday placeholder (calculated by Weekday.asm)
    xor     edx, edx

    ; -------------------------------------------
    ; Epilogue: Restore Non-Volatile Registers
    ; -------------------------------------------
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    ret
EasterDate endp

end
