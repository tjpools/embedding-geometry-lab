# Chapter 6 Source Ledger — Learning by Adjustment

**Status:** Source basis established August 13, 2026  
**Scope:** objectives, empirical risk, gradient descent, learning rate, affine neural units, and backpropagation lineage

## Sources

### S1 — Goodfellow, Bengio, and Courville

Ian Goodfellow, Yoshua Bengio, and Aaron Courville, *Deep Learning*, MIT Press, 2016, Chapter 8, “Optimization for Training Deep Models.”

- URL: https://www.deeplearningbook.org/contents/optimization.html
- Accessed: August 13, 2026
- Authority: established technical monograph published by MIT Press
- Supports: training as optimization of an objective; empirical-risk framing; gradient-based methods; optimization difficulties specific to neural-network training
- Limitation: The chapter uses one affine unit and full-batch deterministic gradient descent, not the book's complete treatment of deep optimization.

### S2 — Google Machine Learning Crash Course

Google, “Linear regression: Gradient descent,” *Machine Learning Crash Course*.

- URL: https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent
- Accessed: August 13, 2026
- Authority: official technical educational material
- Supports: iterative loss calculation, gradient direction, learning-rate-scaled parameter movement, repeated updates, and loss-curve inspection
- Limitation: The page's pedagogical linear-regression case does not establish convergence for arbitrary neural networks or hyperparameters.

### S3 — Rumelhart, Hinton, and Williams

David E. Rumelhart, Geoffrey E. Hinton, and Ronald J. Williams, “Learning representations by back-propagating errors,” *Nature* 323 (1986): 533–536. DOI: 10.1038/323533a0.

- URL: https://doi.org/10.1038/323533a0
- Accessed: August 13, 2026
- Authority: primary peer-reviewed historical research article
- Supports: back-propagated error as a historically important method for adjusting weights in layered networks
- Limitation: The probe does not implement a multilayer network or backpropagation and does not claim this paper originated every component of gradient-based learning.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Training can be posed as minimizing a declared objective over data. | S1, S2 | The probe minimizes expected squared training error over four equally weighted examples. |
| Gradient descent repeats loss, gradient, and update operations. | S1, S2 | The selected base rate reduces the recorded loss over 12 steps. |
| Update size matters. | S1, S2, probe | The control rate increases loss in the declared case; gradient direction alone does not guarantee every step improves. |
| Error backpropagation is part of neural-network history. | S3 | Layered-network training later uses chain-rule derivatives to assign parameter adjustments; the probe stops at one affine unit. |

## Prohibited Inferences

The sources and probe do not warrant claims that optimization guarantees generalization, every neural objective is convex, gradient descent always converges, training loss measures intelligence, artificial neurons reproduce biological neurons, or parameter adjustment establishes understanding.
