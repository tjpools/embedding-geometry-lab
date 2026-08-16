# Chapter 7 Brief — Tensors and Parallel Machines

**Status:** Verified; Part II integrated  
**Part:** II — Learning Systems  
**Modules:** `math.tensors`, `programming.hardware`  
**Visual anchor:** **Tensor Work on Parallel Lanes**

## Reader Entry

Chapter 6 adjusted two parameters through repeated scalar loss and gradient calculations. The reader may still treat a tensor as merely a larger matrix, equate partitionable work with actual concurrent execution, or assume that moving an operation to an accelerator guarantees a speedup.

## Intended Exit

The reader can distinguish:

- a matrix from a batch of matrices with explicit shape
- an axis from the size recorded along that axis
- compatible contraction dimensions from batch and output dimensions
- one output cell from the reduction required to compute it
- independent output work from its assignment to execution lanes
- mathematical parallelism from scheduled hardware concurrency
- a GPU thread hierarchy from a TPU matrix-multiply unit
- operation count from memory movement and elapsed time
- theoretical throughput from measured application performance
- deterministic arithmetic evidence from hardware benchmarking

## Central Question

How does a multidimensional numerical operation expose work that parallel hardware can schedule without changing the declared result?

## Chapter Claim

For a compatible batched matrix multiplication, output cells can be indexed independently, assigned across disjoint work lanes, and assembled into the same tensor as a serial reference. GPUs and tensor accelerators provide execution structures suited to abundant numerical work, but realized performance remains conditional on implementation, data movement, precision, scheduling, workload size, and hardware.

The [verified tensor-partition probe](../evidence/chapter_07_tensor_parallel_probe.md) supports the worked decomposition. The [source ledger](../evidence/chapter_07_sources.md) grounds stacked matrix multiplication and accelerator architecture claims.

## Chapter Result

The probe multiplies tensors with shapes $(2,2,3)$ and $(2,3,2)$ to produce shape $(2,2,2)$. It assigns eight output cells across four abstract lanes, performs 24 scalar product terms, and exactly matches the serial reference. Each output coordinate is written once. Removing one assigned coordinate leaves a `null` cell and fails equivalence, showing that a complete, disjoint work plan is necessary for this decomposition.

## Dependency Alignment

**Incoming edge:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.matrices` | `math.tensors` | Matrix multiplication supplies the contracted row-column operation extended across a batch axis. |

**Internal edge:**

| Source | Target | Chapter use |
|---|---|---|
| `math.tensors` | `programming.hardware` | Independent output coordinates expose numerical work that can be assigned to parallel execution structures. |

**Outgoing edges:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `math.tensors` | `math.geometry` | 8 | Multi-axis representations become objects whose slices, distances, and neighborhoods can be inspected under declared geometric assumptions. |
| `programming.hardware` | `programming.runtimes` | 9 | Parallel work requires scheduling, kernels, and memory movement on concrete execution machinery. |
| `math.tensors` | `ai.transformer` | 11 | Batched tensor operations support the later assembly of attention and feed-forward computation. |

## Reader Movement

1. Declare computational tensors as shaped multidimensional numerical arrays.
2. Separate rank, axes, shape, and stored values.
3. Extend matrix multiplication across one batch axis.
4. Derive output shape from compatible dimensions.
5. Index each output cell and its inner reduction.
6. Partition output coordinates across four abstract lanes.
7. Assemble lane results and compare them with a serial reference.
8. Remove one assignment and observe failed equivalence.
9. Map the exposed work to GPU thread hierarchies and specialized matrix hardware.
10. Separate structural suitability from benchmarked performance.

## Visual Anchor

**Tensor Work on Parallel Lanes** is one structural diagram containing:

- two batched input tensors and their declared shapes
- eight output coordinates partitioned across four labeled lanes
- the three scalar product terms accumulated for each output cell
- a recombined $(2,2,2)$ result equal to the serial reference
- a dashed omitted-work control ending in one visibly absent output cell

**Structural reveal:** the tensor operation contains a complete set of independently indexed output tasks; a work partition preserves the result only when every coordinate is assigned exactly once.

The lanes represent an abstract partition, not measured GPU threads. All values and assignments must derive from the probe.

## Verification Questions

- Are input and output shapes declared before the operation?
- Are batch, row, inner, and column dimensions kept distinct?
- Does every output coordinate contain exactly three product terms?
- Are output coordinates assigned once with no overlap?
- Does the complete partition equal the serial reference?
- Does the omitted-work control fail equality visibly?
- Is concurrency described as an execution possibility rather than a measured fact?
- Are GPU and TPU mechanisms kept architecturally distinct?
- Are speedup, energy, latency, and utilization claims limited to sourced contexts?
- Does the chapter avoid redefining tensors as an ontology or measure of intelligence?

## Explicit Exclusions

This chapter does not benchmark a CPU, GPU, TPU, or other accelerator. It does not execute a CUDA kernel, inspect a device scheduler, model caches, prove optimal tiling, compare numerical precision, or claim that every tensor operation parallelizes in the same way. It uses *tensor* in the computational sense of a shaped multidimensional array and does not develop coordinate-free tensor algebra.

## Narrative Transition

Chapter 7 exposes shaped numerical work and the hardware interface that can execute it. Chapter 8 interprets learned representations geometrically under explicit assumptions. Chapter 9 then adds runtime scheduling, kernels, memory movement, and ordered sequence computation.

## Drafting Gate

Prose began only after the probe, source ledger, and deterministic visual production package passed validation. The completed chapter preserves the brief's claim boundary and has passed probe, visual, link, analytics, source, and manuscript checks.