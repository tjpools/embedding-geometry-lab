\newpage
\vspace*{3cm}
# Chapter 7: Leibniz, Differentials, and the Local Shape of Meaning
## Crossing Over: From Machine to Mathematics

Chapter 6 kept us close to the discrete machine: instructions, registers, stack discipline, and execution. This chapter crosses into a different but necessary language: the language for talking about change itself. If assembly showed how computation runs, calculus begins to show how structured variation can be described.

There are moments in the history of mathematics when the existing tools simply stop working. Not because the problems become harder in a familiar way, but because the world reveals a kind of structure the old grammar cannot express.

Consider the equation

$$
5^x + x = 49
$$

It looks innocent, almost playful, but it marks a boundary. Algebra can manipulate it, rearrange its pieces, and approximate its solution numerically, but it cannot solve it by the ordinary symbolic methods that earlier equations seemed to reward. The equation is a door, and on the other side is a different ontology.

This is not the kind of problem rescued by adjoining one more symbol to an otherwise intact algebraic world. It is the kind of problem that reveals the need for a different representational grammar.

This chapter is not about solving that equation. It is about the invention of a new kind of object: Leibniz's $dx$. Leibniz, the inventor of the symbolic grammar of calculus, did not merely introduce a symbol. He introduced a new species of mathematical being: something smaller than any ordinary quantity, yet not simply zero; something that behaves like a number in calculation, yet becomes difficult to pin down when examined too closely. The infinitesimal is the hinge between two eras: the algebraic world, where equations are rearranged until they yield, and the analytic world, where equations are approached through local behavior rather than mastered in a single symbolic stroke.

To understand Lambert's later triumphs, the modern idea of a function as a geometric object, or the full power of calculus itself, we first have to understand what $dx$ is supposed to be and why Berkeley thought it involved metaphysical sleight of hand. The mathematics becomes more powerful here because the ontology changes. The world becomes continuous, and continuity demands a new grammar.

The cast of this chapter comes from the seventeenth and eighteenth centuries, but you do not need their biographies. You only need their roles: Newton is the geometric and physical imagination behind calculus; Leibniz is the symbolic architect of its language; Berkeley is the philosopher who asks what infinitesimals really are; Lambert is the mathematician who shows what the new grammar can actually do.

Think of this era not as background history, but as the moment mathematics changed its operating system.

For readers coming from AI more than calculus, the key idea can be stated very simply before the history gets denser: some systems cannot be understood all at once, but they can be understood locally, by watching how small changes behave nearby. Leibniz's $dx$ is one of the great tools for making that local behavior thinkable.

You do not need to master every historical detail in this chapter to keep the main thread. What matters most is this:

- algebra looks for exact symbolic closure
- calculus asks how change behaves locally
- that shift from exact answer to local behavior is one of the bridges from classical mathematics to modern AI

Before embeddings became a story about local perturbations, calculus first had to become a story about lawful change. That shift did not happen all at once. It emerged from a tension within equation space itself.


Before we can appreciate what Leibniz invented, we need to feel the failure of the old tools. Try the algebraic moves you already know: subtract $x$ from both sides, take logarithms, isolate the variable, rearrange the terms. Every move leads to a dead end. The variable is trapped in two incompatible worlds: $x$ lives in the linear world, while $5^x$ lives in the exponential one. Algebra can handle either world separately, but not both at once.

This is the moment where mathematics needed a new idea: not a trick, not a clever rearrangement, but a new way to reason when exact symbolic closure fails. The later story of the quintic sharpened that same point. Algebra could still classify, transform, and illuminate structure, but it could not always deliver a closed symbolic answer. Differential thinking mattered because it changed the question. When global solvability is unavailable, mathematics can still ask:

- How does an expression behave nearby?
- If a variable changes slightly, what happens to the result?
- If we cannot solve globally in one stroke, can we reason locally and move step by step?

