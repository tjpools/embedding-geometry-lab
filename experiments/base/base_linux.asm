; Experiment 05 — Base Manifold
; x86-64 NASM Linux, SysV ABI
;
; BaseAdd() -> int (eax)
;   Computes 4+3 at the instruction level.
;   Returns 7 — the base-invariant quantity.
;   The frame (base) is applied in the shim; this substrate knows nothing of it.

section .text
    global BaseAdd

BaseAdd:
    mov  eax, 4
    add  eax, 3     ; 4+3 = 7, in every base
    ret
