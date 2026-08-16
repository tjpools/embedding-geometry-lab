# Chapter 4 Probe — A Map and Its Local Change

**Status:** Verified August 13, 2026  
**Implementation:** [chapter_04_map_and_local_change_probe.py](chapter_04_map_and_local_change_probe.py)  
**Dependencies:** Python standard library only

## Claims Under Test

1. A declared matrix map preserves vector addition and scalar multiplication.
2. The Jacobian of a declared differentiable map at a declared point predicts first-order change in a declared direction.
3. Central finite differences approach that directional prediction as the step decreases in this case.

## Linear Case

Use

$$
A=\begin{bmatrix}1&0.5\\-0.25&1\end{bmatrix},\quad
u=\begin{bmatrix}1\\2\end{bmatrix},\quad
v=\begin{bmatrix}-1\\1\end{bmatrix},\quad c=3.
$$

The probe verifies

$$
A(u+v)=Au+Av=(1.5,3)
$$

and

$$
A(cu)=cAu=(6,5.25).
$$

These examples check the implementation against the defining linearity relations. They do not prove those relations for every matrix by numerical sampling.

## Local Change Case

Declare

$$
f(x,y)=\left(x+\frac14y^2,\sin x+y\right),
$$

the point $p=(0.6,-0.8)$, and direction $d=(0.3,-0.2)$. The analytic Jacobian is

$$
J_f(x,y)=
\begin{bmatrix}
1 & 0.5y\\
\cos x & 1
\end{bmatrix}.
$$

At $p$,

$$
J_f(p)=
\begin{bmatrix}
1 & -0.4\\
0.8253356149 & 1
\end{bmatrix},
$$

and the predicted directional change is

$$
J_f(p)d=(0.38,0.0476006845).
$$

The central difference

$$
\frac{f(p+hd)-f(p-hd)}{2h}
$$

is evaluated for $h\in\{10^{-1},10^{-2},10^{-3},10^{-4}\}$.

## Observed Result

| $h$ | Euclidean error from $J_f(p)d$ |
|---:|---:|
| $10^{-1}$ | $3.7138\times10^{-5}$ |
| $10^{-2}$ | $3.7140\times10^{-7}$ |
| $10^{-3}$ | $3.7140\times10^{-9}$ |
| $10^{-4}$ | $3.7137\times10^{-11}$ |

The error decreases at every recorded step, and the smallest-step error is below $10^{-9}$.

## Evidence Boundary

The probe verifies its arithmetic, the two sampled linearity identities, the analytic derivative implementation, and finite-difference convergence for one map, point, direction, and step sequence.

It does not establish:

- differentiability of arbitrary functions
- global accuracy of a local linear approximation
- numerical stability for arbitrarily small steps
- a gradient, because the worked output is vector-valued
- an optimization rule, learning process, or neural-network result
- that a person or transformer context-freely “has a Jacobian”
