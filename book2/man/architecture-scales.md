```text
ARCHITECTURE-SCALES(7)           Book Two Man Pages           ARCHITECTURE-SCALES(7)

NAME
       architecture-scales - one architecture identity viewed at system, stack, block, operation scope

SYNOPSIS
       system { contains stack { contains block[0..n] { contains attention, ffn, ... } } }

DESCRIPTION
       One fixed architecture ID is inspected at four scopes: system (external
       token-in / logits-out boundary), stack (repeated block instances sharing
       one contract), block (attention plus residual/normalization/feed-forward
       children), and operation (one selected component, e.g. attention). Each
       scope exposes only its own owned interfaces; containment edges are
       exact and acyclic.

NOTES
       Containment is not execution order: "which object owns this" and
       "which operation runs next" are different relations, verified
       separately. A complete, exact attention(2) row cannot stand in for the
       system scope - it lacks the required system interfaces even though it
       carries the same architecture ID. Repetition (three blocks, one
       contract) is not one block existing in three places.

SEE ALSO
       transformer-block(8), execution-trace(1), alignment(7)

SOURCE
       Chapter 14, four-scales probe.
```