This chapter introduces the idea of the **differential**—Leibniz’s famous $dx$—and shows why it matters for modern representation spaces. The point is not that embedding models secretly contain classical infinitesimals in a literal historical sense. The point is that Leibniz developed a language for reasoning about **local change**, and that language maps surprisingly well onto the way we analyze movement in vector spaces.

But to understand why Leibniz matters here, we need to understand not only the utility of differentials, but also the controversy around them. Leibniz invented the grammar of infinitesimals. Berkeley demanded metaphysical clarity about what those infinitesimals were. Lambert later showed how far the new grammar could reach once mathematics accepted its conceptual cost. In modern notation, that legacy appears in the Lambert $W$ function, defined implicitly by

$$
W(z)e^{W(z)} = z,
$$

which packages a whole class of exponential entanglements into a new mathematical object. The point is not that Leibniz or Lambert magically made every stubborn equation yield. The point is that the new language changed what counted as a solvable problem.

## 7.1 From algebraic space to differential space

The transition from algebra to calculus is not merely the addition of new notation. It is a conceptual shift.

In an **algebraic space**, we study fixed expressions and relations among them. We ask whether forms are equivalent, whether variables can be isolated, whether roots can be expressed, and whether a structure can be symbolically resolved.

In a **differential space**, by contrast, we ask how quantities vary. We care about tendencies, slopes, local dependencies, and infinitesimal displacements. The object of understanding is no longer only the static equation, but the behavior of a quantity under change.

This is one reason differential language matters so much. Its power does not come from sharing the same symbolic code as ordinary algebra. Its power comes from encoding a new invariant: the best local account of change available to the tool.

This is a major transition in mathematical thought:

- from solved form to local behavior,
- from exact symbolic closure to controlled approximation,
- from static relation to lawful variation.

That shift is essential for embeddings too. Earlier chapters treated embeddings as points in a high-dimensional space and similarity as a geometric relation. That gave us neighborhoods, directions, clustering, and projection. But geometry becomes much more interesting when we stop asking only *where a point is* and begin asking *how things change near it*.

That is the beginning of calculus.

## 7.2 Newton, Leibniz, and two imaginations of calculus

Newton and Leibniz both developed calculus, but they imagined its foundations differently. Newton imagined calculus through motion; Leibniz imagined it through symbols. Newton was the geometric and physical imagination behind the subject; Leibniz was the symbolic architect who made its operations writable.

Newton’s picture was still deeply geometric and kinematic. His quantities flowed. Magnitudes changed over time. His fluxions arose from motion, variation, and geometric generation. Even when symbolic, the underlying imagination was dynamic and geometric.

Leibniz’s picture was more algebraic, symbolic, and relational. He wrote $dx$, $dy$, and $dy/dx$ in a way that made change look manipulable. His notation did not merely record motion; it made local dependence visible inside symbolic form. It suggested that changes themselves could participate in calculation.

This matters for our purposes. Embedding spaces are usually handled as algebraic objects inside vector spaces: vectors, maps, gradients, Jacobians, projections, norms. In that sense, Leibniz’s formalism fits naturally. His notation helps us reason about how one quantity varies with another inside a symbolic and structural setting.

Leibniz was also a master of language structure. His genius was not only mathematical but linguistic. The symbol $dx$ did not succeed merely because it named a tiny quantity. It succeeded because it gave mathematics a compact formal interface for local complexity. It made variation writable, combinable, and manipulable before every foundational question had been resolved.

So while Newton and Leibniz are both founders of calculus, Leibniz belongs especially well in the story of embeddings because his language of differentials is better suited to a world of symbolic relations among coordinates, features, and transformations.

## 7.3 Berkeley’s challenge: what is $dx$, really?

The power of Leibniz’s notation came with a philosophical problem: what exactly is $dx$? Is it a genuine quantity, an infinitesimal magnitude, a convenient fiction, a limit in disguise, or a formal symbol that works operationally even if its ontology is unclear?

