# Chapter 9 Probe — Recurrent State and Dependency

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_09_recurrent_runtime_probe.py](chapter_09_recurrent_runtime_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_09.md](../chapter_briefs/chapter_09.md)

## Claims Under Test

1. Each state in a declared recurrence depends on the preceding state, producing an ordered forward dependency path.
2. Final-state sensitivity to an earlier input is a product of local derivatives along the intervening recurrent path in the worked scalar case.
3. Setting the recurrent weight to zero removes cross-position sensitivity while retaining the per-position input transformation.
4. Structural dependency and operation counts do not constitute runtime performance measurements.

## Declared Recurrence

Use the ordered input sequence

$$
x=(0.2,-0.1,0.4,0.0,-0.2),
$$

initial state $h_0=0.1$, recurrent weight $w=0.5$, and update

$$
a_t=wh_{t-1}+x_t,
$$

$$
h_t=\tanh(a_t).
$$

The same value of $w$ is used at every step. Hidden states are step-specific values, not shared storage identities.

## Sensitivity

For input position $j$, the local input derivative is

$$
\frac{\partial h_j}{\partial x_j}=1-h_j^2.
$$

For each later step,

$$
\frac{\partial h_t}{\partial h_{t-1}}=w(1-h_t^2).
$$

Therefore the final-state sensitivity is

$$
\frac{\partial h_T}{\partial x_j}
=(1-h_j^2)\prod_{t=j+1}^{T}w(1-h_t^2).
$$

The implementation must compare every analytic value with a central finite difference using $\epsilon=10^{-6}$.

## Zero-Recurrence Control

Set $w=0$ while holding the input sequence, initial state, activation, and finite-difference procedure fixed. Then

$$
h_t=\tanh(x_t),
$$

so $h_T$ must be insensitive to $x_1$ through $x_{T-1}$ and sensitive only to $x_T$.

This control removes the recurrent path. It does not model attention, parallel execution, or a trained non-recurrent architecture.

## Structural Counts

For a sequence of length $T$, record:

- $T$ recurrent updates
- $T$ predecessor-state edges, including $h_0\rightarrow h_1$
- $T$ state reads
- $T$ state writes
- forward dependency depth $T$

These are counts in the declared scalar computation. They are not measured bytes, allocations, kernel launches, latency, throughput, utilization, or energy.

## Validation Gates

- every state and pre-activation is finite
- the trace contains one state per input plus the initial state
- every state names its immediate predecessor
- every analytic sensitivity matches its finite-difference check within $10^{-9}$
- the first-input sensitivity traverses all five updates and remains nonzero in the base case
- the zero-recurrence control produces zero analytic and numerical sensitivity for positions 1 through 4 within tolerance
- the zero-recurrence final position retains nonzero sensitivity
- rerunning the probe produces identical structured output

All gates pass.

## Observed Result

The base recurrence produced the state trace

$$
(0.1,0.2449187,0.0224556,0.3895147,0.1923317,-0.1034626).
$$

The final-state sensitivities were:

| Input | Analytic | Finite difference | Absolute error |
|---:|---:|---:|---:|
| $x_1$ | 0.047455899 | 0.047455899 | $9.06\times10^{-12}$ |
| $x_2$ | 0.100968403 | 0.100968403 | $1.90\times10^{-12}$ |
| $x_3$ | 0.202038684 | 0.202038684 | $1.54\times10^{-11}$ |
| $x_4$ | 0.476349989 | 0.476349989 | $1.15\times10^{-11}$ |
| $x_5$ | 0.989295495 | 0.989295495 | $5.85\times10^{-12}$ |

With recurrent weight zero, sensitivities for $x_1$ through $x_4$ were zero analytically and numerically. Final-input sensitivity was approximately $0.961043$. The structural record contains five updates, five predecessor-state edges, five state reads, five state writes, dependency depth five, and zero runtime measurements.

## Evidence Boundary

The probe establishes exact state, dependency, derivative, and count results for one scalar recurrence. It does not establish training behavior, general recurrent-network performance, LSTM or GRU behavior, framework scheduling, kernel fusion, hardware concurrency, memory traffic, elapsed time, or a universal account of vanishing and exploding gradients.