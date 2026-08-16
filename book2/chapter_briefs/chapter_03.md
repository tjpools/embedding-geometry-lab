# Chapter 3 Brief — Reasoning Under Uncertainty

**Status:** Verified; Part I integrated  
**Part:** I — Structures  
**Modules:** `math.probability`, `ai.probabilistic`  
**Visual anchor:** **The Shape of Updated Belief**

## Reader Entry

Chapter 1 separated formal validity from empirical correspondence and operational adequacy. Chapter 2 showed how selected distinctions become numerical representations and how representation policies can preserve or discard information.

The reader may still expect a system to assign one determinate state to every represented situation. The reader may also treat probability as ignorance waiting to be eliminated, evidence as proof, or a posterior probability as a decision.

## Intended Exit

The reader can distinguish:

- an outcome from an event and a hypothesis
- a probability distribution from a single predicted state
- a prior probability from a likelihood
- a likelihood from the probability of a hypothesis
- evidence from the model used to interpret it
- a posterior probability from certainty
- probabilistic inference from a decision rule or action
- a graphical dependency from a claim of physical causation

The reader understands that evidence redistributes probability within a declared model. An update can increase confidence without eliminating uncertainty, and its result remains conditional on the hypotheses, priors, likelihoods, and observations admitted by that model.

## Central Question

How can a system revise quantified uncertainty when evidence arrives without turning the update into certainty?

## Chapter Claim

Probability represents uncertainty over declared possibilities, and Bayesian inference updates that representation by combining a prior distribution with a likelihood model. The posterior is a normalized consequence of those assumptions and the admitted evidence. It is neither a guarantee that the favored hypothesis is true nor, by itself, a rule for action.

The computational portion of this claim is supported by the verified update probe. Its mathematical and historical framing is grounded by [../evidence/chapter_03_sources.md](../evidence/chapter_03_sources.md). Physical correspondence remains outside the toy probe. The visual anchor and production tests are recorded in [../visuals/chapter_03_shape_of_updated_belief.md](../visuals/chapter_03_shape_of_updated_belief.md).

## Chapter Result

Within the declared two-hypothesis model, observing `red` changes the prior distribution $(0.6,0.4)$ to the posterior distribution $(0.8,0.2)$. Changing only the prior produces $(0.64,0.36)$, while changing only one likelihood produces $(5/7,2/7)$. The update therefore remains conditional on the admitted hypotheses, prior, likelihoods, and evidence; it does not select a certain state or prescribe a decision or action.

## Inherited Terms and Claims

From Chapter 1:

- **modeled domain:** the represented objects admitted by a system
- **operation:** a specified transformation or combination over stated objects
- internal validity does not establish empirical correspondence or task adequacy

From Chapter 2, narratively rather than through a direct DAG edge:

- a representation preserves selected distinctions and discards others
- numerical values acquire their computational role through a declared representation system

Chapter 3 introduces **probability distribution**, **prior**, **likelihood**, **evidence**, and **posterior** as distinct objects within a model of uncertainty.

## Dependency Alignment

The chapter contains one internal module edge.