George Berkeley, the philosopher who demanded to know what infinitesimals are, famously challenged the early calculus on precisely this point. His objection was not that calculus failed in practice. It worked remarkably well. His objection was that its foundational language seemed unstable. Infinitesimals appeared to be treated first as if they were nonzero quantities—so that one could divide by them—and then as if they were zero or negligible quantities—so that one could discard them.

Berkeley's critique was not theological so much as ontological. What is $dx$? Is it something or nothing? If it is something, then it must have some magnitude, but that magnitude seems impossible to specify. If it is nothing, then dividing by it should be illegitimate, yet calculus proceeds by doing exactly that. The price of the infinitesimal is that mathematics begins to manipulate entities that do not exist in the ordinary finite sense.

That, for Berkeley, was not conceptual rigor. It was a kind of sanctioned ambiguity. His famous phrase for infinitesimals was that they were the **ghosts of departed quantities**.

Berkeley was right to press the issue. The early success of calculus outran the clarity of its foundations. Mathematicians trusted the method before they fully settled what kind of thing a differential was.

That trust was not blind faith, but it was still a form of methodological confidence prior to ontological resolution. The methods worked. They produced coherent results, strong predictions, and extraordinary explanatory reach. But the exact status of $dx$ remained contested.

This matters for our chapter because it reveals something important: differential reasoning became powerful before its foundations became fully clean.

One way to understand this is to think about approximation as a general strategy of intelligence. Most human thought is top-down before it is foundational. The brain is not built to derive every conclusion from first principles; it is a sparse, survival-oriented system for bringing overwhelming complexity under practical control.

Modern computation does something similar. Floating-point arithmetic on an x86-64 processor does not deliver perfect mathematical exactness in every operation. Instead, the machine uses a highly structured approximation regime that makes large computational systems tractable, stable, and composable. The user works through the abstraction; the machinery underneath manages the complexity.

Leibniz’s $dx$ can be understood in a similar spirit. It was a way of bringing complexity under symbolic control. Its power came not from immediate ontological transparency, but from the fact that it let mathematics operate coherently on local change. In that sense, $dx$ is less a mysterious tiny object than a language abstraction for handling variation below the scale of ordinary finite reasoning.

Modern machine learning often works the same way: its abstractions can be operationally powerful before their ontology is fully settled.

We speak of semantic directions, latent axes, feature gradients, and manifold structure. These concepts are often useful before their ontology is fully settled. Berkeley’s challenge therefore has a contemporary echo:

- What exactly is a semantic direction?
- What exactly counts as a local move in representation space?
- When we write $dx$, are we naming a real object, a limit process, a computational approximation, or a formal shorthand?

Those questions do not invalidate the method. But they remind us to distinguish practical success from foundational clarity.

## 7.4 What is a differential?

If $y=f(x)$, then a small change in $x$ produces a corresponding change in $y$. Leibniz wrote this relation suggestively as

$$
dy = f'(x)\,dx.
$$

This is one of the most compact and influential formulas in mathematics.

It says that, to first order, the output change $dy$ is the derivative $f'(x)$ times the input change $dx$. In modern language, the differential is the **best local linear approximation** to the change in the function.

For a scalar function of one variable, this is familiar. If

$$
f(x)=x^2,
$$

then

$$
dy = 2x\,dx.
$$

Near a point $x$, doubling the current value of $x$ tells us the local sensitivity of the square function.

If $x=3$, then a tiny increase $dx$ produces an approximate output increase

$$
dy \approx 6\,dx.
$$

The square function is not globally linear, but it is locally linear to first order.

That phrase—**locally linear to first order**—is the real content of differentials.

## 7.5 Why Leibniz notation still matters

Leibniz’s notation proved especially durable because it makes structural relationships visible. The expression

$$
\frac{dy}{dx}
$$
 

looks like a ratio, and while one must treat that carefully, the notation encourages us to think in terms of dependence and transformation. It says: *how much does $y$ change relative to $x$?*

