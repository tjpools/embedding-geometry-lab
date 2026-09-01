```text
MEMORY-LAYOUT(7)                 Book Two Man Pages                MEMORY-LAYOUT(7)

NAME
       memory-layout - typed field layout: size, alignment, offset

SYNOPSIS
       #[repr(C)] struct { field: type, ... }
       size_of, align_of, offset_of

DESCRIPTION
       A type system admits or rejects a source value before any layout exists.
       Once accepted, a declared representation (e.g. repr(C)) fixes field
       order, alignment-driven padding, and total size rounded to struct
       alignment. Compile-time and runtime assertions can verify size,
       alignment, and per-field offsets for one toolchain and target.

NOTES
       A type is not a layout; a layout is not a proof of program purpose or
       correctness. Default (non-C) representations do not guarantee field
       order is preserved. This page does not measure allocation, cache
       behavior, or hardware cost.

       The same layout contract - declared size, alignment, offset - is what a
       tensor(7) library enforces for every weight matrix and activation
       buffer at runtime, across memory hierarchies this page does not model.

SEE ALSO
       tensor(7), execution-trace(1)

SOURCE
       Chapter 5, compiler probe (Rust, repr(C)).
```