**Incoming edge:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.algebra` | `math.probability` | Declared domains and operations are available before probability measures and update rules are introduced. |

**Internal edge:**

| Source | Target | Chapter use |
|---|---|---|
| `math.probability` | `ai.probabilistic` | Distributions and conditional probability support Bayesian inference and graphical models. |

**Outgoing edges:**

| Source | Target | Destination chapter | Handoff |
|---|---|---:|---|
| `math.probability` | `math.optimization` | 6 | Expected outcomes and uncertainty contribute to objectives that learning systems optimize. |
| `math.probability` | `ai.attention` | 10 | Normalized weighting will later provide mathematical context for attention without making attention identical to Bayesian inference. |

`ai.probabilistic` has no outgoing module edge in the canonical DAG. Its historical and conceptual role remains local to this chapter. Chapter 2 precedes Chapter 3 narratively but supplies no direct module dependency.

## Reader Movement

1. Replace one asserted door state with two explicitly represented hypotheses.
2. Assign a complete prior distribution over those hypotheses.
3. Introduce one observation and a declared likelihood for that observation under each hypothesis.
4. Compute the joint weight of each hypothesis and the observation.
5. Normalize those weights to obtain the posterior distribution.
6. Verify that the posterior sums to one and retains nonzero probability for both hypotheses.
7. Change one likelihood assumption and show that the posterior changes even though the observation does not.
8. Represent the dependency as the directed graph $H \rightarrow E$ while distinguishing modeled dependence from physical causation.
9. Separate the posterior from any threshold, loss function, decision rule, or action that might consume it.
10. Hand probability to later chapters as mathematical machinery for optimization and normalized weighting.

## Worked Update

Use a deliberately small hypothesis space:

$$
H \in \{locked, unlocked\}.
$$

Declare the prior:

$$
P(locked)=0.6, \qquad P(unlocked)=0.4.
$$

For the observation $E=red$, declare:

$$
P(red\mid locked)=0.8, \qquad P(red\mid unlocked)=0.3.
$$

Bayes' rule gives:

$$
P(locked\mid red)
=\frac{P(red\mid locked)P(locked)}
{P(red\mid locked)P(locked)+P(red\mid unlocked)P(unlocked)}
=0.8.
$$

The complementary posterior is:

$$
P(unlocked\mid red)=0.2.
$$

The observation changes the distribution from $(0.6,0.4)$ to $(0.8,0.2)$; it does not establish that the door is locked. The values are fixed probe assumptions, not measured sensor performance or claims about a physical door.

## Evidence Plan

The dependency-free probe is specified and validated in [../evidence/chapter_03_bayesian_update_probe.md](../evidence/chapter_03_bayesian_update_probe.md) and implemented in [../evidence/chapter_03_bayesian_update_probe.py](../evidence/chapter_03_bayesian_update_probe.py). It records:

- the complete hypothesis space
- the normalized prior distribution
- the observed evidence value
- the likelihood of that evidence under every hypothesis
- each unnormalized joint weight
- the evidence probability used as the normalization constant
- the complete posterior distribution
- assertions that the prior and posterior each sum to one
- an assertion that both posterior probabilities remain strictly between zero and one
- an assertion that the selected evidence increases the probability of `locked` without making it certain
- a sensitivity case in which one likelihood changes and the posterior changes

The probe tests arithmetic and dependence on declared assumptions. It does not test whether the likelihoods correspond to a real sensor, whether the hypotheses exhaust a physical situation, or whether acting on the posterior would be adequate.

## Visual Anchor

**The Shape of Updated Belief** is one geometric plot with a shared probability axis and two aligned distributions:

1. the prior mass at `locked` and `unlocked`
2. the declared likelihood of `red` under each hypothesis
3. the posterior mass after normalization

Thin structural lines connect each prior mass through its likelihood weight to its posterior mass. The plot must retain visible mass at both posterior outcomes.

**Structural reveal:** Evidence changes the relative weight of represented hypotheses without converting the favored hypothesis into certainty.

**Caption claim:** Under the declared prior and likelihood model, observing `red` shifts probability toward `locked`; the posterior remains a distribution conditioned on the model and evidence.

**Alternative-text requirement:** State both prior values, both likelihoods, both posterior values, and the fact that neither posterior value is zero or one without relying on color.

## Verification Questions

- Are outcomes, events, hypotheses, and observations consistently distinguished?
- Do the prior and posterior distributions each sum to one?
- Is $P(E\mid H)$ kept distinct from $P(H\mid E)$?
- Are all hypotheses, priors, and likelihoods declared before the update?
- Does the worked result preserve uncertainty rather than equate the largest posterior with certainty?
- Does the sensitivity case expose dependence on model assumptions?
- Is the graphical edge described as conditional dependence rather than automatic proof of causation?
- Is inference kept separate from thresholding, utility, decision, and action?
- Can every historical and technical claim about probabilistic AI be traced to an appropriate source?
- Does the visual remain legible in grayscale and at thumbnail size?

## Explicit Exclusions

This chapter does not:

- claim that uncertainty is always reducible to probability
- claim that the two hypotheses exhaust the states of a physical door
- infer real sensor reliability from illustrative likelihoods
- treat evidence as proof or the posterior as ground truth
- introduce confidence intervals for parameters not estimated by the worked model
- prescribe a threshold, utility function, decision policy, or physical action
- explain matrix transformations, derivatives, or gradients; Chapter 4 owns transformation and change
- explain optimization or parameter learning; Chapter 6 owns learning by adjustment
- treat normalized probabilistic weights as attention; Chapter 10 owns attention
- claim that Bayesian inference resolves meaning, induction, causation, or justification; that philosophical work belongs to Book Three

## Outgoing Handoffs

### To Chapter 6 — Learning by Adjustment

Probability supplies distributions and expected quantities. Chapter 6 combines mathematical objectives with gradients and neural systems to explain parameter adjustment.

### To Chapter 10 — Attention Changes the Path

Probability establishes normalization and weighted alternatives. Chapter 10 introduces attention's learned relevance weights without presenting them as posterior probabilities or Bayesian belief updates.

## Narrative Transition to Chapter 4

Chapter 3 shows how a distribution changes when evidence is admitted. Chapter 4 develops the maps and derivatives needed to describe transformations and local change more generally. This is a narrative transition; the canonical DAG contains no direct edge from either Chapter 3 module to Chapter 4's modules.

## Drafting Gate

Prose begins only after:

- the hypothesis space, prior, evidence, and likelihood model are fixed
- the update probe passes normalization, non-collapse, direction, and sensitivity assertions
- the model assumptions and physical correspondence limits are stated together
- every element of the visual can be derived from the same recorded probe values
- primary or authoritative sources for probability, Bayesian inference, and probabilistic AI are recorded

The source requirement is satisfied by [../evidence/chapter_03_sources.md](../evidence/chapter_03_sources.md), and the visual-production requirement is satisfied by [../visuals/chapter_03_shape_of_updated_belief.md](../visuals/chapter_03_shape_of_updated_belief.md).

## Gate Revalidation

Completed August 12, 2026:

- probe execution and Python compilation pass
- source ledger and local references pass diagnostics
- SVG generation is deterministic from the verified probe
- full-size color, grayscale, and 100-pixel exports pass production checks
- the canonical DAG remains one incoming, one internal, and two outgoing module edges
- framing analytics complete with zero broken local links

The verified manuscript is [../chapters/chapter_03.md](../chapters/chapter_03.md). It preserves the declared assumptions, reproduces the base and sensitivity results, distinguishes graphical dependence from causation, and stops before decision or action. Part I integration remains pending.
