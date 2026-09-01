```text
SOFTMAX(3)                       Book Two Man Pages                     SOFTMAX(3)

NAME
       softmax - normalize scores into a nonnegative row summing to one

SYNOPSIS
       alpha_j = exp(s_j) / sum_m exp(s_m)

DESCRIPTION
       Exponentiate every score in a row, sum the results, and divide each
       exponentiated score by that sum. The output row is nonnegative and
       sums to one. Every entry in the row is coupled: changing one admitted
       score changes the shared denominator and can change every normalized
       weight in the row.

NOTES
       A softmax row is a normalized weighting distribution, not a Bayesian
       posterior (bayesian-update(3)): no hypothesis space, prior, or
       likelihood model is conditioned here. On hardware this is exponentiate,
       reduce-sum, normalize - a fused kernel, not three independent passes in
       a production implementation. Shared arithmetic with bayesian-update(3)
       is not shared interpretation.

SEE ALSO
       attention(2), bayesian-update(3)

SOURCE
       Chapter 10, attention-paths probe.
```
