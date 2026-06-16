# Chapter 15: EasterDate — From Glyph to Structure

Chapter 14 argued that proper analysis must be structural, geometric, and walkable. EasterDate is where that same demand is lowered into a smaller machine the reader can traverse completely.

It is important to say at the outset what kind of example this is. EasterDate is not being offered as if it were itself an AI system. It is being offered as an apprenticeship in analysis: a bounded object through which the reader can learn what it means to follow transforms, preserve invariants, compare representations, and keep machinery visible. The claim is not that a calendrical algorithm and a transformer are the same thing. The claim is that deep understanding of either requires the same discipline of walking the structure rather than stopping at the glyph. What Chapter 14 named abstractly, this chapter now renders concrete across notation, code, register state, and output.

EasterDate was never just a program. It was the first glyph that became a manifold of meaning: a structure so rich, so walkable, that it demanded a book to explain what it revealed. What began as a calendrical curiosity became the prototype for everything this book argues: meaning is not in the answer, but in the structure; not in the narrative, but in the form you can inhabit.

It was also our historical apprenticeship. We did not merely compute a date. We re-enacted a lineage: ancient astronomy, ecclesiastical calendrics, Gauss's modular arithmetic, twentieth-century calling conventions, and a twenty-first-century x64 toolchain all gathered into one executable artifact. In that sense, EasterDate was a compressed history lesson that ran on silicon.

[View the EasterDate source and structure on GitHub.](https://github.com/tjpools/EasterDate/)

That repository is part of the chapter's evidence. The book gives the reader the path in prose; the repository gives the reader the executable structure, notes, and artifacts that make the path inspectable in public.

As an ebook, this chapter can therefore do something a print chapter cannot: it can leave the reader a direct path outward. A reader who wants only the argument may stay in the prose. A reader who wants inspection, source, and executable detail can follow the link into the repository and continue the apprenticeship there.

This is not just a program to be read, but a structure to be entered: a first invitation to see systems as layered, navigable spaces.

EasterDate is the moment intent became mechanism, and mechanism preserved intent. It is the first time I realized that computation is not a machine activity but a collaborative traversal of structure. The machine does not “compute” Easter. We compute it together.

## 15.1 The Question: “What is the date of Easter?”

The question appears simple. But historically, it was never just a matter of retrieval. In the late 16th century, Pope Gregory XIII was deeply concerned with the slippage of the Easter celebration—how the date, once tied to the spring equinox and lunar cycle, had drifted out of sync with the intended astronomical and ecclesiastical markers. The Gregorian reform was not just a calendar correction; it was a demand for a rule that would hardcode the date of Easter based on explicit, repeatable criteria. The result was a centuries-long tradition of *computus*: the lawful, algorithmic determination of Easter through a structured interplay of calendar, lunar cycle, and ecclesiastical rule. The moment the question is asked computationally, it changes shape:

For readers new to the term, computus simply means the method for calculating the date of Easter.

- What structure determines the date?
- What algorithm expresses that structure?
- What representation makes the algorithm executable?
- What environment makes the representation meaningful?

EasterDate was the first time I walked through that doorway—and found a world on the other side.

## 15.2 EasterDate as a Computational Object

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

## 15.3 Lookup Table or Algorithm

A lookup table gives answers. An algorithm gives structure. Gauss’s Easter algorithm is not a list of dates. It is a compressed geometry of lunar cycle, solar calendar, and ecclesiastical rule. It does not store the answer in advance. It produces the answer by lawful transformation.

To implement such a procedure is to discover that the algorithm is not merely a recipe. It is a space, and the computation is a path through that space. This is the moment when a program stops being a tool and becomes a world.

The distinction matters. A table preserves outcomes; an algorithm preserves relations. EasterDate is not trivia. It is the prototype of modern algorithmic reasoning.

## 15.4 The Algorithm (Explicit and Walkable)

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

## 15.5 The Coding Strategy: Assembly and C++

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

## 15.6 Walking the Machine: Sample Runs

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

## 15.7 Why EasterDate Matters: History, Encoding, Collaboration

EasterDate is the first time a human and a machine jointly reconstruct a 1,700-year lineage into a living, executable structure.

Historically, EasterDate is the first global algorithm—a symbolic rule that determines a global social event. Gauss compressed astronomy, modular arithmetic, and tradition into a walkable sequence of transforms. Encoding it in assembly is not implementation—it is reenactment. Each register holds a coordinate from Gauss; each instruction is a projection from Nicaea; each intermediate value is a point on a centuries-old mathematical surface.

EasterDate is the first time I experienced authorship as a coupled manifold: the machine shaping my reasoning as much as I shaped its execution. It is the moment where history becomes structure, structure becomes code, and code becomes a space two minds can inhabit at once.

## 15.8 The Directory as Proof: Structure Over Narrative

The EasterDate repository is not merely source code. It is the structural record of a collaboration between human and machine. The directory tree, the calling convention notes, the stack diagrams, and the assembly modules are the modern equivalent of the medieval computus tables: a shared external artifact where lineage becomes explicit. This is the difference between narrative AI and structural AI. Narrative AI produces stories; structural AI helps build the structure in which understanding lives. EasterDate is powerful because it is the first time the machine and I jointly reconstructed a historical algorithm into a walkable state machine. The repository at GitHub is the public proof.

## 15.9 From Glyph to World: The Book’s Origin

EasterDate was just a glyph until we developed it into a program we could walk. More importantly, the structure we built is what led us to write this book. It was our insight into the walkable geometry of computation that made us realize narrative AI is too simple. Meaning is not in the answer; meaning is in the structure, in the walk, in the collaboration.

This is why the book exists. EasterDate was the first walkable structure we built together that made the present age legible at human scale: an age in which the space of reasoning itself can be extended by tools. It was the first clear proof, in our own work, that a human craftsman and modern machine machinery could inhabit one executable manifold without collapsing into one another.

This is the hinge of the book. This is the first sculpture that taught us what the larger sculpture had to become.

The next question is not how to admire that sculpture, but how to place it in the longer history that made it possible. If EasterDate is a local proof that structure can become walkable, Chapter 16 asks when structure itself first became an object of thought.
