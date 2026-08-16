# Chapter 5 Brief — Memory, Types, and Translation

**Status:** Verified; Part I integrated  
**Part:** I — Structures  
**Modules:** `programming.memory`, `programming.compilers`  
**Visual anchor:** **Intent Through the Compiler**

## Reader Entry

Chapters 2 and 4 established numerical representations and transformations. The reader may still treat a source declaration, typed value, memory layout, compiler intermediate representation, executable, and runtime behavior as interchangeable versions of one unchanged object.

## Intended Exit

The reader can distinguish:

- source-level declaration from admitted value
- static type checking from proof of program correctness
- a type from its concrete layout
- size, alignment, field offset, and padding
- default representation from a declared layout contract
- source syntax from compiler intermediate representation
- accepted translation from optimized machine instruction selection
- compilation from runtime scheduling and hardware execution

## Central Question

What must happen before a declared numerical object becomes a typed, laid-out, translated, and executable program artifact?

## Chapter Claim

Programming representations acquire additional constraints as they cross source typing, layout, and compiler translation. Types reject some source constructions; representation attributes and target rules determine inspectable layout; intermediate representations preserve information needed for checks and later code generation without maintaining a one-to-one correspondence with source text.

The [verified Rust probe](../evidence/chapter_05_intent_through_compiler_probe.md) supports the concrete case. The [source ledger](../evidence/chapter_05_sources.md) grounds Rust language and compiler claims. The visual anchor and production tests are recorded in [../visuals/chapter_05_intent_through_compiler.md](../visuals/chapter_05_intent_through_compiler.md).

## Chapter Result

In the recorded Rust 1.97.1 environment, a `repr(C)` `TokenRecord` has size 12, alignment 4, and field offsets 0, 4, and 8. Three tests pass. The accepted record produces `weighted_identifier=1.5`; changing the Boolean field value from `true` to integer `1` is rejected as a type mismatch. Emitted MIR contains the typed function boundary and record construction.

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `programming.representation` | `programming.memory` | Numerical representations exist before their storage layout is inspected. |
| `programming.languages` | `programming.compilers` | Source-language declarations exist before compiler checks and translation. |
| `programming.representation` | `programming.compilers` | Represented values and operations become compiler inputs. |

There is no internal DAG edge from `programming.memory` to `programming.compilers`. The chapter joins them through one typed record whose layout is checked during compilation and observed by the accepted executable.

**Outgoing edges:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `programming.memory` | `programming.runtimes` | 9 | Laid-out values later participate in allocation, movement, and ordered execution. |
| `programming.compilers` | `programming.runtimes` | 9 | Translated artifacts later enter runtime scheduling and execution. |

## Reader Movement

1. Declare one typed record with a representation policy.
2. Show the compiler accepting valid field values and rejecting one invalid value.
3. Calculate size, alignment, offsets, and trailing padding.
4. Distinguish `repr(C)` guarantees from default Rust representation.
5. Apply one typed function to the record.
6. Inspect the typed function and construction in emitted MIR.
7. Run the accepted executable and reproduce its output.
8. Separate type acceptance from program purpose and task adequacy.
9. Separate compilation from runtime scheduling and hardware behavior.
10. Hand memory and compiler artifacts to Chapter 9.

## Visual Anchor

**Intent Through the Compiler** is one left-to-right execution trace:

```text
source declaration
    -> type check
    -> declared layout
    -> MIR
    -> accepted executable output
```

A rejected side branch at type checking shows `active: 1` stopping before layout and translation. The layout stage exposes offsets 0, 4, and 8 plus trailing padding to size 12. The MIR stage shows only the bounded typed signature, not an invented full compiler pipeline.

**Structural reveal:** source intent becomes executable only by crossing distinct enforcement and translation interfaces; rejection at one interface prevents later artifacts from existing.

## Verification Questions

- Is the type mismatch kept distinct from semantic or task correctness?
- Are size, alignment, offsets, and padding distinguished?
- Are layout claims scoped to `repr(C)`, the fields, and recorded environment?
- Is MIR described as intermediate rather than source or machine code?
- Does the chapter avoid one-source-line/one-instruction claims?
- Are runtime scheduling and hardware cost reserved for later chapters?
- Can every visual value be reproduced by the probe?

## Explicit Exclusions

This chapter does not explain borrow checking in depth, LLVM internals, linker behavior, assembly instruction selection, allocator implementation, caches, runtime scheduling, kernels, or hardware performance. It does not claim that types prove purpose or that compilation preserves human intention intact.

## Narrative Transition

Part I ends when source-level structure has crossed typing, layout, and translation into an executable artifact. Chapter 6 begins Part II by combining the derivative machinery from Chapter 4 with objectives and repeated parameter adjustment. Chapter 9 later resumes the programming path with runtimes, memory movement, and ordered execution.

## Drafting Gate

Prose begins only after the Rust probe, source ledger, and deterministic visual production package pass validation. All three gates are complete. The verified manuscript is [../chapters/chapter_05.md](../chapters/chapter_05.md). Its Part I interfaces are recorded in the [integration audit](../evidence/part_01_integration.md).
