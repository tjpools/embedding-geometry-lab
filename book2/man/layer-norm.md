```text
LAYER-NORM(3)                    Book Two Man Pages                  LAYER-NORM(3)

NAME
       layer-norm - rescale a row to near-zero mean and near-unit variance

SYNOPSIS
       LN(x) = (x - mean(x)) / sqrt(var(x) + epsilon)

DESCRIPTION
       For each row, subtract its mean and divide by the square root of its
       variance plus a small epsilon. Applied per row (per example), not
       across a batch. In the fixture, recorded output rows have mean near
       zero and variance near one under this exact formula.

NOTES
       The check validates the declared arithmetic for this fixture; it does
       not assert training behavior or optimization dynamics. Normalization is
       not the residual(3) addition and not the feed-forward(3) stage that
       follows it.

SEE ALSO
       transformer-block(8), residual(3)

SOURCE
       Chapter 11, transformer-block probe; Ba, Kiros, Hinton (layer normalization).
```
