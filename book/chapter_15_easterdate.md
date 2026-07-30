# Chapter 15: Runtime Revealed — EasterDate and TokenQuine

Chapter 14 argued that proper analysis must be structural, geometric, and walkable. Chapter 15 lowers that demand into runtime. It takes the reader from analysis as method to analysis as executable practice.

Two public repositories help carry that work: EasterDate and TokenQuine. They sit at opposite ends of the transformer's world, and together they reveal the programming form of this book.

EasterDate belongs to the deterministic end. It turns computus into a stack-driven state machine. Registers, calling conventions, arithmetic partitions, and output formatting all remain explicit. It reveals what runtime looks like when intent has been compressed into a classical executable machine.

TokenQuine belongs to the reflective end. It takes text, files, conversations, and tokenizers, places them into a layered pipeline, and turns representational cost into something inspectable. Where EasterDate reveals runtime through registers and stack frames, TokenQuine reveals runtime through canonicalization, tokenization, comparison, summarization, and projection. One shows how a deterministic machine preserves intent. The other shows how a transformer-facing tool exposes the cost and structure of representation itself.

Taken together, these are not just projects adjacent to the book. They are the book in programming form. They show the confluence of human formation and machine execution building behavior on a computer. One begins close to the metal. The other begins close to the token. One is assembly lawfulness. The other is semantic observability. Between them lies the same claim the book has been making throughout: structure becomes legible when runtime is revealed rather than hidden.

It is important to say at the outset what kind of example this is. EasterDate is not being offered as if it were itself an AI system, and TokenQuine is not being offered as if it were itself a foundation model. They are being offered as runtime apprenticeships in analysis: bounded objects through which the reader can learn what it means to follow transforms, preserve invariants, compare representations, and keep machinery visible. The claim is not that a calendrical algorithm and a token observability tool are the same thing. The claim is that deep understanding of either requires the same discipline of walking the structure rather than stopping at the glyph. What Chapter 14 named abstractly, this chapter now renders concrete across notation, code, register state, tokens, and output.

This is also the first complete runnable instance of the book's architecture. Human reasoning frames the problem, chooses the representation, and judges the result. The classical machine executes deterministically, preserves invariants, and closes the loop under hardware and ABI constraint. The transformer-facing analytic tool traverses the semantic field, compresses the search space, and helps reason across representations. EasterDate and TokenQuine are the first bounded objects in this book where the coupled instrument leaves behind public, runnable proof.

EasterDate was never just a program. TokenQuine is not just a utility. Together they are runtime revealed: two walkable structures that show why this book had to exist.

EasterDate was our historical apprenticeship. We did not merely compute a date. We re-enacted a lineage: ancient astronomy, ecclesiastical calendrics, Gauss's modular arithmetic, twentieth-century calling conventions, and a twenty-first-century x64 toolchain all gathered into one executable artifact. TokenQuine is the matching apprenticeship on the transformer side: canonical text, tokenizer disagreement, representational cost, and self-inspection gathered into one layered instrument. In that sense, the two repositories are a compressed history lesson that runs on silicon from opposite directions.

