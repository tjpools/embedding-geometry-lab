# Chapter 10 Probe — Attention Opens Direct Paths

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_10_attention_paths_probe.py](chapter_10_attention_paths_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_10.md](../chapter_briefs/chapter_10.md)

## Claims Under Test

1. Scaled dot-product attention forms normalized weights from query-key scores and outputs from weighted value combinations.
2. In the declared attention graph, an earlier value contributes directly to a later output rather than traversing every intervening recurrent state.
3. Attention weights do not contain the value vectors they scale: changing only one value can change outputs while leaving all scores and weights fixed.
4. A causal mask excludes future key-value positions by rule rather than assigning them low learned compatibility.

## Declared Fixture

Use five positions with two-dimensional query, key, and value vectors:

$$
Q=((1,0),(0,1),(1,1),(-1,1),(0.5,-0.5)),
$$

$$
K=((1,0),(0,1),(1,1),(-1,0),(0.5,-0.5)),
$$

$$
V=((1,0),(0,1),(1,1),(-1,1),(0.5,-1)).
$$

For query position $i$ and key position $j$, compute

$$
s_{ij}=\frac{q_i\cdot k_j}{\sqrt{2}}.
$$

For every admitted position in a row, compute

$$
\alpha_{ij}=\frac{\exp(s_{ij})}{\sum_m\exp(s_{im})}.
$$

The output is

$$
o_i=\sum_j\alpha_{ij}v_j.
$$

## Value-Only Control

Change only the first value by

$$
\Delta v_1=(0.4,-0.2).
$$

Queries and keys remain fixed. Therefore scores and weights must remain exactly equal. For every output row,

$$
o_i'-o_i=\alpha_{i1}\Delta v_1.
$$

This equality isolates the role of the value vector. It does not establish a causal explanation of a trained model.

## Causal Mask

For output position $i$, admit only key-value positions $j\le i$. Excluded positions receive recorded output weight zero and are omitted from the softmax denominator.

The mask is a declared architectural rule. A zero masked weight is not evidence that a learned score found the position irrelevant.

## Structural Path Comparison

Use two declared abstract graphs:

```text
recurrent: x1 -> h1 -> h2 -> h3 -> h4 -> h5
attention contribution: v1 -> o5
```

The corresponding edge counts are five and one. They describe these graphs only. They are not timing, kernel, memory, throughput, or quality measurements.

## Validation Gates

- every query, key, value, contribution, and output has dimension two
- every full-attention weight row sums to one within $10^{-12}$
- every causal weight row sums to one within $10^{-12}$
- every future position in the causal case has weight exactly zero
- every output equals the sum of its recorded contributions
- the value-only control preserves scores and weights exactly
- every observed control output difference matches the fixed weight times $\Delta v_1$ within $10^{-12}$
- the direct-path and recurrent-path edge counts remain labeled as structural
- rerunning the probe produces identical structured output

All gates pass.

## Observed Result

For the fifth query, full attention produced:

| Position | Score | Weight | Weighted value contribution |
|---:|---:|---:|---:|
| 1 | 0.353553 | 0.271126 | $(0.271126,0)$ |
| 2 | -0.353553 | 0.133684 | $(0,0.133684)$ |
| 3 | 0 | 0.190381 | $(0.190381,0.190381)$ |
| 4 | -0.353553 | 0.133684 | $(-0.133684,0.133684)$ |
| 5 | 0.353553 | 0.271126 | $(0.135563,-0.271126)$ |

The weights sum to one and the contributions sum to

$$
o_5=(0.463386,0.186623).
$$

Changing only $v_1$ by $(0.4,-0.2)$ preserved the complete score and weight matrices. The final output changed by

$$
(0.108450,-0.054225)
=0.271126(0.4,-0.2)
$$

within floating-point tolerance. Every causal row normalized to one, and every excluded future position had recorded weight zero.

## Evidence Boundary

The probe establishes arithmetic and graph structure for one fixed, one-head attention fixture. It does not train projection matrices, implement multi-head attention or a transformer block, measure causal influence, validate semantic interpretation, compare task quality, or benchmark runtime performance.