# Chapter 7: Leibniz, Differentials, and the Local Shape of Meaning

We have already treated embeddings as points in a high-dimensional space and similarity as a geometric relation. That view gave us neighborhoods, directions, clustering, and projection. But geometry becomes much more interesting when we stop asking only *where a point is* and begin asking *how things change near it*.

That is the beginning of calculus.

This chapter introduces the idea of the **differential**—Leibniz’s famous \(dx\)—and shows why it matters for modern representation spaces. The point is not that embedding models secretly contain classical infinitesimals in a literal historical sense. The point is that Leibniz developed a language for reasoning about **local change**, and that language maps surprisingly well onto the way we analyze movement in vector spaces.

When we move a point in an embedding space by a tiny amount, what changes? Which features remain stable? Which directions matter, and which are mostly noise? What does it mean for a transformation to be smooth, singular, linear to first order, or curved only at larger scale?

These are questions of local geometry. Leibniz gave us one of the earliest systematic ways to think about them.

## 7.1 From static points to local behavior

Suppose a word, sentence, image, or user profile is represented by a vector \(x\in\mathbb{R}^n\). In earlier chapters we cared about distances such as

\[
\|x-y\|,
\]

angles such as cosine similarity,

\[
\cos(\theta)=\frac{x\cdot y}{\|x\|\,\|y\|},
\]

and transformations such as projection into lower-dimensional subspaces.

All of that is static geometry. It compares finished positions.

But many real questions are dynamic, even when no time variable appears explicitly. We may ask:

- What happens if we perturb a vector slightly?
- How sensitive is a classifier to a small change in input representation?
- Which semantic directions produce the largest downstream effect?
- When does a local linear approximation describe the system well?

To ask these questions is to move from geometry to **differential geometry in miniature**: not the full machinery of manifolds and tensors, but the basic insight that a space is often best understood by studying how quantities vary under very small displacements.

Leibniz wrote such small displacements as \(dx\), \(dy\), and so on. Today we interpret them in several compatible ways: as differentials, as infinitesimal changes, as linear approximations, or as formal symbols inside derivative notation. What unifies these interpretations is the same idea:

> A differential captures how a quantity changes locally when its input changes by a small amount.

That idea is everywhere in machine learning.

## 7.2 What is a differential?

If \(y=f(x)\), then a small change in \(x\) produces a corresponding change in \(y\). Leibniz wrote this relation suggestively as

\[
dy = f'(x)\,dx.
\]

This is one of the most compact and influential formulas in mathematics.

It says that, to first order, the output change \(dy\) is the derivative \(f'(x)\) times the input change \(dx\). In modern language, the differential is the **best local linear approximation** to the change in the function.

For a scalar function of one variable, this is familiar. If

\[
f(x)=x^2,
\]

then

\[
dy = 2x\,dx.
\]

Near a point \(x\), doubling the current value of \(x\) tells us the local sensitivity of the square function.

If \(x=3\), then a tiny increase \(dx\) produces an approximate output increase

\[
dy \approx 6\,dx.
\]

The square function is not globally linear, but it is locally linear to first order.

That phrase—**locally linear to first order**—is the real content of differentials.

## 7.3 Why Leibniz notation still matters

Newton and Leibniz both invented calculus, but Leibniz’s notation proved especially durable because it makes structural relationships visible. The expression

\[
\frac{dy}{dx}
\]

looks like a ratio, and while one must treat that carefully, the notation encourages us to think in terms of dependence and transformation. It says: *how much does y change relative to x?*

This way of writing derivatives becomes even more powerful in multivariable settings. If a function depends on many coordinates, we can ask how the output responds to each coordinate separately, producing partial derivatives:

\[
\frac{\partial f}{\partial x_1},\quad \frac{\partial f}{\partial x_2},\quad \dots,\quad \frac{\partial f}{\partial x_n}.
\]

These assemble into the gradient

\[
\nabla f(x)=\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right).
\]

Then the differential becomes

\[
df = \nabla f(x)\cdot dx,
\]

where now \(dx\) is itself a small displacement vector.

This is exactly the language we need for embedding geometry.

A point in embedding space is already multivariate. A local move is naturally a vector. A score, probability, loss, or semantic feature can be treated as a function on that space. The differential tells us how that quantity changes under a tiny movement.

## 7.4 Differential thinking in embedding space

Let \(x\in\mathbb{R}^n\) be an embedding, and let

\[
f:\mathbb{R}^n\to\mathbb{R}
\]

measure something we care about. For example, \(f(x)\) might represent:

- the score assigned to a label,
- the strength of a semantic attribute,
- the output logit of a classifier,
- the distance to a prototype,
- or the loss incurred by a downstream task.

If we perturb the embedding by a small vector \(h\), then

\[
f(x+h) \approx f(x) + \nabla f(x)\cdot h.
\]

In Leibniz-style notation, if \(dx=h\), then

\[
df = \nabla f(x)\cdot dx.
\]

