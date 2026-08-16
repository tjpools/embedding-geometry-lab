# Chapter 6 Probe — The Learning Loop

**Status:** Verified August 13, 2026  
**Implementation:** [chapter_06_learning_loop_probe.py](chapter_06_learning_loop_probe.py)  
**Dependencies:** Python standard library only

## Claims Under Test

1. A scalar loss can evaluate one parameterized unit over a declared probability distribution of examples.
2. Analytic gradients can be checked against finite differences.
3. Repeated gradient updates can reduce the declared training loss for a selected learning rate.
4. Gradient information alone does not guarantee improvement for every update size.

## Model, Data, and Loss

The affine unit is

$$
\hat y=wx+b.
$$

The four training examples are equally weighted:

| $x$ | target $y$ | $P(x,y)$ |
|---:|---:|---:|
| $-1$ | $-1$ | $0.25$ |
| $0$ | $1$ | $0.25$ |
| $1$ | $3$ | $0.25$ |
| $2$ | $5$ | $0.25$ |

They follow the declared relation $y=2x+1$. The objective is half the expected squared error under this finite distribution:

$$
L(w,b)=\frac12\sum_i P_i( wx_i+b-y_i)^2.
$$

The probe starts from $w=0$, $b=0$ and computes

$$
\nabla L(0,0)=(-3.5,-2.0).
$$

A central finite-difference check with $h=10^{-6}$ differs from the analytic components by less than $5\times10^{-10}$.

## Update Rule

For learning rate $\eta$, each step applies

$$
(w,b)\leftarrow(w,b)-\eta\nabla L(w,b).
$$

With $\eta=0.2$, the first update moves to $(0.7,0.4)$ and reduces loss from $4.5$ to $1.8375$. Loss decreases at every one of 12 recorded updates, and both parameters move closer to the declared relation $(2,1)$.

With the same model, data, objective, gradient, initialization, and step count but $\eta=1.2$, final loss is approximately $197.5298$, above the initial loss $4.5$. The control case demonstrates that a gradient direction does not make every finite step an improvement.

## Validation Gates

- example probabilities sum to one
- analytic and finite-difference gradients agree within $10^{-6}$
- base-case loss decreases at every recorded step
- base-case parameters move toward $(2,1)$
- control-rate final loss exceeds initial loss
- rerunning the probe produces identical structured output

All gates pass.

## Evidence Boundary

The probe establishes arithmetic and behavior for one affine unit, one finite training distribution, one squared-error objective, one initialization, two learning rates, and 12 steps.

It does not establish:

- performance on unseen data or generalization
- convergence for arbitrary objectives, models, initializations, or learning rates
- that lowest training loss is the best deployed model
- stochastic gradient behavior, minibatching, or noisy estimates
- backpropagation through multiple layers
- automatic differentiation
- biological learning, understanding, intention, or intelligence
- that all parameter adjustment should be called learning outside the declared machine-learning context
