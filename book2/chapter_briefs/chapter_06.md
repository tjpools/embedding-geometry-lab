# Chapter 6 Brief — Learning by Adjustment

**Status:** Verified; Part II integrated  
**Part:** II — Learning Systems  
**Modules:** `math.optimization`, `ai.neural`  
**Visual anchor:** **The Learning Loop**

## Reader Entry

Part I established probability distributions, matrices, derivatives, typed artifacts, and executable results without claiming that any mechanism learned. The reader may still equate a gradient with learning, assume every gradient step lowers loss, or treat reduced training loss as proof of generalization or intelligence.

## Intended Exit

The reader can distinguish:

- a parameterized model from its current predictions
- training examples from their declared probability weights
- a scalar loss from prediction error on one example
- a gradient from a parameter update
- learning rate from gradient direction
- one update from an iterative training loop
- reduced training loss from generalization
- an affine artificial unit from a biological neuron
- single-unit gradient descent from multilayer backpropagation

## Central Question

What additional machinery turns derivatives and executable computation into a bounded process of parameter adjustment?

## Chapter Claim

Within a declared machine-learning problem, training requires a parameterized model, data distribution, scalar objective, derivative, update rule, step size, and repeated evaluation. Gradient descent can reduce the selected training objective, but improvement remains conditional on the objective, data, model, initialization, and learning rate.

The [verified learning-loop probe](../evidence/chapter_06_learning_loop_probe.md) supports the worked case. The [source ledger](../evidence/chapter_06_sources.md) grounds optimization, neural-training, and historical claims.

## Chapter Result

For one affine unit trained on four equally weighted examples following $y=2x+1$, the analytic initial gradient $(-3.5,-2.0)$ matches finite differences within $5\times10^{-10}$. With learning rate $0.2$, loss decreases from $4.5$ at every one of 12 updates and parameters move toward $(2,1)$. With learning rate $1.2$, final loss rises to approximately $197.53$. The update mechanism is therefore inspectable but not self-guaranteeing.

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.probability` | `math.optimization` | Expected quantities over declared alternatives support the training objective. |
| `math.calculus` | `math.optimization` | Gradients provide local change information for the objective. |
| `math.vectors` | `ai.neural` | Inputs and parameters are numerical objects. |
| `math.matrices` | `ai.neural` | Affine and later layered computations use linear maps. |

**Internal edge:**

| Source | Target | Chapter use |
|---|---|---|
| `math.optimization` | `ai.neural` | A gradient-based update adjusts the unit's weight and bias against a declared loss. |

**Outgoing edge:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `ai.neural` | `ai.sequence` | 9 | Parameterized neural computation becomes the prerequisite for recurrent sequence models. |

## Reader Movement

1. Declare the affine unit $\hat y=wx+b$.
2. Declare four examples and normalized probability weights.
3. Define half expected squared training error.
4. Derive gradients with respect to weight and bias.
5. Check the analytic gradient with finite differences.
6. Apply one learning-rate-scaled update.
7. Repeat for 12 steps and trace loss and parameters.
8. Hold all else fixed and increase only the learning rate.
9. Separate training improvement from convergence and generalization.
10. Place the single-unit case in neural and backpropagation lineage without implementing a deep network.

## Visual Anchor

**The Learning Loop** is one geometric plot containing:

- the base loss trajectory across 12 steps
- parameter positions $(w,b)$ moving toward the declared relation
- a loop labeled `predict → loss → gradient → update`
- a thin control trajectory showing the oversized rate leaving the useful region

**Structural reveal:** learning in the worked system is repeated, objective-directed parameter adjustment; gradient direction and update size jointly determine the observed trajectory.

The control must remain subordinate to the single anchor and all values must derive from the probe.

## Verification Questions

- Do the example probabilities sum to one?
- Is the loss declared before the gradient and update?
- Does the analytic gradient match finite differences?
- Are gradient direction and learning rate kept distinct?
- Is monotonic decrease claimed only for the base trace?
- Is training loss kept distinct from unseen-data performance?
- Is the artificial unit kept distinct from biological neurons?
- Is backpropagation described historically without being claimed as implemented?
- Does the visual derive every plotted point from the probe?

## Explicit Exclusions

This chapter does not implement hidden layers, activation functions, automatic differentiation, stochastic gradient descent, minibatches, regularization, train/test splits, early stopping, backpropagation through a deep network, or deployment evaluation. It does not claim that optimization is understanding or that an artificial neuron is a biological neuron.

## Narrative Transition

Chapter 6 establishes parameter adjustment. Chapter 7 scales matrix operations into tensors and parallel hardware. Chapter 9 later adds recurrence and ordered state, using neural computation as its prerequisite.

## Drafting Gate

Prose began only after the probe, source ledger, and deterministic visual production package passed validation. The completed chapter preserves the brief's claim boundary and has passed probe, visual, link, analytics, and manuscript checks.
