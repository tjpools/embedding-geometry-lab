```text
ALIGNMENT(7)                     Book Two Man Pages                   ALIGNMENT(7)

NAME
       alignment - exact typed match between an export and a destination requirement

SYNOPSIS
       accept(source_module, capability_id, interface_id) iff
           graph edge exists AND triple matches a destination requirement exactly

DESCRIPTION
       Three lineage exports - an architectural relation (AI), a declared
       transform/compare rule (mathematics), and a validated callable-package(8)
       contract (programming) - are matched against named destination
       requirements by an exact typed triple, not by vocabulary resemblance.
       Every requirement must be satisfied exactly once: no missing match, no
       duplicate match. Source identity is retained through the match, not
       discarded.

NOTES
       A shared word (e.g. "transform") does not authorize substitution for a
       different requirement; a missing dependency-graph edge is a distinct
       failure from an available but non-matching export. Alignment produces
       one outgoing edge to architecture-scales(7); it does not itself
       inspect the resulting object.

SEE ALSO
       transformer-block(8), callable-package(8), architecture-scales(7)

SOURCE
       Chapter 13, lineage-alignment probe.
```
