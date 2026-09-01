```text
REPRESENTATION(3)                Book Two Man Pages               REPRESENTATION(3)

NAME
       representation - map source text to a vocabulary identifier and vector

SYNOPSIS
       normalize(text) -> tokens
       lookup(token, vocabulary) -> identifier
       select(identifier, table) -> vector

DESCRIPTION
       Source text is normalized (Unicode NFC, case folding, trim), split into
       tokens, and each token is assigned an integer identifier by a declared
       vocabulary. The identifier selects one row of a lookup table. Renumbering
       the vocabulary and permuting the table together preserves the selected
       row; the identifier is an assigned index, not an intrinsic property of
       the token.

       A vocabulary miss falls back to <unk>, ID 0. Distinct absent tokens can
       collapse onto the same identifier and vector; the fallback discards the
       distinction between them.

NOTES
       An identifier is not a meaning. A coordinate is meaningful only relative
       to its basis and vocabulary. This page does not train a table, interpret
       vector directions, or establish task adequacy.

       At Transformer scale, this same lookup is the embedding layer: hardware
       executes it as a memory-bound gather from contiguous rows, not an
       arithmetic-bound computation. Training changes which vectors occupy the
       rows; it does not change the indexing operation.

SEE ALSO
       tensor(7), embedding-space(7)

SOURCE
       Chapter 2, representation probe.
```