This tells us several things immediately.

First, not all directions are equal. If \(dx\) points in a direction aligned with the gradient, the function changes rapidly. If \(dx\) is orthogonal to the gradient, the first-order change is zero.

Second, local behavior is anisotropic. A representation may be very sensitive to movement along one semantic axis and almost insensitive along another.

Third, differential analysis gives us a principled way to separate **signal** from **flatness**. Some nearby moves matter because they correspond to meaningful local directions. Others leave the relevant quantity almost unchanged and therefore behave, at least locally, like semantic null directions.

This is not just abstract mathematics. It is how one analyzes robustness, adversarial perturbations, feature attribution, and local interpretability.

## 7.5 Tangent intuition without full manifold formalism

In advanced geometry, the differential at a point acts on tangent vectors. We do not need the full formal machinery yet, but the intuition is valuable.

Imagine standing at a point in a curved landscape. Globally the landscape may twist, bend, and fold. But if you zoom in enough, the area around your feet looks approximately flat. The directions in which you can step form a tangent plane. The differential tells you the local slope of a function along those directions.

Embedding spaces are usually modeled as Euclidean vector spaces, but many learned representations effectively live near lower-dimensional structures: clusters, sheets, trajectories, or curved semantic strata. Even in a nominally flat ambient space, the data distribution can have local shape.

So when we talk about a small displacement \(dx\), we are often implicitly talking about a move that stays near the meaningful local structure of the data. Some directions are natural continuations of the representation; others shoot away from the data manifold into regions with little interpretive value.

Leibniz did not speak in the language of manifolds as we do now, but his notation prepared mathematics to think locally, relationally, and structurally. That legacy matters here.

## 7.6 The chain rule as compositional geometry

One of the most important consequences of differential notation is the chain rule. If

\[
y=f(u), \qquad u=g(x),
\]

then

\[
\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}.
\]

This looks almost mechanical in Leibniz notation, and that is part of its power. It expresses the fact that local change propagates through composition.

Modern machine learning systems are built from compositions of functions. An input is transformed into tokens, tokens into embeddings, embeddings through layers, layers into logits, logits into probabilities, probabilities into loss. The chain rule tracks how local change flows through the whole system.

Backpropagation is, in a very real sense, a massive organized application of the chain rule.

If a small perturbation \(dx\) at one stage creates a change \(du\), and that change creates a later change \(dy\), then differential notation helps us see how sensitivity accumulates or contracts across the pipeline.

In representation learning, this means that local geometric changes at one layer can be amplified, damped, rotated, or compressed by later transformations. The differential of the composed map captures that behavior.

## 7.7 Jacobians: the multivariable form of local change

So far we have let a vector input produce a scalar output. But often we have a vector-valued transformation

\[
F:\mathbb{R}^n \to \mathbb{R}^m.
\]

This is the natural setting for neural layers and learned feature maps.

The derivative of such a map is the **Jacobian matrix**:

\[
J_F(x)=
\begin{bmatrix}
\frac{\partial F_1}{\partial x_1} & \cdots & \frac{\partial F_1}{\partial x_n}\\
\vdots & \ddots & \vdots\\
\frac{\partial F_m}{\partial x_1} & \cdots & \frac{\partial F_m}{\partial x_n}
\end{bmatrix}.
\]

Then the local change in output is approximated by

\[
dF = J_F(x)\,dx.
\]