This way of writing derivatives becomes even more powerful in multivariable settings. If a function depends on many coordinates, we can ask how the output responds to each coordinate separately, producing partial derivatives:

$$
\frac{\partial f}{\partial x_1},\quad \frac{\partial f}{\partial x_2},\quad \dots,\quad \frac{\partial f}{\partial x_n}.
$$ 

These assemble into the gradient

$$
\nabla f(x)=\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)
$$

Then the differential becomes

$$
df = \nabla f(x)\cdot dx,
$$

where now $dx$ is itself a small displacement vector.

This is exactly the language we need for embedding geometry.

A point in embedding space is already multivariate. A local move is naturally a vector. A score, probability, loss, or semantic feature can be treated as a function on that space. The differential tells us how that quantity changes under a tiny movement.

## 7.6 Differential thinking in embedding space

Let $x \in \mathbb{R}^n$ be an embedding, and let $f:\mathbb{R}^n\to\mathbb{R}$
measure something we care about. For example, $f(x)$ might represent:

- the score assigned to a label,
- the strength of a semantic attribute,
- the output logit of a classifier,
- the distance to a prototype,
- or the loss incurred by a downstream task.

If we perturb the embedding by a small vector $h$, then

$$
f(x+h) \approx f(x) + \nabla f(x)\cdot h.
$$ 

In Leibniz-style notation, if $dx=h$, then

$$ 
df = \nabla f(x)\cdot dx.
$$ 

This tells us several things immediately.

First, not all directions are equal. If $dx$ points in a direction aligned with the gradient, the function changes rapidly. If $dx$ is orthogonal to the gradient, the first-order change is zero.

Second, local behavior is anisotropic. A representation may be very sensitive to movement along one semantic axis and almost insensitive along another.

Third, differential analysis gives us a principled way to separate **signal** from **flatness**. Some nearby moves matter because they correspond to meaningful local directions. Others leave the relevant quantity almost unchanged and therefore behave, at least locally, like semantic null directions.

This is not just abstract mathematics. It is how one analyzes robustness, adversarial perturbations, feature attribution, and local interpretability.

## 7.7 Tangent intuition without full manifold formalism

In advanced geometry, the differential at a point acts on tangent vectors. We do not need the full formal machinery yet, but the intuition is valuable.

Imagine standing at a point in a curved landscape. Globally the landscape may twist, bend, and fold. But if you zoom in enough, the area around your feet looks approximately flat. The directions in which you can step form a tangent plane. The differential tells you the local slope of a function along those directions.

Embedding spaces are usually modeled as Euclidean vector spaces, but many learned representations effectively live near lower-dimensional structures: clusters, sheets, trajectories, or curved semantic strata. Even in a nominally flat ambient space, the data distribution can have local shape.

So when we talk about a small displacement $dx$, we are often implicitly talking about a move that stays near the meaningful local structure of the data. Some directions are natural continuations of the representation; others shoot away from the data manifold into regions with little interpretive value.

Leibniz did not speak in the language of manifolds as we do now, but his notation prepared mathematics to think locally, relationally, and structurally. That legacy matters here.

## 7.8 The chain rule as compositional geometry

One of the most important consequences of differential notation is the chain rule. If

$$
y=f(u), \qquad u=g(x),
$$ 

then

$$ 
\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}.
$$ 

This looks almost mechanical in Leibniz notation, and that is part of its power. It expresses the fact that local change propagates through composition.

Modern machine learning systems are built from compositions of functions. An input is transformed into tokens, tokens into embeddings, embeddings through layers, layers into logits, logits into probabilities, probabilities into loss. The chain rule tracks how local change flows through the whole system.

Backpropagation is, in a very real sense, a massive organized application of the chain rule.

If a small perturbation $dx$ at one stage creates a change $du$, and that change creates a later change $dy$, then differential notation helps us see how sensitivity accumulates or contracts across the pipeline.

In representation learning, this means that local geometric changes at one layer can be amplified, damped, rotated, or compressed by later transformations. The differential of the composed map captures that behavior.

