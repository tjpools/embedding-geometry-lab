# Chapter 4 Source Ledger — Transformations and Change

**Status:** Source basis established August 13, 2026  
**Scope:** linear maps, matrix representation, multivariable derivatives, Jacobians, and finite-difference checking

## Sources

### S1 — Axler, *Linear Algebra Done Right*

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Springer, 2024.

- URL: https://linear.axler.net/
- Accessed: August 13, 2026
- Authority: established advanced undergraduate textbook; fourth edition openly published by its author
- Supports: linear maps as maps preserving addition and scalar multiplication; matrices as representations of linear maps after bases are selected; composition of linear maps
- Limitation: Chapter 4 uses a finite-dimensional real-coordinate case and does not import the book's broader operator theory.

### S2 — OpenStax, *Calculus Volume 3*

Gilbert Strang and Edwin “Jed” Herman, *Calculus Volume 3*, OpenStax, 2016, sections 2.2–2.4.

- URL: https://openstax.org/details/books/calculus-volume-3
- Accessed: August 13, 2026
- Authority: peer-reviewed open textbook from Rice University
- Supports: partial derivatives, differentiability of multivariable functions, directional derivatives, and the multivariable chain rule
- Limitation: The source supplies calculus definitions and examples, not claims about machine learning or transformer architecture.

### S3 — SciPy `check_grad` Documentation

SciPy community, “`scipy.optimize.check_grad`,” SciPy API reference.

- URL: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.check_grad.html
- Accessed: August 13, 2026
- Authority: official documentation for a widely used scientific-computing library
- Supports: comparing an implemented derivative with a finite-difference approximation as a computational check
- Limitation: The chapter's probe is dependency-free, uses a central directional difference, and does not call SciPy or claim that one numerical match proves a derivative correct universally.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Linear maps preserve addition and scalar multiplication. | S1 | The two preservation laws define linearity; the probe checks them for declared inputs. |
| A matrix represents a linear map only relative to coordinate choices. | S1 | The worked matrix acts on declared coordinates and is not an intrinsic meaning of the vectors. |
| A derivative is a local approximation. | S2 | The Jacobian at a point predicts first-order output change near that point. |
| Finite differences can check derivative code. | S3 | Decreasing error in the recorded case supports consistency between the analytic Jacobian and the executable map. |

## Prohibited Inferences

The sources and probe do not warrant claims that every transformation is linear, every function is differentiable, a local derivative describes global behavior, a Jacobian measures intelligence, or differentiation alone performs learning or optimization.
