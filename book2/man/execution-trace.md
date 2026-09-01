```text
EXECUTION-TRACE(1)               Book Two Man Pages              EXECUTION-TRACE(1)

NAME
       execution-trace - one request moved through validated stages in runtime order

SYNOPSIS
       text -> tokens -> ids -> embed+position -> [gate] -> block -> select-row
            -> project -> argmax -> decode

DESCRIPTION
       A fixed request crosses tokenization, vocabulary lookup, embedding and
       positional addition, a shape-validation gate, transformer-block(8)
       execution, final-row selection, vocabulary projection, deterministic
       argmax (lowest-ID tie rule), and decode. Every stage records status,
       input/output shape, expected shape, a work-count inventory, and a
       digest or concrete value. A corrupted-width control fails at the first
       gate and marks every downstream stage "unexecuted" rather than filling
       in guessed values.

NOTES
       Work counts (multiplications, additions, exponentials) are structural
       arithmetic inventories, not elapsed time, latency, throughput, memory
       traffic, or hardware utilization. Output is judged for arithmetic
       correctness, not fluency or semantic appropriateness.

SEE ALSO
       transformer-block(8), architecture-scales(7), limits(7)

SOURCE
       Chapter 15, token-through-machine probe.
```
