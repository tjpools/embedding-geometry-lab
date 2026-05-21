# Chapter 15: EasterDate — From Glyph to Structure

Chapter 14 argued that proper analysis must be structural, geometric, and walkable. EasterDate is where that claim becomes executable.

EasterDate was never just a program. It was the first glyph that became a manifold of meaning: a structure so rich, so walkable, that it demanded a book to explain what it revealed. What began as a calendrical curiosity became the prototype for everything this book argues: meaning is not in the answer, but in the structure; not in the narrative, but in the form you can inhabit.

[View the EasterDate source and structure on GitHub.](https://github.com/tjpools/EasterDate/)

This is not just a program to be read, but a structure to be entered: a first invitation to see systems as layered, navigable spaces.

EasterDate is the moment intent became mechanism, and mechanism preserved intent. It is the first time I realized that computation is not a machine activity but a collaborative traversal of structure. The machine does not “compute” Easter. We compute it together.

## 15.1 The Question: “What is the date of Easter?”

The question appears simple. But historically, it was never just a matter of retrieval. In the late 16th century, Pope Gregory XIII was deeply concerned with the slippage of the Easter celebration—how the date, once tied to the spring equinox and lunar cycle, had drifted out of sync with the intended astronomical and ecclesiastical markers. The Gregorian reform was not just a calendar correction; it was a demand for a rule that would hardcode the date of Easter based on explicit, repeatable criteria. The result was a centuries-long tradition of *computus*: the lawful, algorithmic determination of Easter through a structured interplay of calendar, lunar cycle, and ecclesiastical rule. The moment the question is asked computationally, it changes shape:

- What structure determines the date?
- What algorithm expresses that structure?
- What representation makes the algorithm executable?
- What environment makes the representation meaningful?

EasterDate was the first time I walked through that doorway—and found a world on the other side.

## 15.2 Lookup Table or Algorithm

A lookup table gives answers. An algorithm gives structure. Gauss’s Easter algorithm is not a list of dates. It is a compressed geometry of lunar cycle, solar calendar, and ecclesiastical rule. It does not store the answer in advance. It produces the answer by lawful transformation.

To implement such a procedure is to discover that the algorithm is not merely a recipe. It is a space, and the computation is a path through that space. This is the moment when a program stops being a tool and becomes a world.

The distinction matters. A table preserves outcomes; an algorithm preserves relations. EasterDate is not trivia. It is the prototype of modern algorithmic reasoning.

## 15.3 The Algorithm (Explicit and Walkable)

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

Each line is a projection from one coordinate system to another: mod → circular coordinate, div → partition, +/− → drift, month/day → semantic glyph. This is the manifold. These are the coordinate transforms. This is the walk.

## 15.4 The Coding Strategy: Assembly and C++

### Assembly (Register Choreography)

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

This is the semantic mirror of the assembly manifold.

## 15.5 Walking the Machine: Sample Runs

Let’s walk the machine with actual values:

Year: 2025
a=11 b=20 c=25 d=5 e=0 f=1 g=6 h=14 i=6 k=1 l=4 m=0
month=4 day=20

Or, in summary:

2024 → March 31
2025 → April 20
2026 → April 5

Each intermediate value is a coordinate. Each operation is a projection. The output is a semantic glyph. This is a manifold you can walk.

## 15.6 Why EasterDate Matters: History, Encoding, Collaboration

EasterDate is the first time a human and a machine jointly reconstruct a 1,700-year lineage into a living, executable structure.

Historically, EasterDate is the first global algorithm—a symbolic rule that determines a global social event. Gauss compressed astronomy, modular arithmetic, and tradition into a walkable sequence of transforms. Encoding it in assembly is not implementation—it is reenactment. Each register holds a coordinate from Gauss; each instruction is a projection from Nicaea; each intermediate value is a point on a centuries-old mathematical surface.

EasterDate is the first time I experienced authorship as a coupled manifold: the machine shaping my reasoning as much as I shaped its execution. It is the moment where history becomes structure, structure becomes code, and code becomes a space two minds can inhabit at once.

## 15.7 The Directory as Proof: Structure Over Narrative

The EasterDate repository is not merely source code. It is the structural record of a collaboration between human and machine. The directory tree, the calling convention notes, the stack diagrams, and the assembly modules are the modern equivalent of the medieval computus tables: a shared external artifact where lineage becomes explicit. This is the difference between narrative AI and structural AI. Narrative AI produces stories; structural AI helps build the structure in which understanding lives. EasterDate is powerful because it is the first time the machine and I jointly reconstructed a historical algorithm into a walkable state machine. The repo is the proof.

## 15.8 From Glyph to World: The Book’s Origin

EasterDate was just a glyph until we developed it into a program we could walk. More importantly, the structure we built is what led us to write this book. It was our insight into the walkable geometry of computation that made us realize narrative AI is too simple. Meaning is not in the answer; meaning is in the structure, in the walk, in the collaboration.

This is the hinge of the book. This is the moment where everything aligns.
