; Experiment 04 — Sphere Manifold
; x86-64 Linux NASM — x87 FPU substrate
;
; SphereVolume(double r) -> double (returned in xmm0, per SysV ABI)
;
; Uses x87 FLDPI — the CPU's own 80-bit extended-precision encoding of π.
; This is the deepest hardware approximation available: ~18-19 significant
; decimal digits. Still not π. Still a ghost of a departed quantity.
;
; Formula: V = (4/3) * π * r³
;
; Calling convention: xmm0 = r (double, per SysV x86-64 float ABI)
; Return:            xmm0 = V (double)
;
; NASM note: fldl/fstpl are GAS mnemonics.
;   NASM uses: fld qword [mem]  /  fstp qword [mem]

section .data
    four_thirds  dq 1.3333333333333333   ; 4/3 as double

section .text
    global SphereVolume

SphereVolume:
    sub     rsp, 8
    movsd   [rsp], xmm0           ; spill r to memory (x87 loads from mem)

    ; Build r^3 on x87 stack, cleaning up as we go
    fld     qword [rsp]           ; ST0 = r
    fld     st0                   ; ST0 = r, ST1 = r
    fmulp   st1, st0              ; ST0 = r^2  (pops one r)
    fld     qword [rsp]           ; ST0 = r, ST1 = r^2
    fmulp   st1, st0              ; ST0 = r^3  (pops r)

    ; Multiply by π
    fldpi                         ; ST0 = π, ST1 = r^3
    fmulp   st1, st0              ; ST0 = π * r^3

    ; Multiply by 4/3
    fld     qword [rel four_thirds] ; ST0 = 4/3, ST1 = π*r^3
    fmulp   st1, st0              ; ST0 = (4/3) * π * r^3

    ; Return in xmm0 (SysV ABI)
    fstp    qword [rsp]           ; store and pop x87 result
    movsd   xmm0, [rsp]          ; move to SSE return register

    add     rsp, 8
    ret
