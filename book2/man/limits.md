```text
LIMITS(7)                        Book Two Man Pages                      LIMITS(7)

NAME
       limits - typed constraint boundaries: context, representation, compute, vocabulary, decoding, contribution

SYNOPSIS
       CONTEXT_CAPACITY_EXCEEDED
       BLOCK_INPUT_WIDTH_MISMATCH
       M(n,d), A(n,d), E(n)          (structural operation counts)
       <unk> collision
       policy-dependent argmax
       contribution-control output delta

DESCRIPTION
       Six constraints on the Chapter 15 execution-trace(1) fixture are varied
       one at a time, each producing its own result type: an admission record
       (context), an interface-gate record (representation width),
       sequence-dependent structural counts (compute), an ID collision
       (vocabulary coverage), a selected-ID change under an explicit
       eligibility set (decoding), and a numerical output difference
       (zeroing the attention contribution before the first residual).

NOTES
       These six result types are not interchangeable measurements: a
       rejected shape, an arithmetic count, and a changed token ID answer
       different questions. None of them establishes production usable
       context, benchmark performance, semantic understanding, or which
       component is "most important" in a trained model. Structural counts
       are not timings; a numerical sensitivity is not semantic importance.

SEE ALSO
       execution-trace(1), tensor(7), attention(2)

SOURCE
       Chapter 16, measured-limits probe.
```
