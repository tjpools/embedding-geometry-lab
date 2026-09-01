# Chapter 1 Formal Artifact — Door Transition

**Status:** Formalized; Rust execution verified August 12, 2026  
**Chapter:** 1 — Rules, Operations, and Programs  
**Purpose:** Compare three internal sources of permission and consequence over one represented state space.

## Scope

Modeled mechanism assumption:

$$
\text{locked} \implies \text{closed}
$$

This assumption applies only to the mechanism modeled here.

Excluded from the internal model:

- sensor calibration and freshness
- mechanical faults and transitional states
- actuator behavior
- obstruction and task suitability
- correspondence between represented and physical state

## State Model

Let

$$
B=\{L,U\},\qquad P=\{C,O\}
$$

where $B$ is bolt state and $P$ is position state. The raw product is

$$
X=B\times P.
$$

The modeled mechanism admits

$$
D=\{(L,C),(U,C),(U,O)\}\subset X.
$$

Use the abbreviations

$$
LC=(L,C),\qquad UC=(U,C),\qquad UO=(U,O).
$$

## Algebraic View

Define partial transformations $u,o:D\rightharpoonup D$:

$$
u(LC)=UC
$$

and

$$
o(UC)=UO.
$$

All other inputs are undefined. Composition is read right to left. Therefore,

$$
(o\circ u)(LC)=UO,
$$

while

$$
(u\circ o)(LC)
$$

is undefined because $o(LC)$ is undefined.

**Permission:** the input lies in the domain of the partial transformation.  
**Consequence:** the transformation returns another element of $D$.

## Symbolic-AI View

Initial facts:

```text
locked
closed
```

Rules:

```text
ACTION UNLOCK
PRECONDITIONS: locked, closed
EFFECTS: unlocked, closed, not locked

ACTION OPEN
PRECONDITIONS: unlocked, closed
EFFECTS: unlocked, open, not closed
```

The represented effect of `UNLOCK` satisfies the represented preconditions of `OPEN`:

```text
locked, closed
    --UNLOCK-->
unlocked, closed
    --OPEN-->
unlocked, open
```

**Permission:** represented facts satisfy an action's preconditions.  
**Consequence:** represented effects update the fact set.

## Programmatic View

The standalone source is [chapter_01_door_model.rs](chapter_01_door_model.rs).

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DoorState {
    LockedClosed,
    UnlockedClosed,
    UnlockedOpen,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum DoorError {
    AlreadyUnlocked,
    DoorOpen,
    Locked,
    AlreadyOpen,
}

fn unlock(state: DoorState) -> Result<DoorState, DoorError> {
    match state {
        DoorState::LockedClosed => Ok(DoorState::UnlockedClosed),
        DoorState::UnlockedClosed => Err(DoorError::AlreadyUnlocked),
        DoorState::UnlockedOpen => Err(DoorError::DoorOpen),
    }
}

fn open(state: DoorState) -> Result<DoorState, DoorError> {
    match state {
        DoorState::LockedClosed => Err(DoorError::Locked),
        DoorState::UnlockedClosed => Ok(DoorState::UnlockedOpen),
        DoorState::UnlockedOpen => Err(DoorError::AlreadyOpen),
    }
}

fn unlock_then_open(state: DoorState) -> Result<DoorState, DoorError> {
    let state = unlock(state)?;
    open(state)
}

fn main() {
    assert_eq!(
        unlock_then_open(DoorState::LockedClosed),
        Ok(DoorState::UnlockedOpen),
    );
    assert_eq!(open(DoorState::LockedClosed), Err(DoorError::Locked));
}
```

### Execution Record

- Environment: Linux `x86_64-unknown-linux-gnu`
- Compiler: `rustc 1.97.1 (8bab26f4f 2026-07-14)`
- Edition: Rust 2024
- Compile policy: warnings denied
- Test result: 3 passed; 0 failed

Observed program output:

```text
unlock_then_open(LockedClosed) = Ok(UnlockedOpen)
open(LockedClosed) = Err(Locked)
```

The tests cover every input branch of `unlock` and `open` and verify that operation order changes the result from a successful composition to a rejected first step.

**Permission:** a represented state reaches a matched branch under the language's type and control-flow rules.  
**Consequence:** execution returns `Ok(next_state)` or an explicit `Err`.

## Cross-View Alignment

| Transition | Algebraic | Symbolic AI | Programmatic |
|---|---|---|---|
| unlock closed door | $u(LC)=UC$ | `UNLOCK` preconditions hold | `unlock(LockedClosed) = Ok(UnlockedClosed)` |
| open unlocked door | $o(UC)=UO$ | `OPEN` preconditions hold | `open(UnlockedClosed) = Ok(UnlockedOpen)` |
| open locked door | $o(LC)$ undefined | `OPEN` preconditions fail | `open(LockedClosed) = Err(Locked)` |
| unlock, then open | $(o\circ u)(LC)=UO$ | effects of `UNLOCK` enable `OPEN` | `unlock_then_open(LockedClosed) = Ok(UnlockedOpen)` |

The views align on three represented states and two ordered transitions. They do not share a source of permission or a mechanism of consequence.

## Evidence Boundary

Let $W$ denote physical door states, $S$ sensor readings, and $D$ represented states. Empirical correspondence requires a tested chain such as

$$
W_t\longrightarrow S_t\overset{\operatorname{encode}}{\longrightarrow}D_t.
$$

Operational adequacy requires a further tested chain:

$$
D_t
\longrightarrow \text{command}
\longrightarrow \text{controller}
\longrightarrow \text{actuator}
\longrightarrow S_{t+1}
\overset{\operatorname{encode}}{\longrightarrow}D_{t+1}
\longrightarrow \text{task criterion}.
$$

No equation, rule, or function above establishes either chain by internal validity alone.

## Result

Algebraic operations, symbolic rules, and programs constrain transformations in different ways. Each operates on represented objects and can establish validity within its own system. None, by internal success alone, establishes correspondence with observation or adequacy for a physical task. Stronger claims require tested evidence chains beyond the formal operation.
