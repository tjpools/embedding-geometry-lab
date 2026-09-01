```text
GRADIENT-DESCENT(3)              Book Two Man Pages             GRADIENT-DESCENT(3)

NAME
       gradient-descent - adjust parameters by a scaled negative gradient

SYNOPSIS
       (w, b) <- (w, b) - eta * grad L(w, b)

DESCRIPTION
       Given a scalar loss over parameters, compute the gradient, scale it by
       a learning rate eta, and subtract it from the parameters. Repeating
       predict -> loss -> gradient -> update forms a training loop. Under a
       small enough eta, loss can decrease at every recorded step for a fixed
       model, data, and objective; under a large enough eta, the same loop can
       diverge while every other component stays fixed.

NOTES
       Reduced training loss is not generalization: no held-out evaluation is
       performed here. Gradient is not update; update is not learning in the
       biological or ordinary-language sense. Direction alone does not
       guarantee a good step size.

       This four-step loop does not change shape when the parameters are a
       Transformer's attention(2) projections, feed-forward(3) weights, and
       embeddings instead of one weight and one bias. What changes is size and
       hardware cost: batched matrix multiplications, tensor(7) contractions,
       and gradient-accumulation buffers replace two scalar partial
       derivatives.

SEE ALSO
       jacobian(3), tensor(7), transformer-block(8)

SOURCE
       Chapter 6, learning-loop probe.
```