This is the multivariable generalization of \(dy=f'(x)dx\).

The Jacobian tells us how tiny motions in input space are transformed into tiny motions in output space. It can stretch some directions, compress others, and mix coordinates together through rotation or shear.

In embedding analysis, the Jacobian is a local microscope. It tells us what the model does *right here*, near this representation, not merely on average over the whole dataset.

Questions such as the following are Jacobian questions in disguise:

- Which local directions get amplified?
- Which local directions collapse?
- Where is the representation map nearly singular?
- Which features are stable under small perturbations?

Whenever we care about local expressivity or fragility, we are already in the world of differentials.

## 7.8 Singular directions and semantic fragility

If the Jacobian has directions with very small singular values, then movement in those input directions barely affects the output to first order. Those are locally compressed directions.

If it has directions with very large singular values, then tiny input changes can cause large output shifts. Those are sensitive or amplified directions.

This gives a geometric vocabulary for understanding representational stability.

A robust semantic feature should often be stable across irrelevant perturbations. That means there are directions in embedding space along which the feature score changes very little. By contrast, a brittle feature may depend strongly on a narrow local direction, making it vulnerable to tiny perturbations.

This is why differential thinking connects naturally to adversarial examples. An adversarial perturbation is often a very small movement in input space engineered to produce a disproportionately large change in output. That is a statement about the local derivative structure of the model.

Leibniz’s \(dx\) was meant to represent an arbitrarily small change. In modern ML, the meaningful question is often: *what kinds of tiny changes matter, and why?*

## 7.9 Differential versus finite difference

It is important to distinguish the differential from an ordinary finite change.

If we move from \(x\) to \(x+h\), the exact change is

\[
\Delta f = f(x+h)-f(x).
\]

The differential, by contrast, is the linear approximation

\[
df = \nabla f(x)\cdot h.
\]

These agree closely when \(h\) is small and the function is smooth. But they are not identical in general. The difference between them reflects curvature and higher-order effects.

This distinction matters in embedding spaces because some transformations are locally linear but globally nonlinear. A semantic direction that works well for tiny edits may fail for larger moves. Local analogies can break down. Neighborhood structure can distort. The first-order approximation is informative, but only within its domain of validity.

So the differential is not a magic substitute for actual movement through the space. It is a disciplined local approximation.

## 7.10 Local linearity and the practical meaning of “smoothness”

When we say a map is smooth, we mean roughly that small changes in input produce controlled changes in output, and that these changes vary in a regular way from point to point. Smoothness is what allows local linear approximations to be useful.

In practice, much of modern representation analysis assumes some degree of smoothness:

- nearest neighbors are expected to remain somewhat stable under tiny perturbations,
- interpolation between nearby points is expected to remain meaningful,
- gradients are expected to say something useful about behavior,
- and optimization is expected to follow local slope information.

If the learned geometry were wildly discontinuous everywhere, these tools would fail.

Of course, actual neural systems are not smooth in every possible sense, and high-dimensional phenomena can be subtle. But the success of gradient-based training and local interpretability methods depends on enough regularity for differential approximations to be informative.

This is another reason Leibniz belongs in the story: he provided the conceptual grammar for describing systems whose local behavior is more tractable than their global form.

## 7.11 A semantic reading of \(dx\)

We can now give \(dx\) a more interpretive reading.

In ordinary calculus, \(dx\) is a small change in the independent variable. In embedding geometry, \(dx\) can be read as a **local semantic displacement**.

That displacement might correspond to:

- a slight shift in tone,
- a modest increase in formality,
- a movement toward a topic,
- a perturbation in sentiment,
- or a change along a latent feature discovered by the model.

Then \(df\) records how a measured property changes under that semantic displacement.

For example, if \(f\) scores “positivity,” then \(df\) tells us how positivity changes under a tiny move. If \(f\) scores “technicality,” then the gradient of \(f\) points in the direction of greatest local increase in technical language.

This perspective makes the differential a bridge between pure geometry and interpretability. It is not merely algebraic notation; it is a language for talking about **which local moves mean what**.

## 7.12 From differentials to tangent features

Suppose that at a point \(x\), several interpretable scalar functions are defined:

\[
f_1(x), f_2(x), \dots, f_k(x).
\]

Each has a gradient, and each gradient identifies a local direction of maximal increase for that feature. Together these gradients define a local system of semantic sensitivities.

You can think of them as forming a first-order semantic atlas around the point.

Some gradients may align, indicating correlated features. Others may be nearly orthogonal, indicating locally independent directions. Some may be small, indicating local flatness. Others may change rapidly from point to point, indicating curvature in the semantic landscape.

This is a deeply Leibnizian way of understanding representation: not by assigning a fixed essence to each point, but by studying the network of local relations among varying quantities.

## 7.13 Why this matters philosophically

Leibniz did not just contribute notation. He also promoted a relational style of thought. Quantities were understood through how they varied together. Structure emerged through dependencies, transformations, and lawful coordination.

That resonates strongly with embedding-based views of meaning.

In an embedding system, the meaning of a point is not usually an isolated intrinsic tag. Meaning comes from position, neighborhood, direction, transformability, and response under measurement. In other words, meaning is partly constituted by relations.

The differential sharpens this relational picture. It asks not only what a point is near, but how measured properties change when we move away from it in different directions. This adds a local dynamical layer to geometric semantics.

So the transition from static embedding geometry to differential embedding geometry mirrors a broader conceptual shift:

- from locations to local transformations,
- from similarity alone to sensitivity,
- from pointwise description to relational variation.

That is one reason Leibniz belongs naturally in this narrative.

## 7.14 Summary

Leibniz’s differential notation gives us a powerful way to describe local change.

For a scalar function,

\[
df = \nabla f(x)\cdot dx,
\]

and for a vector-valued map,

\[
dF = J_F(x)\,dx.
\]

These formulas express the central idea of the chapter:

> Near a point, a smooth transformation is best understood by its first-order action on small displacements.

In embedding spaces, this means:

- local directions matter,
- sensitivity is anisotropic,
- gradients reveal feature increase,
- Jacobians reveal local transformation structure,
- and robustness or fragility can often be framed in differential terms.

Leibniz’s \(dx\) is therefore not a historical curiosity. It is a compact symbol for one of the most useful ideas in modern geometric thinking: that the local behavior of a system can often be captured by how it transforms very small changes.

In the next chapter, we will extend this local viewpoint further by examining curvature: what happens when first-order approximations are not enough, and the geometry of bending begins to matter.
