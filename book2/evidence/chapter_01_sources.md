# Chapter 1 Source Ledger — Rules, Operations, and Programs

**Status:** Source basis established August 12, 2026  
**Scope:** Declarative symbolic reasoning, operator-based planning, symbols and search, and Rust control-flow enforcement  
**Chapter brief:** [../chapter_briefs/chapter_01.md](../chapter_briefs/chapter_01.md)

## Source Standard

This ledger grounds the chapter's symbolic-AI lineage and programmed-panel terminology. The door transition itself remains grounded separately by [chapter_01_door_model.md](chapter_01_door_model.md) and its execution-verified [Rust source](chapter_01_door_model.rs).

Sources are used only for the claims named below. Historical symbolic-AI papers do not establish that the toy door model corresponds to a physical door, and Rust documentation does not establish that a successfully executing program is empirically correct or operationally adequate.

## Sources

### S1 — Programs with Common Sense

John McCarthy, "Programs with Common Sense," in *Proceedings of the Symposium on Mechanisation of Thought Processes*, Teddington, England, 1959. The paper was presented in December 1958.

- URL: https://www-formal.stanford.edu/jmc/mcc59/mcc59.html
- Accessed: August 12, 2026
- Authority: Primary historical source hosted by the author's Stanford archive
- Supports: Formal-language expressions as machine representations; declarative sentences as premises; an immediate deduction routine producing consequences; the distinction between represented premises, inference, heuristic premise selection, and action
- Limitation: The Advice Taker was a proposal, and McCarthy explicitly left major heuristic and implementation questions unresolved. The paper does not establish that deduction alone supplies search control, truth, or successful physical action.

### S2 — STRIPS

Richard E. Fikes and Nils J. Nilsson, "STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving," *Artificial Intelligence* 2, nos. 3–4 (December 1971): 189–208.

- DOI: https://doi.org/10.1016/0004-3702(71)90010-5
- Accessed: August 12, 2026
- Authority: Primary peer-reviewed AI research article
- Supports: Operator-based problem solving as a historical symbolic-AI method; represented conditions governing operator applicability; represented effects changing a modeled state for planning
- Limitation: The chapter uses a deliberately simplified precondition/effect notation. It does not reproduce the full STRIPS formalism, theorem prover, planner, execution monitoring, or treatment of change.

### S3 — Symbols and Search

Allen Newell and Herbert A. Simon, "Computer Science as Empirical Inquiry: Symbols and Search," *Communications of the ACM* 19, no. 3 (March 1976): 113–126.

- DOI: https://doi.org/10.1145/360018.360022
- Accessed: August 12, 2026
- Authority: Primary peer-reviewed research article and ACM Turing Award lecture
- Supports: Physical symbol systems and heuristic search as explicit claims in the historical development of AI and computer science
- Limitation: The physical symbol system hypothesis is a historical scientific claim, not a premise this chapter proves or requires. It does not make every program a symbolic reasoner or every transformer a symbolic system.

### S4 — Rust Match Expressions

The Rust Project Developers, "Match expressions," *The Rust Reference*.

- URL: https://doc.rust-lang.org/reference/expressions/match-expr.html
- Accessed: August 12, 2026
- Authority: Official language reference
- Supports: A `match` expression branches by comparing a typed scrutinee with arm patterns and selecting the first matching arm
- Limitation: Pattern matching determines language-level control flow over represented values. It does not validate the modeled domain or physical interpretation.

### S5 — Rust Result and Try Propagation

The Rust Project Developers, "Error handling with the `Result` type," Rust standard-library documentation, and "The try propagation expression," *The Rust Reference*.

- URLs: https://doc.rust-lang.org/std/result/ and https://doc.rust-lang.org/reference/expressions/operator-expr.html#the-question-mark-operator
- Accessed: August 12, 2026
- Authority: Official language and standard-library documentation
- Supports: `Result<T, E>` as either `Ok(T)` or `Err(E)`; `?` extracting an `Ok` value or returning an `Err` early from the enclosing function
- Limitation: `Result` records a program-defined success or error value. An `Ok` result is not evidence that a physical transition occurred or that a task criterion was met.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Symbolic systems can represent premises and derive consequences through explicit inference procedures. | S1 | McCarthy's Advice Taker proposal separates represented declarative premises, immediate deduction, heuristic premise selection, and resulting imperatives. |
| Planning operators can be gated by represented conditions and update represented states. | S2 | In the chapter's STRIPS-inspired toy notation, an action is applicable when its declared preconditions hold, and its effects update the represented fact set. |
| Symbols and search are part of AI's technical history. | S1, S2, S3 | Symbolic representation, deduction, operator-based planning, and heuristic search were explicit subjects in foundational AI research. |
| Rust pattern matching selects behavior over typed represented states. | S4 | Each declared `DoorState` variant reaches the matching branch in `unlock` or `open`. |
| Rust can make success and failure explicit and propagate failure through composition. | S5 | The door functions return `Ok(next_state)` or `Err(reason)`, and `?` returns the first error before the next operation runs. |
| Similar transition traces do not imply identical constraint mechanisms. | S1, S2, S4, S5 | The algebraic, symbolic, and programmed panels align on selected represented transitions while deriving permission and consequence differently. |

## Prohibited Inferences

The sources do not warrant claims that:

- symbolic AI, algebra, and programming languages are equivalent systems
- rule applicability establishes truth
- successful deduction guarantees useful search or successful action
- the toy action notation is a complete implementation of STRIPS
- the physical symbol system hypothesis is proven by the chapter
- all AI systems or transformers are symbolic rule engines
- Rust's type and control-flow checks validate physical correspondence
- `Ok` means that an actuator moved or a real door opened
- internal validity establishes empirical truth, operational adequacy, or justified trust

## Drafting Requirement

Every sourced technical or historical sentence in Chapter 1 must map to this ledger or trigger an explicit ledger update. Final references must preserve the distinction between presentation year and proceedings year for McCarthy's paper.