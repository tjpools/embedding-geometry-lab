# Chapter 5 Source Ledger — Memory, Types, and Translation

**Status:** Source basis established August 13, 2026  
**Scope:** Rust types, `repr(C)` layout, size and alignment, compiler rejection, and MIR translation

## Sources

### S1 — The Rust Reference: Type Layout

Rust Project Developers, “Type Layout,” *The Rust Reference*.

- URL: https://doc.rust-lang.org/reference/type-layout.html
- Accessed: August 13, 2026
- Authority: official language reference
- Supports: layout as size, alignment, and relative field offsets; primitive sizes; limited guarantees of the default Rust representation; declaration-order and padding algorithm for `repr(C)` structs
- Limitation: alignment can be platform-specific, layout does not alone determine function-call ABI compatibility, and the chapter reports one concrete target result rather than universalizing it.

### S2 — Rust Compiler Development Guide: MIR

Rust Compiler Team, “The MIR (Mid-level IR),” *Rust Compiler Development Guide*.

- URL: https://rustc-dev-guide.rust-lang.org/mir/index.html
- Accessed: August 13, 2026
- Authority: official rustc implementation guide
- Supports: MIR as a control-flow-graph-based intermediate representation constructed from HIR; explicit MIR types; use in flow-sensitive checks, optimization, and code generation
- Limitation: human-readable MIR output is subject to change, and MIR is not identical to source or final machine instructions.

### S3 — Rust Compiler Error Index: E0308

Rust Project Developers, “E0308: Mismatched types,” *Rust Compiler Error Index*.

- URL: https://doc.rust-lang.org/error_codes/E0308.html
- Accessed: August 13, 2026
- Authority: official rustc diagnostic documentation
- Supports: a compiler type mismatch occurs when an expression has a type different from the expected type
- Limitation: one rejected mismatch does not establish that the type system proves program purpose or correctness.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Type declarations constrain admitted source values. | S3 | rustc rejects the probe's integer where a Boolean field is required. |
| Layout includes size, alignment, and offsets. | S1 | The probe reports all three for its declared `repr(C)` record and environment. |
| Representation policy affects layout guarantees. | S1 | `repr(C)` supplies field-order and padding rules not guaranteed by default `repr(Rust)`. |
| Compilation crosses intermediate forms. | S2 | The accepted typed source can be inspected in MIR before later code generation. |

## Prohibited Inferences

The sources do not warrant claims that source intent survives translation without change, type checking proves correctness, `repr(C)` makes every type portable, MIR is a stable interchange format, or one source construct corresponds to one machine instruction.
