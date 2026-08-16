# Chapter 5 Probe — Intent Through the Compiler

**Status:** Verified August 13, 2026  
**Rust source:** [chapter_05_intent_through_compiler.rs](chapter_05_intent_through_compiler.rs)  
**Probe:** [chapter_05_intent_through_compiler_probe.py](chapter_05_intent_through_compiler_probe.py)

## Claims Under Test

1. A source-level field type rejects an inadmissible value before executable output is produced.
2. A declared `repr(C)` record has an inspectable size, alignment, and field offsets in the recorded environment.
3. rustc translates the typed source function and record construction into MIR while retaining explicit types.
4. The accepted program produces deterministic output for the declared input.

## Declared Record

```rust
#[repr(C)]
struct TokenRecord {
    identifier: u32,
    weight: f32,
    active: bool,
}
```

Compile-time assertions require:

| Property | Recorded value |
|---|---:|
| size | 12 bytes |
| alignment | 4 bytes |
| `identifier` offset | 0 |
| `weight` offset | 4 |
| `active` offset | 8 |

The trailing bytes complete the total size required for array stride and alignment. The program does not interpret padding bytes as values.

## Translation and Rejection Cases

The accepted function computes `identifier as f32 * weight` when `active` is true and zero otherwise. Three Rust tests verify layout, active behavior, and inactive behavior.

The wrapper also creates a temporary source variant that changes

```rust
active: true
```

to

```rust
active: 1
```

rustc exits unsuccessfully and reports mismatched types. The invalid source is temporary and is not a repository artifact.

For accepted source, stable rustc emits MIR containing the typed function boundary

```text
fn weighted_identifier(_1: TokenRecord) -> f32
```

and a `TokenRecord` construction. The probe checks only these stable-enough substrings for the recorded toolchain; it does not treat complete MIR text as a publication-stable format.

## Environment and Observed Output

- `rustc 1.97.1 (8bab26f4f 2026-07-14)`
- Rust 2024 edition
- warnings denied

```text
size=12
alignment=4
offsets=identifier:0,weight:4,active:8
weighted_identifier=1.5
```

All three tests and all six wrapper validations pass.

## Evidence Boundary

The probe establishes compiler behavior, layout, MIR markers, and runtime output only for the declared source, toolchain, target environment, and commands.

It does not establish:

- the layout of a default `repr(Rust)` struct
- one universal C ABI across targets
- one-to-one correspondence between source expressions, MIR statements, or machine instructions
- a stable MIR serialization contract
- optimization quality or a particular assembly sequence
- runtime scheduling, allocation strategy, cache behavior, or hardware cost
- that a compiler verifies program purpose, empirical correspondence, or task adequacy
