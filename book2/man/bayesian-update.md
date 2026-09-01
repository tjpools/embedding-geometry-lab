```text
BAYESIAN-UPDATE(3)               Book Two Man Pages              BAYESIAN-UPDATE(3)

NAME
       bayesian-update - redistribute probability over hypotheses given evidence

SYNOPSIS
       w(h) = P(evidence | h) * P(h)
       P(h | evidence) = w(h) / sum_h w(h)

DESCRIPTION
       Given a prior distribution over a declared, exhaustive hypothesis space
       and a likelihood model for one observation, the posterior weights each
       hypothesis by prior times likelihood, then normalizes by the total
       weight. The posterior sums to one and remains strictly between zero and
       one for every hypothesis that is not already certain.

       The posterior depends on the declared prior and likelihood model, not
       only on the observed evidence string. Changing either input changes the
       result for the same evidence.

NOTES
       A posterior is not a decision; a decision requires a threshold or loss
       function not supplied here. A likelihood is not its inverse:
       P(evidence | h) != P(h | evidence).

       This weighting arithmetic - multiply, sum, normalize - recurs later as
       the softmax(3) kernel inside attention(2). Shared arithmetic is not
       shared interpretation: a posterior is conditioned on a declared
       hypothesis space and likelihood model, an attention weight is not.

SEE ALSO
       softmax(3), attention(2), gradient-descent(3)

SOURCE
       Chapter 3, Bayesian update probe.
```
