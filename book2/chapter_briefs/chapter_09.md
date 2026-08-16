# Chapter 9 Brief — Sequence, Memory, and Runtime

**Status:** Verified; Part II integrated  
**Part:** II — Learning Systems  
**Modules:** `ai.sequence`, `programming.runtimes`  
**Visual anchor:** **The Recurrent Bottleneck**

## Reader Entry

Chapters 5 through 7 established typed executable artifacts, repeated parameter adjustment, tensor operations, and partitionable numerical work. The reader may still assume that every sequence position can be computed independently, that a recurrent state is a record of the complete past, or that an operation count predicts elapsed runtime.

## Intended Exit

The reader can distinguish:

- an input sequence from the order in which its elements are processed
- a recurrent state from the complete input history
- parameter sharing across steps from equal state values at those steps
- a forward state dependency from a gradient or sensitivity calculation
- mathematical dependency depth from measured elapsed time
- per-step numerical work from runtime scheduling and kernel execution
- retained state from actual memory traffic or capacity
- a simple recurrent unit from LSTM and GRU gating
- a reproducible operation count from a hardware benchmark

## Central Question

What does ordered recurrent state require from execution, and what can a structural probe establish before runtime performance is measured?

## Chapter Claim

In a declared recurrent computation, each state depends on the preceding state, so the forward dependency path grows one step at a time even when the numerical work inside a step may be implemented by optimized kernels. Repeated multiplication along that path can attenuate or amplify sensitivity in the worked scalar case. These structural facts expose a recurrent bottleneck but do not determine elapsed time, kernel choice, memory traffic, or hardware utilization.

## Chapter Result

For the scalar recurrence

$$
h_t=\tanh(0.5h_{t-1}+x_t),
$$

the final state is approximately $-0.103463$. Its analytic sensitivities to the five ordered inputs are approximately $(0.047456,0.100968,0.202039,0.476350,0.989295)$ and match central finite differences within $1.54\times10^{-11}$. Setting the recurrent weight to zero makes the first four sensitivities zero while retaining final-input sensitivity near $0.961043$. The probe records five updates, predecessor edges, state reads, and state writes, but performs no runtime measurement.

## Inherited Terms and Claims

From Chapter 5:

- accepted source and observable output do not by themselves explain runtime scheduling or hardware cost
- represented values require concrete layout, translation, and execution interfaces

From Chapter 6:

- a parameterized computation is distinct from its training procedure
- a gradient or sensitivity is distinct from an update
- repeated multiplication can produce behavior that one local operation does not reveal

From Chapter 7:

- partitionable work is not observed concurrent execution
- operation count is not elapsed time
- kernels, scheduling, memory movement, precision, workload, and hardware remain part of a performance claim

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `ai.neural` | `ai.sequence` | Parameterized neural computation exists before recurrent state is introduced. |
| `programming.memory` | `programming.runtimes` | Represented values require storage before runtime movement and retention can be discussed. |
| `programming.compilers` | `programming.runtimes` | Translated artifacts exist before scheduling and execution. |
| `programming.hardware` | `programming.runtimes` | Runtime work is scheduled onto concrete execution machinery. |

**Internal interface:**

| Source | Target | Chapter use |
|---|---|---|
| `ai.sequence` | `programming.runtimes` | Ordered state dependencies constrain when successive recurrent steps become ready to execute. |

**Outgoing edge:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `ai.sequence` | `ai.attention` | 10 | The recurrent path supplies the bounded comparison against direct pairwise attention paths. |

## Reader Movement

1. Declare an ordered input sequence and one scalar recurrent update.
2. Unroll the recurrence into distinct time steps with shared parameters.
3. Record the state produced at every step.
4. Trace how one early input can affect later states only through intervening states.
5. Derive sensitivity as a product of local recurrent derivatives.
6. Check the analytic sensitivity against finite differences.
7. Set the recurrent weight to zero and observe the loss of cross-position dependence.
8. Count sequential dependency depth, state reads, and state writes without converting them into timing or byte-traffic claims.
9. Place LSTM and GRU gates in the historical response to recurrent-state limitations without claiming that the probe implements them.
10. Hand the recurrent path to Chapter 10 for a measured comparison with attention.

## Evidence Plan

Create a dependency-free Python probe that records:

- the complete ordered input sequence
- initial state, recurrent weight, and activation
- every pre-activation and hidden state
- the predecessor edge required by every step
- analytic sensitivity of the final state to each input
- central finite-difference checks for those sensitivities
- a zero-recurrence control in which earlier inputs no longer affect the final state
- structural counts for steps, recurrent edges, state reads, and state writes

The verified [recurrent-runtime probe](../evidence/chapter_09_recurrent_runtime_probe.md) records these values. It may call them structural counts. It may not report them as measured allocation, memory traffic, kernel launches, latency, throughput, utilization, or energy.

## Visual Anchor

**The Recurrent Bottleneck** is one left-to-right execution trace containing:

- ordered inputs $x_1$ through $x_T$
- hidden states $h_0$ through $h_T$
- one predecessor edge between successive hidden states
- local derivative factors along the final-state sensitivity path
- a cumulative runtime-work band that adds one declared step at a time
- a zero-recurrence control whose cross-position path is visibly broken

**Structural reveal:** each recurrent state must be available before its successor can be computed, and influence from an early position reaches the final state through every intervening recurrence.

The runtime-work band represents declared dependency and operation counts, not observed clock time or hardware execution.

## Verification Questions

- Is sequence order declared before recurrent computation?
- Does every state depend only on the declared input and preceding state?
- Are shared parameters kept distinct from state values?
- Is forward dependency kept distinct from gradient computation?
- Do analytic sensitivities match finite differences within tolerance?
- Does the zero-recurrence control remove cross-position sensitivity?
- Are structural counts kept distinct from runtime measurements?
- Are retained states kept distinct from measured memory traffic?
- Are LSTM and GRU claims grounded in appropriate primary sources?
- Does the visual avoid implying that one abstract step equals one kernel launch or fixed duration?

## Explicit Exclusions

This chapter does not benchmark a runtime, inspect a framework scheduler, launch a GPU kernel, measure memory bandwidth, prove asymptotic speedup, implement backpropagation through time, train an RNN, or implement LSTM or GRU cells. It does not claim that recurrent state is human memory or that attenuation of one derivative product explains every long-range modeling limitation.

## Narrative Transition

Part II ends with a visible constraint: a recurrent sequence can reuse one parameterized update while still requiring an ordered chain of state availability. Chapter 10 asks how attention changes that path by computing direct pairwise relationships, while preserving the distinction between a shorter dependency path and measured runtime performance.

## Drafting Gate

The recurrence specification, executable probe, primary-source ledger, deterministic visual production package, and manuscript pass validation. The verified manuscript is [../chapters/chapter_09.md](../chapters/chapter_09.md). Its Part II interfaces are recorded in the [integration audit](../evidence/part_02_integration.md).