# Chapter 7 Source Ledger — Tensors and Parallel Machines

**Status:** Source basis established August 13, 2026  
**Scope:** batched matrix multiplication, GPU execution structure, specialized tensor hardware, and performance boundaries

## Sources

### S1 — NumPy Matrix Multiplication Reference

NumPy Developers, “numpy.matmul,” *NumPy Reference*.

- URL: https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
- Accessed: August 13, 2026
- Authority: official NumPy API reference
- Supports: conventional multiplication for two-dimensional arrays; treatment of higher-dimensional inputs as stacks of matrices; compatibility signature $(n,k),(k,m)\rightarrow(n,m)$; batched result-shape semantics
- Limitation: The Chapter 7 probe uses the Python standard library and implements only equal batch dimensions, not NumPy broadcasting or its optimized execution paths.

### S2 — NVIDIA CUDA Programming Guide

NVIDIA, *CUDA Programming Guide*, updated May 27, 2026.

- URL: https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html
- Accessed: August 13, 2026
- Authority: official documentation for the CUDA programming model and GPU execution
- Supports: GPU kernels and the organization of work through threads, thread blocks, and grids; the distinction between a program's work decomposition and its execution on CUDA-capable hardware
- Limitation: The probe does not compile or execute CUDA code and cannot establish scheduling behavior or performance on any GPU.

### S3 — Jouppi et al.

Norman P. Jouppi et al., “In-Datacenter Performance Analysis of a Tensor Processing Unit,” *Proceedings of the 44th Annual International Symposium on Computer Architecture*, 2017.

- URL: https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/
- Accessed: August 13, 2026
- Authority: primary peer-reviewed architecture paper and official Google Research publication record
- Supports: the evaluated TPU as a domain-specific inference accelerator; its 65,536 8-bit multiply-accumulate matrix unit; the importance of workload, memory, execution model, latency requirements, and deployment context in reported performance
- Limitation: The reported first-generation TPU results belong to specified production inference workloads and contemporaneous hardware. They do not establish present-day or universal accelerator speedups.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Higher-dimensional arrays can represent stacks of matrices for batched multiplication. | S1 | The probe multiplies shapes $(2,2,3)$ and $(2,3,2)$ to obtain $(2,2,2)$. |
| Independent output coordinates expose a possible work partition. | S1, probe | Eight output cells are assigned disjointly across four abstract lanes and reproduce the serial reference. |
| GPUs provide explicit parallel execution structures. | S2 | CUDA organizes kernel work through threads, blocks, and grids; the probe does not execute those structures. |
| Tensor accelerators can include specialized matrix-multiply machinery. | S3 | The evaluated TPU contains a large 8-bit multiply-accumulate matrix unit for its documented inference workloads. |
| Hardware performance depends on more than arithmetic shape. | S2, S3 | Scheduling, memory, precision, workload, and implementation remain part of any measured performance claim. |

## Prohibited Inferences

The sources and probe do not warrant claims that tensors intrinsically execute in parallel, partitionable work guarantees concurrent execution, accelerators always outperform CPUs, every tensor operation maps efficiently to every device, operation count predicts elapsed time, or the first-generation TPU results generalize to current hardware and arbitrary workloads.