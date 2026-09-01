```text
TRANSFORMER-BLOCK(8)             Book Two Man Pages             TRANSFORMER-BLOCK(8)

NAME
       transformer-block - assembled attention, residual, normalization, feed-forward stage

SYNOPSIS
       H0 = X + P
       Q,K,V = H0 Wq, H0 Wk, H0 Wv
       Z = Concat(head_1..head_h) Wo
       R1 = H0 + Z ;  N1 = layer-norm(R1)
       F  = feed-forward(N1)
       R2 = N1 + F ;  N2 = layer-norm(R2)

DESCRIPTION
       Input rows are combined with positional information, projected into
       per-head queries/keys/values, passed through attention(2), concatenated
       and output-projected, composed with the entry path by a residual(3)
       addition, normalized (layer-norm(3)), transformed per-position by
       feed-forward(3), and composed and normalized a second time. Zeroing
       the projected attention contribution before the first residual, with
       everything else fixed, measurably changes every final output row.

NOTES
       Attention alone is not this block: removing the surrounding interfaces
       loses positional entry, multi-head subspaces, residual routing,
       normalization, and the feed-forward stage. This is a fixed,
       deterministic, untrained fixture: no optimizer, no corpus loss, no
       tokenization or decoding pipeline, no encoder-decoder cross-attention,
       no causal decoder mask. It is an encoder-style block slice, not a full
       stack or production model.

SEE ALSO
       attention(2), residual(3), layer-norm(3), feed-forward(3),
       architecture-scales(7), execution-trace(1)

SOURCE
       Chapter 11, transformer-block probe.
```
