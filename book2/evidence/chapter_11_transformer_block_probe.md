# Chapter 11 Probe — Transformer Architectural Elevation

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_11_transformer_block_probe.py](chapter_11_transformer_block_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_11.md](../chapter_briefs/chapter_11.md)

## Claims Under Test

1. A minimal transformer block requires more than attention: positional combination, multi-head composition, output projection, residual paths, normalization, and feed-forward interfaces.
2. In a fixed deterministic fixture, each head can have distinct normalized attention rows while sharing the same incoming representation sequence.
3. Residual and normalization equations can be verified exactly for recorded intermediate tensors.
4. Removing projected multi-head attention before the first residual changes final outputs, exposing component contribution.

## Declared Fixture

- positions: 4
- model dimension: 4
- attention heads: 2
- per-head dimension: 2
- feed-forward hidden dimension: 6
- normalization epsilon: $10^{-9}$

Use fixed incoming token rows $X$ and fixed positional rows $P$, then combine them row-wise:

$$
H_0 = X + P.
$$

Apply fixed matrices:

$$
Q = H_0W_Q,\quad K = H_0W_K,\quad V = H_0W_V.
$$

Split each row into two heads. For head $h$ and query row $i$:

$$
s^{(h)}_{ij} = \frac{q^{(h)}_i\cdot k^{(h)}_j}{\sqrt{d_h}},
\qquad
\alpha^{(h)}_{ij} = \operatorname{softmax}(s^{(h)}_{i\cdot})_j,
$$

$$
z^{(h)}_i = \sum_j \alpha^{(h)}_{ij} v^{(h)}_j.
$$

Concatenate heads and project:

$$
Z = \operatorname{Concat}(z^{(1)},z^{(2)})W_O.
$$

Apply residual and normalization:

$$
R_1 = H_0 + Z,
\qquad
N_1 = \operatorname{LN}(R_1).
$$

Apply positionwise feed-forward with ReLU:

$$
F_1 = \operatorname{ReLU}(N_1W_1+b_1),
\qquad
F_2 = F_1W_2+b_2.
$$

Apply second residual and normalization:

$$
R_2 = N_1 + F_2,
\qquad
N_2 = \operatorname{LN}(R_2).
$$

Layer normalization is declared as:

$$
\operatorname{LN}(x)=\frac{x-\operatorname{mean}(x)}{\sqrt{\operatorname{var}(x)+\varepsilon}}.
$$

## Control

Run a no-attention control that sets projected multi-head output $Z$ to zero before the first residual while keeping all inputs, positional rows, and other fixed matrices unchanged.

This isolates the contribution of the attention branch inside the block. It is not a claim about learned causality in trained systems.

## Validation Gates

- declared dimensions match all recorded tensor shapes
- every attention weight row in both heads sums to one within $10^{-12}$
- head 1 and head 2 contain at least one non-identical weight row
- first residual equation $R_1=H_0+Z$ holds for all rows
- second residual equation $R_2=N_1+F_2$ holds for all rows
- $N_1$ row means are near zero and row variances near one under the declared formula
- $N_2$ row means are near zero and row variances near one under the declared formula
- rerunning the probe produces identical final outputs
- the no-attention control changes final output rows

All gates pass.

## Observed Result

For query row 4:

- head 1 weights: $(0.231425,0.224919,0.236720,0.306937)$
- head 2 weights: $(0.316628,0.297562,0.194005,0.191805)$

After concatenation and output projection:

$$
Z_4 \approx (0.162918,-0.060338,0.457843,-0.006945).
$$

After second residual and normalization:

$$
N_{2,4} \approx (0.255460,-1.698430,0.654426,0.788544).
$$

No-attention control difference norms (per position):

$$
(0.905029,1.337468,0.464690,0.254784).
$$

All values reproduce identically on rerun.

## Evidence Boundary

The probe establishes deterministic block arithmetic and interface composition in one fixed fixture. It does not train parameters, evaluate language tasks, model decoding behavior, measure runtime latency or throughput, reproduce full token-through-machine execution, or establish architecture limits beyond this bounded block experiment.