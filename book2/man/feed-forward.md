```text
FEED-FORWARD(3)                  Book Two Man Pages                 FEED-FORWARD(3)

NAME
       feed-forward - per-position nonlinear transformation between two projections

SYNOPSIS
       F1 = ReLU(N W1 + b1)
       F2 = F1 W2 + b2

DESCRIPTION
       Each row is projected to a wider hidden dimension, passed through
       ReLU, then projected back to model dimension with a second bias. The
       transformation is applied independently per position: it does not mix
       information across positions the way attention(2) does.

NOTES
       Feed-forward is a distinct sublayer contract inside transformer-block(8),
       not a substitute for attention's cross-position mixing role. Its role
       is transformation of a row's content, not comparison across rows.

SEE ALSO
       transformer-block(8), attention(2)

SOURCE
       Chapter 11, transformer-block probe.
```
