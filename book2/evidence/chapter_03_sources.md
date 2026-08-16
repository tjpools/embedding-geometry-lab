# Chapter 3 Source Ledger — Reasoning Under Uncertainty

**Status:** Source basis established August 12, 2026  
**Scope:** Probability, Bayesian conditioning, sensitivity to assumptions, and probabilistic graphical models in AI  
**Chapter brief:** [../chapter_briefs/chapter_03.md](../chapter_briefs/chapter_03.md)

## Source Standard

This ledger grounds the chapter's mathematical and historical framing. The executable arithmetic remains grounded separately by [chapter_03_bayesian_update_probe.md](chapter_03_bayesian_update_probe.md).

Sources are used only for the claims named below. A source about Bayesian methodology does not establish that the chapter's illustrative door hypotheses or likelihoods correspond to a physical system.

## Sources

### S1 — NIST/SEMATECH e-Handbook

National Institute of Standards and Technology, "How can Bayesian methodology be used for reliability evaluation?" section 8.1.10 of the *NIST/SEMATECH e-Handbook of Statistical Methods*.

- URL: https://www.itl.nist.gov/div898/handbook/apr/section1/apr1a.htm
- Accessed: August 12, 2026
- Authority: United States national measurement institute technical handbook
- Supports: Bayes' formula; prior, likelihood, and posterior roles; total-probability normalization; sensitivity of conclusions to prior assumptions
- Limitation: The page's application domain is reliability evaluation. Chapter 3 uses its probability statements, not its reliability-specific parameter or interval claims.

### S2 — Stanford Encyclopedia of Philosophy

James Joyce, "Bayes' Theorem," *The Stanford Encyclopedia of Philosophy*, first published June 28, 2003, substantive revision September 30, 2003.

- URL: https://plato.stanford.edu/entries/bayes-theorem/
- Accessed: August 12, 2026
- Authority: Peer-reviewed reference work published by Stanford's Metaphysics Research Lab
- Supports: The definition of conditional probability; the distinction between $P(H\mid E)$ and $P(E\mid H)$; Bayes' theorem in two-hypothesis form; the dependence of conditional results on unconditional probabilities and likelihoods
- Limitation: The entry surveys philosophical interpretations of probability and evidence. Chapter 3 does not adopt those interpretations as technical conclusions.

### S3 — Bayes' Original Essay

Thomas Bayes, "LII. An essay towards solving a problem in the doctrine of chances," communicated by Richard Price, *Philosophical Transactions of the Royal Society of London* 53, 370–418.

- DOI: https://doi.org/10.1098/rstl.1763.0053
- Crossref publication date: December 31, 1763
- Accessed: August 12, 2026
- Authority: Primary historical source
- Supports: Historical origin of the inverse-probability problem later associated with Bayes' theorem
- Limitation: The chapter must not project current terminology, graphical models, or modern AI concepts into the original essay. Bibliographies sometimes cite the paper as 1764; use the journal and DOI metadata consistently in final references.

### S4 — Pearl's Belief-Network Paper

Judea Pearl, "Fusion, propagation, and structuring in belief networks," *Artificial Intelligence* 29, no. 3 (September 1986): 241–288.

- DOI: https://doi.org/10.1016/0004-3702(86)90072-X
- Accessed: August 12, 2026
- Authority: Primary peer-reviewed AI research article
- Supports: Belief networks as a named computational subject within AI and the historical presence of structured probabilistic reasoning in the field by 1986
- Limitation: One paper does not establish that probabilistic methods replaced rule-based AI or that all directed probabilistic edges are causal.

### S5 — Probabilistic Graphical Models

Daphne Koller and Nir Friedman, *Probabilistic Graphical Models: Principles and Techniques*. Cambridge, MA: MIT Press, 2009. ISBN 978-0-262-01319-2.

- URL: https://mitpress.mit.edu/9780262013192/probabilistic-graphical-models/
- Accessed: August 12, 2026
- Authority: Technical monograph in the MIT Press Adaptive Computation and Machine Learning series
- Supports: Probabilistic graphical models as an AI framework for representation, inference, and learning under uncertainty; coverage of Bayesian and undirected networks
- Limitation: The chapter uses only the introductory distinction between graphical representation and inference. Learning, complex networks, causal inference, and decision making remain outside its worked probe.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Conditional probability reverses neither term automatically nor semantically. | S1, S2 | $P(H\mid E)$ and $P(E\mid H)$ are distinct conditional probabilities related by Bayes' theorem. |
| The posterior combines a prior and likelihood through normalization. | S1, S2 | For the declared exhaustive hypotheses and nonzero evidence probability, posterior mass is proportional to prior mass times likelihood. |
| Bayesian output depends on model assumptions. | S1, S2 | Changing the declared prior or likelihood can change the posterior. |
| Bayes' theorem has a historical source in Bayes' inverse-probability problem. | S2, S3 | Bayes' posthumously published essay is a historical source for the problem later associated with the theorem. |
| Probabilistic belief networks are part of AI's technical history. | S4, S5 | By the 1980s, belief networks were an explicit research subject in AI; later graphical-model treatments organize representation, inference, and learning. |
| A graphical model makes selected dependence structure explicit. | S4, S5 | The chapter's edge $H\rightarrow E$ declares the conditional factorization used by the toy model. |

## Prohibited Inferences

The sources do not warrant claims that:

- Bayesian inference eliminates uncertainty
- a larger posterior is a true state, decision, or action
- the chapter's illustrative likelihoods measure a real indicator
- a directed edge alone proves physical causation
- belief networks replaced symbolic AI
- all AI inference is Bayesian
- Bayesian probability is the uniquely correct interpretation of uncertainty
- posterior probabilities are confidence intervals

## Drafting Requirement

Every sourced technical or historical sentence in Chapter 3 must map to this ledger or trigger an explicit ledger update. The final bibliography must be generated from verified publication metadata rather than reconstructed from prose.
