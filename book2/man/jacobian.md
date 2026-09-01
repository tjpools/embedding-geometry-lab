```text
JACOBIAN(3)                      Book Two Man Pages                     JACOBIAN(3)

NAME
       jacobian - local linear approximation of a differentiable map

SYNOPSIS
       J_f(p)[i][j] = d f_i / d x_j, evaluated at point p
       f(p + h*d) ~= f(p) + h * J_f(p) d

DESCRIPTION
       For a differentiable vector-valued map f, the Jacobian collects partial
       derivatives of each output with respect to each input, evaluated at one
       point p. It predicts first-order output change for a small step along a
       direction d. A finite-difference check with decreasing step size h
       supplies an independent numerical verification of the analytic formula.

NOTES
       The approximation is local: valid near p, with error growing as steps
       move away from p. A Jacobian is not a gradient (which belongs to a
       scalar-valued function) and is not an update rule (which requires an
       objective and a step). "Has a Jacobian" is not a trait a person has.

       The matrix-vector product underlying this page recurs, at far greater
       width, in every attention(2) score and feed-forward(3) projection. On
       hardware it decomposes into fused multiply-add operations; the
       locality and linearity distinctions here do not change with scale.

SEE ALSO
       gradient-descent(3), tensor(7), attention(2)

SOURCE
       Chapter 4, map-and-local-change probe.
```