[View the EasterDate source and structure on GitHub.](https://github.com/tjpools/EasterDate/)

[View the TokenQuine source and structure on GitHub.](https://github.com/tjpools/tokenQuine)

These repositories are part of the chapter's evidence. The book gives the reader the path in prose; the repositories give the reader the executable structure, notes, and artifacts that make the path inspectable in public.

As an ebook, this chapter can therefore do something a print chapter cannot: it can leave the reader a direct path outward. A reader who wants only the argument may stay in the prose. A reader who wants inspection, source, and executable detail can follow the link into the repository and continue the apprenticeship there.

This is not just code to be read, but runtime to be entered: a first invitation to see systems as layered, navigable spaces.

EasterDate is the moment intent became mechanism, and mechanism preserved intent. TokenQuine is the moment representation became inspectable, and inspection preserved meaning. Together they show that computation is not a machine activity alone but a coupled traversal of structure. The computer runs; the human enters; the runtime becomes visible.

## 15.1 Two Runtime Geometries

The contrast between these repositories is the point.

EasterDate reveals a runtime of explicit state transitions. Input year enters a calling convention. Arithmetic decomposes into quotient and remainder work. Registers preserve intermediate coordinates. Stack frames stabilize function boundaries. Output emerges only when the machine has lawfully carried the structure through every transition.

TokenQuine reveals a runtime of explicit representational layers. Input text enters a canonical embedding stage. Tokenizers impose alternative segmentations. Comparative routines expose disagreement. Summary stages derive metrics, heuristics, and cost-oriented views. Projection stages render the result as text, JSON, or Markdown. Output emerges only when the layered pipeline has lawfully carried the structure through every stage.

These are opposite runtime geometries. EasterDate lives near the deterministic machine. TokenQuine lives near the transformer-facing representation layer. But the opposition is exactly what makes them belong together. Both are public proofs that structure can be made walkable. Both make runtime visible rather than hiding it behind an answer.

## 15.2 The Question: “What is the date of Easter?”

The question appears simple. But historically, it was never just a matter of retrieval. In the late 16th century, Pope Gregory XIII was deeply concerned with the slippage of the Easter celebration—how the date, once tied to the spring equinox and lunar cycle, had drifted out of sync with the intended astronomical and ecclesiastical markers. The Gregorian reform was not just a calendar correction; it was a demand for a rule that would hardcode the date of Easter based on explicit, repeatable criteria. The result was a centuries-long tradition of *computus*: the lawful, algorithmic determination of Easter through a structured interplay of calendar, lunar cycle, and ecclesiastical rule. The moment the question is asked computationally, it changes shape:

For readers new to the term, computus simply means the method for calculating the date of Easter.

- What structure determines the date?
- What algorithm expresses that structure?
- What representation makes the algorithm executable?
- What environment makes the representation meaningful?

EasterDate was the first time I walked through that doorway and found a world on the other side.

## 15.3 EasterDate as a Computational Object

To stabilize the argument, EasterDate needs a precise definition. It is not a timestamp waiting to be looked up. It is a rule-generated object. For a given year $Y$, under calendar system $S$ and computus procedure $C$, EasterDate$(Y, S, C)$ is the date produced by applying that lawful structure to that year. The surface is simple; the object is not.

In plain language: Easter is not being fetched from a table here. It is being produced by a rule.

It carries several domains at once:

- mathematics, because the result depends on modular arithmetic, periodicity, and partition
- astronomy, because the rule tracks an ecclesiastical approximation to solar and lunar cycles
- history, because calendar reform and church authority constrain the acceptable result
- practical human life, because the output coordinates ritual, planning, and civil time
- machine execution, because the procedure only became fully legible in this project when written as explicit operations over registers, memory, and calling conventions

That layering is exactly why EasterDate belongs in this book. It is an aggregate object: one thing whose meaning is distributed across several coordinate systems at once.

Representation matters as much as definition. EasterDate can be represented as a month-day pair, an ordinal date, a symbolic record, or a sequence of intermediate values flowing through a program. In our work, the last form mattered most. The date was not merely the answer at the end. It was the terminus of a walk through structured intermediates. Each scratch value, each register choice, and each implementation note became part of the representation layer that made the object intelligible.

This is also why the repository structure mattered. The directory tree was not a neutral container for files. It was scaffolding for thought. It separated algorithm from implementation, implementation from inspection, and inspection from historical reflection. It let EasterDate become something larger than a solved exercise: a walkable object whose lineage, machinery, and meaning could remain visible at the same time. The public repository preserves that scaffolding so the reader can verify that the structure is not being merely described after the fact.

## 15.4 Lookup Table or Algorithm

A lookup table gives answers. An algorithm gives structure. Gauss’s Easter algorithm is not a list of dates. It is a compressed geometry of lunar cycle, solar calendar, and ecclesiastical rule. It does not store the answer in advance. It produces the answer by lawful transformation.

To implement such a procedure is to discover that the algorithm is not merely a recipe. It is a space, and the computation is a path through that space. This is the moment when a program stops being a tool and becomes a world.

The distinction matters. A table preserves outcomes; an algorithm preserves relations. EasterDate is not trivia. It is the prototype of modern algorithmic reasoning.

## 15.5 The Algorithm (Explicit and Walkable)

The heart of EasterDate is Gauss’s algorithm. Here is the walkable sequence of operations:

Given a year $Y$:

	a = Y mod 19
	b = Y div 100
	c = Y mod 100
	d = b div 4
	e = b mod 4
	f = (b + 8) div 25
	g = (b - f + 1) div 3
	h = (19a + b - d - g + 15) mod 30
	i = c div 4
	k = c mod 4
	l = (32 + 2e + 2i - h - k) mod 7
	m = (a + 11h + 22l) div 451
	month = (h + l - 7m + 114) div 31
	day = ((h + l - 7m + 114) mod 31) + 1

Two plain-language notes help here: `mod` means "the remainder after division," and `div` means "whole-number division, discarding any remainder."

Each line is a projection from one coordinate system to another: mod → circular coordinate, div → partition, +/− → drift, month/day → semantic glyph. This is the manifold. These are the coordinate transforms. This is the walk.

Or more simply: each line takes the year, extracts one useful fact from it, and passes that fact to the next step.

## 15.6 The Coding Strategy: Assembly and C++

This is the hinge where the mathematical manifold becomes a machine manifold. The values $a$ through $m$ are no longer only algebraic intermediates. They become coordinates that must survive translation into a calling convention, a register discipline, and an execution model.

In the Windows x64 calling convention, the input year arrives in `RCX`. That fact already shapes the geometry of the implementation. Division on x64 also has its own discipline: `div` treats `RDX:RAX` as a combined dividend, places the quotient in `RAX`, and the remainder in `RDX`. That means the assembly walk is not just “doing the math.” It is preserving the invariants of the machine while the math passes through it.

The coding strategy therefore had to answer four practical questions at once:

- which values need stable homes across later steps
- when `RAX` and `RDX` can be safely reused for quotient and remainder work
- which scratch registers can hold long-lived coordinates such as `a`, `b`, `c`, `h`, `l`, and `m`
- how the return convention should expose the final semantic glyph as month and day

The result is a register choreography. The algorithm stays the same, but each intermediate value is given a machine location, and each arithmetic step is forced to respect both Gauss and the ABI.

### Assembly (Register Choreography)

One useful way to read the assembly is as a map of invariants:

- `RCX` carries the input year into the function
- `RAX` is the active arithmetic workspace
- `RDX` is the compulsory partner register for division and remainder
- `R9`, `R10`, `R11`, and related scratch registers hold intermediate coordinates that must survive future steps
- the final month and day are returned in agreed machine-visible locations rather than left as private internal state

This is the point where the abstract sequence becomes walkable as code. `a = Y mod 19` is not only a mathematical statement. It is a machine event: clear `RDX`, move `Y` into `RAX`, divide by `19`, preserve the remainder, and keep the quotient path available for what comes next.

; Input: year in RCX
; Output: month in RDX, day in R8

	mov rax, rcx
	xor rdx, rdx
	mov rbx, 19
	div rbx
	mov r9, rdx        ; a = Y mod 19
	; ...reuse RAX for each intermediate
	; keep a, b, c, h, l, m in stable registers (r9, r10, r11, etc.)
	; no branches, pure arithmetic drift

Even this short fragment shows the deeper pattern. The code does not “know” Easter. It preserves a lawful sequence of transforms. The machine is not retrieving a holiday from memory; it is carrying a structured relation through register state.

### C++ (Semantic Mirror)

```cpp
struct Easter {
	int month;
	int day;
};

Easter easter(int Y) {
	int a = Y % 19;
	int b = Y / 100;
	int c = Y % 100;
	int d = b / 4;
	int e = b % 4;
	int f = (b + 8) / 25;
	int g = (b - f + 1) / 3;
	int h = (19*a + b - d - g + 15) % 30;
	int i = c / 4;
	int k = c % 4;
	int l = (32 + 2*e + 2*i - h - k) % 7;
	int m = (a + 11*h + 22*l) / 451;
	int month = (h + l - 7*m + 114) / 31;
	int day = ((h + l - 7*m + 114) % 31) + 1;
	return {month, day};
}
```

This is the semantic mirror of the assembly manifold. The C++ version makes the semantic names immediately legible; the assembly version makes the execution discipline immediately legible. One clarifies the conceptual coordinates. The other clarifies the machine constraints that must preserve them.

Read together, they show the same structure surviving across two manifolds. In C++, the variables look like mathematics. In assembly, the same relations are distributed across registers, calling convention, and instruction sequence. That survival of structure across representation is the real point of the chapter.

## 15.7 Walking the Machine: Sample Runs

Let’s walk the machine with one actual year closely enough that the reader can inhabit it.

Take `Y = 2025`.

At the semantic level, the coordinates become:

`a=11, b=20, c=25, d=5, e=0, f=1, g=6, h=14, i=6, k=1, l=4, m=0, month=4, day=20`

At the machine level, the walk looks like this:

- `RCX = 2025` enters as the input year.
- `RAX <- RCX`, `RDX <- 0`, `div 19` yields quotient `106` in `RAX` and remainder `11` in `RDX`; preserve that remainder as `a`.
- Reusing the same division discipline, split `2025` into `b = 20` and `c = 25` by dividing through `100`.
- Continue the manifold through successive partitions and remainders: `d = 5`, `e = 0`, `f = 1`, `g = 6`.
- Combine the preserved coordinates to form the first deep seasonal correction: `h = 14`.
- Compute the local weekly adjustment: `i = 6`, `k = 1`, then `l = 4`.
- The final correction term collapses cleanly: `m = 0`.
- The semantic glyph emerges only at the end: `month = 4`, `day = 20`.

The C++ mirror records the same walk in more readable symbolic form:

```cpp
int a = 2025 % 19;                  // 11
int b = 2025 / 100;                 // 20
int c = 2025 % 100;                 // 25
int d = b / 4;                      // 5
int e = b % 4;                      // 0
int f = (b + 8) / 25;               // 1
int g = (b - f + 1) / 3;            // 6
int h = (19*a + b - d - g + 15) % 30; // 14
int i = c / 4;                      // 6
int k = c % 4;                      // 1
int l = (32 + 2*e + 2*i - h - k) % 7; // 4
int m = (a + 11*h + 22*l) / 451;    // 0
int month = (h + l - 7*m + 114) / 31; // 4
int day = ((h + l - 7*m + 114) % 31) + 1; // 20
```

This is the apprenticeship in its clearest form. The reader can see the same structure three ways at once: as mathematics, as register choreography, and as semantic code.

Or, in summary:

2024 → March 31
2025 → April 20
2026 → April 5

Each intermediate value is a coordinate. Each operation is a projection. The output is a semantic glyph. This is a manifold you can walk.

## 15.8 TokenQuine and the Other End of the Runtime

If EasterDate shows how a classical machine preserves a lawful structure through explicit state transitions, TokenQuine shows how a transformer-facing tool can make representational cost and token structure visible without pretending to be the model itself.

Its architecture is deliberately layered. Text, files, standard input, or conversations enter a canonical representation stage. Tokenizers then impose different segmentations on the same underlying material. Comparison stages reveal where those representations disagree. Feedforward summary stages derive counts, heuristics, and cost-oriented estimates. Projection stages render the analysis back out as text, JSON, or Markdown.

The effect is pedagogical but not shallow. TokenQuine is a tool for understanding tools. It reveals the first layer of transformer cost by making tokenization inspectable. It can even turn its own files into objects of inspection. In that sense, it is the reflective counterpart to EasterDate. EasterDate makes stack runtime visible. TokenQuine makes token runtime visible.

The chapter needs both. EasterDate alone might suggest that the book's argument lives only in deterministic machinery. TokenQuine alone might suggest that the book's argument lives only near language models. Together they show the full confluence: human formation and machine behavior meeting on both sides of the representational divide.

## 15.9 Why These Runtimes Matter: History, Encoding, Confluence

EasterDate and TokenQuine are the first time the book's two programming geometries stand side by side in public form.

Historically, EasterDate is not itself the original algorithm, but our assembly-language instantiation of a much older calendrical problem: finding lawful closure for Easter within the Church's timekeeping framework. In its modern form, the program borrows Gauss's algorithm in service of calendar manipulation. Gauss compressed astronomy, modular arithmetic, and tradition into a walkable sequence of transforms; our assembly version re-enacts that compression in executable form. Each register holds a coordinate from Gauss; each instruction is a projection from a long ecclesiastical and mathematical lineage; each intermediate value is a point on a centuries-old calendrical surface.

TokenQuine performs an analogous compression on the transformer's side. It takes a diffuse problem, how text becomes tokens, cost, and representational burden, and turns it into a layered inspection runtime. Canonical form, tokenization, comparison, summarization, and projection become a public path rather than a hidden service.

Together they show authorship as a coupled runtime. The machine shapes the reasoning as much as the reasoning shapes the executable artifact. History becomes structure, structure becomes code, and code becomes a space the human can enter without losing sight of the machine.

## 15.10 The Directory as Proof: Structure Over Narrative

The EasterDate repository is not merely source code. The TokenQuine repository is not merely a utility package. Each is the structural record of a coupled runtime. In EasterDate, the directory tree, the calling convention notes, the stack diagrams, and the assembly modules are the modern equivalent of the medieval computus tables: a shared external artifact where lineage becomes explicit. In TokenQuine, the layered package structure, analysis pipeline, comparison routines, and projection modules make the path from text to token report equally explicit.

This is the difference between narrative AI and structural AI. Narrative AI produces stories; structural AI helps build the structure in which understanding lives. EasterDate is powerful because it reconstructs a historical algorithm into a walkable state machine. TokenQuine is powerful because it reconstructs token cost and representation into a walkable inspection pipeline. [The EasterDate repository at GitHub is public proof.](https://github.com/tjpools/EasterDate/) [The TokenQuine repository at GitHub is public proof.](https://github.com/tjpools/tokenQuine)

## 15.11 From Glyph to World: The Book's Origin

EasterDate was just a glyph until we developed it into a program we could walk. TokenQuine would have remained a loose intuition about token cost until it became a layered instrument we could run against its own artifacts. More importantly, the structures we built are what led us to write this book. They made visible a walkable geometry of computation that narrative AI is too simple to carry. Meaning is not in the answer; meaning is in the structure, in the walk, in the runtime we can inspect.

This is why the book exists. EasterDate and TokenQuine are the first walkable structures we built that made the present age legible at human scale: an age in which the space of reasoning itself can be extended by tools and in which runtime can be revealed instead of merely consumed. They are the first clear proof, in our own work, that a human craftsman and modern machine machinery could inhabit one executable manifold without collapsing into one another.

This is the hinge of the book. This is the first sculpture that taught us what the larger sculpture had to become.

The next question is not how to admire that sculpture, but how to place it in the longer history that made it possible. If EasterDate is a local proof that structure can become walkable, Chapter 16 asks when structure itself first became an object of thought.
