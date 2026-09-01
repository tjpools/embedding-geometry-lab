```text
RESIDUAL(3)                      Book Two Man Pages                    RESIDUAL(3)

NAME
       residual - compose a branch output with its entry path by addition

SYNOPSIS
       R = H + Z

DESCRIPTION
       The output of a transformed branch (e.g. attention or feed-forward) is
       added, coordinate-wise, to the value that entered the branch. Both
       operands must share dimension. The equation is verified row-by-row
       against declared fixture values.

NOTES
       Residual composition is not normalization and not the branch
       transformation itself; each stage in transformer-block(8) has a
       distinct contract. This page does not establish why residual paths aid
       trainability at depth beyond citing the architectural principle.

SEE ALSO
       transformer-block(8), layer-norm(3)

SOURCE
       Chapter 11, transformer-block probe; He et al. (residual networks).
```
