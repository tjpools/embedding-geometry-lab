# Chapter 7 Probe — Tensor Work on Parallel Lanes

**Status:** Verified August 13, 2026  
**Implementation:** [chapter_07_tensor_parallel_probe.py](chapter_07_tensor_parallel_probe.py)  
**Dependencies:** Python standard library only

## Claims Under Test

1. Compatible stacks of matrices can produce a batched matrix-multiplication result with a declared output shape.
2. Distinct output coordinates can be partitioned into disjoint work assignments.
3. A complete partition can reproduce a serial reference exactly.
4. A work plan that omits one output coordinate does not reproduce the declared result.

## Inputs and Operation

The left tensor has shape $(2,2,3)$:

```text
[
  [[ 1,  2, 0], [-1,  3, 1]],
  [[ 2,  0, 1], [ 1, -2, 2]]
]
```

The right tensor has shape $(2,3,2)$:

```text
[
  [[1, 2], [0, 1], [ 3, -1]],
  [[2, 1], [1, 0], [-1,  2]]
]
```

For batch $b$, row $i$, and column $j$, the probe computes

$$
C_{b,i,j}=\sum_{k=0}^{2} A_{b,i,k}B_{b,k,j}.
$$

The batch dimensions agree, and the left inner dimension equals the right inner dimension. The output shape is therefore $(2,2,2)$.

## Serial Reference

The serial traversal produces:

```text
[
  [[ 1, 4], [ 2, 0]],
  [[ 3, 4], [-2, 5]]
]
```

There are eight output coordinates. Each requires three scalar product terms, for 24 terms in the declared operation.

## Work Partition

Coordinates are assigned round-robin across four abstract lanes:

| Lane | First assignment | Second assignment |
|---:|---|---|
| 0 | $(0,0,0)$ | $(1,0,0)$ |
| 1 | $(0,0,1)$ | $(1,0,1)$ |
| 2 | $(0,1,0)$ | $(1,1,0)$ |
| 3 | $(0,1,1)$ | $(1,1,1)$ |

No two lanes write the same output coordinate. Executing every assignment produces exactly the serial reference.

The lanes are a deterministic work decomposition. The Python probe executes them sequentially and does not demonstrate concurrent hardware execution.

## Omitted-Work Control

The control removes coordinate $(1,1,1)$ from lane 3. Its assembled result ends with:

```text
[[3, 4], [-2, null]]
```

The incomplete result differs from the serial reference and contains seven rather than eight writes. This control establishes that the equality check can detect an incomplete plan.

## Validation Gates

- batch and contracted inner dimensions are compatible
- every output coordinate is assigned exactly once
- the complete partition matches the serial reference
- lane writes are disjoint
- the omitted-work control fails equivalence with one `null` cell
- rerunning the probe produces identical structured output

All gates pass.

## Evidence Boundary

The probe establishes arithmetic and partition behavior for two fixed input tensors, one batched matrix multiplication, four abstract lanes, and one omitted-coordinate control.

It does not establish:

- actual concurrent execution
- CPU, GPU, TPU, or accelerator performance
- speedup, throughput, utilization, latency, or energy use
- memory-transfer, cache, scheduling, kernel-launch, or synchronization cost
- optimal work partitioning or tiling
- numerical behavior under reduced precision
- that every tensor operation has independent output coordinates
- that computational arrays exhaust the mathematical meaning of tensors