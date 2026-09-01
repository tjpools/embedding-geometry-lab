```text
RECURRENCE(7)                    Book Two Man Pages                  RECURRENCE(7)

NAME
       recurrence - ordered state update with a predecessor dependency

SYNOPSIS
       h_t = tanh(w * h_(t-1) + x_t)

DESCRIPTION
       A recurrent update reuses one parameterized function while carrying a
       hidden state from position to position. Computing h_t requires h_(t-1);
       the dependency can be unrolled into a feed-forward graph with repeated
       parameters. Sensitivity of a late state to an early input is a product
       of per-step factors along the path and can attenuate or amplify
       depending on the weight and activation.

NOTES
       A dependency graph is not a runtime measurement; an edge count is not
       elapsed time. A scalar state is not complete recall of its inputs, and
       "memory" here names a recurrent role, not persistence or addressability
       in the ordinary sense. Setting the recurrent weight to zero removes the
       predecessor link entirely and is the control that isolates the claim.

SEE ALSO
       tensor(7), attention(2)

SOURCE
       Chapter 9, recurrent-bottleneck probe.
```
