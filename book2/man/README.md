# Book Two — Man Pages

**Status:** established August 31, 2026

This is not a glossary and not an appendix. It is a lookup layer, in the Unix man-page tradition: terse, structured, tool-oriented reference for the transformer's components. Each page describes what one component does, not what it means. Interpretation, boundaries, and disclaimers stay attached to every entry, because the narrative chapters earn those boundaries and the man pages must not spend them for free.

Run `man <name>` mentally by opening the matching file. Every page cites the chapter whose probe verified its claims; the man page asserts nothing the chapter did not already establish. Start with [man(7)](man.md) if you want the convention explained before the components.

## Why This Exists

A question-and-answer tool gives an answer and the interaction ends. This layer is built to do something different: expose stable, inspectable primitives - one per operation - so a reader can compose their own understanding in whatever order their own confusion demands, the way a Unix reference sheet let a programmer look things up without breaking flow.

That only works if the primitives are trustworthy. If one page overclaimed - if `softmax` quietly became a Bayesian posterior, or `attention` quietly became explanation - every later composition built on it would inherit the error. The terseness of these pages and the epistemic discipline in their NOTES sections are the same design choice, not two separate ones. A tool's value is not the answer it emits; it is whether its primitives hold up under whatever the reader builds on top of them.

## Index (apropos)

| Name | Section | One-line description | Source |
|---|---|---|---|
| [man](man.md) | 7 | what this lookup layer is, and what it is not | this directory |
| [representation](representation.md) | 3 | map source text to a numerical identifier and vector | [Ch2](../chapters/chapter_02.md) |
| [bayesian-update](bayesian-update.md) | 3 | redistribute probability over hypotheses given evidence | [Ch3](../chapters/chapter_03.md) |
| [jacobian](jacobian.md) | 3 | local linear approximation of a differentiable map | [Ch4](../chapters/chapter_04.md) |
| [memory-layout](memory-layout.md) | 7 | typed field layout: size, alignment, offset | [Ch5](../chapters/chapter_05.md) |
| [gradient-descent](gradient-descent.md) | 3 | adjust parameters by a scaled negative gradient | [Ch6](../chapters/chapter_06.md) |
| [tensor](tensor.md) | 7 | shaped multidimensional array and its partitionable work | [Ch7](../chapters/chapter_07.md) |
| [embedding-space](embedding-space.md) | 7 | coordinates, distance, and transformation of learned points | [Ch8](../chapters/chapter_08.md) |
| [recurrence](recurrence.md) | 7 | ordered state update with a predecessor dependency | [Ch9](../chapters/chapter_09.md) |
| [attention](attention.md) | 2 | weighted combination of values by query-key compatibility | [Ch10](../chapters/chapter_10.md) |
| [softmax](softmax.md) | 3 | normalize scores into a nonnegative row summing to one | [Ch10](../chapters/chapter_10.md) |
| [transformer-block](transformer-block.md) | 8 | assembled attention, residual, normalization, feed-forward stage | [Ch11](../chapters/chapter_11.md) |
| [residual](residual.md) | 3 | compose a branch output with its entry path by addition | [Ch11](../chapters/chapter_11.md) |
| [layer-norm](layer-norm.md) | 3 | rescale a row to near-zero mean and near-unit variance | [Ch11](../chapters/chapter_11.md) |
| [feed-forward](feed-forward.md) | 3 | per-position nonlinear transformation between two projections | [Ch11](../chapters/chapter_11.md) |
| [callable-package](callable-package.md) | 8 | validated serialized model bound to a runtime and interface | [Ch12](../chapters/chapter_12.md) |
| [alignment](alignment.md) | 7 | exact typed match between an export and a destination requirement | [Ch13](../chapters/chapter_13.md) |
| [architecture-scales](architecture-scales.md) | 7 | one architecture identity viewed at system, stack, block, operation scope | [Ch14](../chapters/chapter_14.md) |
| [execution-trace](execution-trace.md) | 1 | one request moved through validated stages in runtime order | [Ch15](../chapters/chapter_15.md) |
| [limits](limits.md) | 7 | typed constraint boundaries: context, representation, compute, vocabulary, decoding, contribution | [Ch16](../chapters/chapter_16.md) |

## Section Conventions

- **1** — executable trace / user-observable run
- **2** — core operator
- **3** — mathematical or scalar procedure
- **7** — architectural or structural concept
- **8** — packaging, alignment, and administration

## Page Format

```text
NAME
SYNOPSIS
DESCRIPTION
NOTES        (boundaries this page must not cross)
SEE ALSO
SOURCE       (chapter and probe this page is grounded in)
```
