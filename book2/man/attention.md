```text
ATTENTION(2)                     Book Two Man Pages                    ATTENTION(2)

NAME
       attention - weighted combination of values by query-key compatibility

SYNOPSIS
       s_ij = (q_i . k_j) / sqrt(d_k)
       alpha_ij = softmax(s_i.)_j
       o_i = sum_j alpha_ij * v_j

DESCRIPTION
       Each position supplies a query, key, and value vector (produced by
       learned projections in a Transformer; fixed vectors in the fixture
       here). Scaled dot-product scores between a query and every admitted
       key are normalized by softmax(3) into a nonnegative row summing to one.
       Each weight scales its value vector; the output sums those weighted
       contributions. A causal mask can zero out positions after the current
       one before normalization.

       Holding the weight matrix fixed while changing only one value vector
       changes the output but not the displayed weights: a weight display
       alone does not specify the resulting numerical contribution.

NOTES
       Not Bayesian: no hypotheses, prior, likelihood model, or evidence-
       conditioning operation is present. Normalized weights are not Bayesian
       posteriors, causal explanations, or semantics (bayesian-update(3)). A
       direct query-key edge is not a runtime measurement; a large weight is
       not automatically causal importance; a masked zero has a different
       origin than a small unmasked weight. Attention is one operator inside
       transformer-block(8), not the whole architecture.

SEE ALSO
       softmax(3), bayesian-update(3), transformer-block(8)

SOURCE
       Chapter 10, attention-paths probe.
```
