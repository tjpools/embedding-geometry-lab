```text
TENSOR(7)                        Book Two Man Pages                     TENSOR(7)

NAME
       tensor - shaped multidimensional array and its partitionable work

SYNOPSIS
       C[b,i,j] = sum_k A[b,i,k] * B[b,k,j]

DESCRIPTION
       A tensor is a shaped multidimensional array; its shape assigns axes to
       batch, row, column, or other declared groupings. Batched matrix
       multiplication is defined per matching batch index, contracting one
       shared inner dimension. Output coordinates can be partitioned into
       disjoint, complete lane assignments that reproduce a serial reference
       exactly; an incomplete assignment leaves a detectable missing
       coordinate rather than a plausible wrong number.

NOTES
       Partitionable is not parallel: a work plan divided into lanes is not
       the same claim as concurrent execution on hardware. An operation count
       is not an elapsed time. This page does not measure GPU speedup,
       memory traffic, or kernel launch cost.

SEE ALSO
       gradient-descent(3), attention(2), recurrence(7)

SOURCE
       Chapter 7, tensor-parallel probe.
```