## 7.9 Jacobians: the multivariable form of local change

So far we have let a vector input produce a scalar output. But often we have a vector-valued transformation

$$ 
F:\mathbb{R}^n \to \mathbb{R}^m.
$$ 

This is the natural setting for neural layers and learned feature maps.

The derivative of such a map is the **Jacobian matrix**:

$$ 
J_F(x)=
\begin{bmatrix}
\frac{\partial F_1}{\partial x_1} & \cdots & \frac{\partial F_1}{\partial x_n}\\
\vdots & \ddots & \vdots\\
\frac{\partial F_m}{\partial x_1} & \cdots & \frac{\partial F_m}{\partial x_n}
\end{bmatrix}
$$

Then the local change in output is approximated by

$$
dF = J_F(x)\,dx.
$$

This is the multivariable generalization of $dy=f'(x)dx$.

The Jacobian tells us how tiny motions in input space are transformed into tiny motions in output space. It can stretch some directions, compress others, and mix coordinates together through rotation or shear.

In embedding analysis, the Jacobian is a local microscope. It tells us what the model does *right here*, near this representation, not merely on average over the whole dataset.

Questions such as the following are Jacobian questions in disguise:

- Which local directions get amplified?
- Which local directions collapse?
- Where is the representation map nearly singular?
- Which features are stable under small perturbations?

Whenever we care about local expressivity or fragility, we are already in the world of differentials.

## 7.10 Singular directions and semantic fragility

If the Jacobian has directions with very small singular values, then movement in those input directions barely affects the output to first order. Those are locally compressed directions.

If it has directions with very large singular values, then tiny input changes can cause large output shifts. Those are sensitive or amplified directions.

This gives a geometric vocabulary for understanding representational stability.

A robust semantic feature should often be stable across irrelevant perturbations. That means there are directions in embedding space along which the feature score changes very little. By contrast, a brittle feature may depend strongly on a narrow local direction, making it vulnerable to tiny perturbations.

This is why differential thinking connects naturally to adversarial examples. An adversarial perturbation is often a very small movement in input space engineered to produce a disproportionately large change in output. That is a statement about the local derivative structure of the model.

Leibniz’s $dx$ was meant to represent an arbitrarily small change. In modern ML, the meaningful question is often: *what kinds of tiny changes matter, and why?*

## 7.11 Differential versus finite difference

It is important to distinguish the differential from an ordinary finite change.

If we move from $x$ to $x+h$, the exact change is

$$ 
\Delta f = f(x+h)-f(x).
$$ 

The differential, by contrast, is the linear approximation

$$
df = \nabla f(x)\cdot h.
$$ 

These agree closely when $h$ is small and the function is smooth. But they are not identical in general. The difference between them reflects curvature and higher-order effects.

This distinction matters in embedding spaces because some transformations are locally linear but globally nonlinear. A semantic direction that works well for tiny edits may fail for larger moves. Local analogies can break down. Neighborhood structure can distort. The first-order approximation is informative, but only within its domain of validity.

So the differential is not a magic substitute for actual movement through the space. It is a disciplined local approximation.

## 7.12 Local linearity and the practical meaning of “smoothness”

When we say a map is smooth, we mean roughly that small changes in input produce controlled changes in output, and that these changes vary in a regular way from point to point. Smoothness is what allows local linear approximations to be useful.

In practice, much of modern representation analysis assumes some degree of smoothness:

- nearest neighbors are expected to remain somewhat stable under tiny perturbations,
- interpolation between nearby points is expected to remain meaningful,
- gradients are expected to say something useful about behavior,
- and optimization is expected to follow local slope information.

If the learned geometry were wildly discontinuous everywhere, these tools would fail.

Of course, actual neural systems are not smooth in every possible sense, and high-dimensional phenomena can be subtle. But the success of gradient-based training and local interpretability methods depends on enough regularity for differential approximations to be informative.

