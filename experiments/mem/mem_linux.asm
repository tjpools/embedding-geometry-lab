; Experiment 06 — Memory Manifold
; x86-64 NASM Linux, SysV ABI
;
; MemProbe() -> int (eax)
;   Computes Fibonacci(20) iteratively using only registers.
;   No heap allocation. No stack beyond the return address.
;   Zero temporal curvature: calling this N times costs the same as calling it once.
;   The past does not accumulate in silicon.

section .text
    global MemProbe

MemProbe:
    ; Iterative Fibonacci — register-only, no memory access
    ; eax = a (previous), ecx = b (current), edx = loop counter
    xor  eax, eax       ; a = 0
    mov  ecx, 1         ; b = 1
    mov  edx, 20        ; N iterations
.loop:
    add  eax, ecx       ; a = a + b  (new value)
    xchg eax, ecx       ; rotate: ecx holds the new b, eax holds old b
    dec  edx
    jnz  .loop
    mov  eax, ecx       ; return final value
    ret
