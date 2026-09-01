```text
EMBEDDING-SPACE(7)               Book Two Man Pages              EMBEDDING-SPACE(7)

NAME
       embedding-space - coordinates, distance, and transformation of learned points

SYNOPSIS
       euclidean(u, v) = sqrt(sum (u_i - v_i)^2)
       cosine(u, v)    = (u . v) / (|u| |v|)

DESCRIPTION
       A learned representation assigns a coordinate to each item under a
       model, data set, task, and training procedure. Euclidean distance and
       cosine similarity can rank neighbors differently for the same points.
       Rigid rotation preserves Euclidean neighborhoods; invertible anisotropic
       scaling can change them while preserving all coordinate information.

NOTES
       Proximity is not meaning. "Nearest neighbor" is incomplete until the
       representation and comparison rule are both named. A visual direction
       on a projected plot is not automatically an intrinsic direction in the
       represented domain. This page does not perform training or claim
       semantic interpretation.

SEE ALSO
       tensor(7), jacobian(3), representation(3)

SOURCE
       Chapter 8, learned-space probe.
```