This is another reason Leibniz belongs in the story: he provided the conceptual grammar for describing systems whose local behavior is more tractable than their global form.

## 7.13 A semantic reading of $dx$

We can now give $dx$ a more interpretive reading.

In ordinary calculus, $dx$ is a small change in the independent variable. In embedding geometry, $dx$ can be read as a **local semantic displacement**.

That displacement might correspond to:

- a slight shift in tone,
- a modest increase in formality,
- a movement toward a topic,
- a perturbation in sentiment,
- or a change along a latent feature discovered by the model.

Then $df$ records how a measured property changes under that semantic displacement.

For example, if $f$ scores “positivity,” then $df$ tells us how positivity changes under a tiny move. If $f$ scores “technicality,” then the gradient of $f$ points in the direction of greatest local increase in technical language.

This perspective makes the differential a bridge between pure geometry and interpretability. It is not merely algebraic notation; it is a language for talking about **which local moves mean what**.

## 7.14 From differentials to tangent features

Suppose that at a point $x$, several interpretable scalar functions are defined:

$$ 
f_1(x), f_2(x), \dots, f_k(x).
$$

Each has a gradient, and each gradient identifies a local direction of maximal increase for that feature. Together these gradients define a local system of semantic sensitivities.

You can think of them as forming a first-order semantic atlas around the point.

Some gradients may align, indicating correlated features. Others may be nearly orthogonal, indicating locally independent directions. Some may be small, indicating local flatness. Others may change rapidly from point to point, indicating curvature in the semantic landscape.

This is a deeply Leibnizian way of understanding representation: not by assigning a fixed essence to each point, but by studying the network of local relations among varying quantities.

## 7.15 Why this matters philosophically

Leibniz did not just contribute notation. He also promoted a relational style of thought. Quantities were understood through how they varied together. Structure emerged through dependencies, transformations, and lawful coordination.

That resonates strongly with embedding-based views of meaning.

In an embedding system, the meaning of a point is not usually an isolated intrinsic tag. Meaning comes from position, neighborhood, direction, transformability, and response under measurement. In other words, meaning is partly constituted by relations.

The differential sharpens this relational picture. It asks not only what a point is near, but how measured properties change when we move away from it in different directions. This adds a local dynamical layer to geometric semantics.

So the transition from static embedding geometry to differential embedding geometry mirrors a broader conceptual shift:

- from locations to local transformations,
- from similarity alone to sensitivity,
- from pointwise description to relational variation.

That is one reason Leibniz belongs naturally in this narrative.

## 7.16 Summary

Leibniz’s differential notation gives us a powerful way to describe local change.

For a scalar function,

$$ 
df = \nabla f(x)\cdot dx,
$$ 

and for a vector-valued map,

$$
dF = J_F(x)\,dx.
$$

These formulas express the central idea of the chapter:

> Near a point, a smooth transformation is best understood by its first-order action on small displacements.

In embedding spaces, this means:

- local directions matter,
- sensitivity is anisotropic,
- gradients reveal feature increase,
- Jacobians reveal local transformation structure,
- and robustness or fragility can often be framed in differential terms.

But the deeper lesson is historical as well as mathematical. Differential reasoning emerged when algebraic solvability reached its limits and mathematics needed a new way to make sense of difficult problems. Leibniz provided that language in symbolic form. Berkeley exposed the metaphysical bill attached to its early use. Lambert later showed how far that new grammar could reach in problems that algebra could not touch. Newton grounded a related vision in geometry and motion. Out of that tension emerged one of the most powerful ideas in mathematics: that local behavior can be studied lawfully even when global closed-form mastery is unavailable.

That is why $dx$ matters here. It is not just a technical mark on the page. It is the sign of a new mode of thought: one that trades absolute symbolic closure for local intelligibility, and one that still shapes how we reason about modern representation spaces.

In the next chapter, we will extend this local viewpoint further by examining curvature: what happens when first-order approximations are not enough, and the geometry of bending begins to matter.
