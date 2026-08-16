# Chapter 10 Brief — Attention Changes the Path

**Status:** Verified; Part III integrated  
**Part:** III — Attention Becomes Architecture  
**Module:** `ai.attention`  
**Visual anchor:** **Attention Opens Direct Paths**

## Reader Entry

Chapter 9 established that a recurrent final state depends on an ordered predecessor chain and that structural dependency depth is not measured runtime. The reader may still treat attention as memory retrieval, interpret a large attention weight as causal importance, or assume a shorter graph path guarantees a faster program.

## Intended Exit

The reader can distinguish:

- query, key, and value vectors
- compatibility score from normalized attention weight
- softmax normalization from Bayesian conditioning
- an attention weight from the value vector it scales
- weighted value combination from copying or selecting one token
- direct graph path from measured latency
- full self-attention from causal masking
- one attention head from multi-head attention
- a visible attention distribution from causal or semantic explanation

## Central Question

How does attention create direct relationships across sequence positions, and what does that changed path not establish?

## Chapter Claim

Scaled dot-product self-attention computes pairwise query-key compatibility, normalizes scores across admitted key positions, and forms each output as a weighted combination of value vectors. In the declared graph, a value at an earlier position contributes directly to a later output rather than passing through every intervening recurrent state. The shorter graph path does not by itself establish causal importance, semantic interpretation, lower latency, or superior task performance.

## Chapter Result

The five-position, one-head fixture produces a final-query weight row of approximately $(0.271126,0.133684,0.190381,0.133684,0.271126)$ and output $(0.463386,0.186623)$. Changing only the first value by $(0.4,-0.2)$ leaves every score and weight unchanged and changes the final output by $(0.108450,-0.054225)$, exactly the first weight times the perturbation within $1.2\times10^{-16}$. The causal case assigns every excluded future position weight zero while renormalizing admitted positions.

## Inherited Terms and Claims

From Chapter 3:

- normalized weights are not automatically Bayesian posterior probabilities

From Chapter 4:

- matrix products are declared transformations; local derivative language is not required to describe the forward attention operation

From Chapter 7:

- partitionable tensor work is not measured concurrent execution
- operation count and graph structure do not determine elapsed time

From Chapter 9:

- forward dependency is distinct from sensitivity or gradient analysis
- the recurrent comparison path is an ordered predecessor chain
- graph path length is not runtime latency

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `math.probability` | `ai.attention` | Normalization over declared alternatives is available without making attention Bayesian inference. |
| `math.matrices` | `ai.attention` | Matrix products and projections are available before query-key scores and value combinations. |
| `ai.sequence` | `ai.attention` | The recurrent predecessor path supplies the bounded architectural comparison. |

**Outgoing edge:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `ai.attention` | `ai.transformer` | 11 | Attention becomes one component assembled with embeddings, position, residual paths, normalization, and feed-forward stages. |

## Reader Movement

1. Return to the five-position sequence from Chapter 9.
2. Separate each position's query, key, and value roles.
3. Compute scaled query-key compatibility scores for one head.
4. Normalize admitted scores with softmax.
5. Multiply each value by its weight and sum the contributions.
6. Show the direct value-to-output path from position 1 to position 5.
7. Change only the first value and verify that weights remain fixed while the output changes predictably.
8. Apply a causal mask and distinguish excluded positions from low learned weights.
9. Compare graph paths with recurrence without making a runtime claim.
10. Hand the operation to Chapter 11 for architectural assembly.

## Evidence Plan

Create a standard-library Python probe that records:

- five declared query, key, and value vectors
- scale factor and complete score matrix
- admitted positions under full and causal attention
- complete softmax weight rows that each sum to one
- every weighted value contribution and output vector
- a value-only perturbation with unchanged scores and weights
- the predicted and observed output difference
- structural source-to-output path lengths for the declared recurrent and attention graphs

The path comparison belongs only to the declared graphs. It may not be reported as measured latency, throughput, memory use, or task quality.

## Visual Anchor

**Attention Opens Direct Paths** is one execution trace with two aligned lanes:

- the upper lane shows the Chapter 9 recurrent path from position 1 through intervening states to position 5
- the lower lane shows the final query connected to all admitted keys and weighted value contributions entering one output
- a value-only control changes one contribution without changing the weight row
- a mask boundary visibly excludes future positions in a subordinate inset

**Structural reveal:** attention permits a value at one position to contribute to another position's output through one weighted combination edge rather than an intervening recurrent-state chain.

The visual must label the relationship as graph structure, not measured execution time or causal attribution.

## Verification Questions

- Are query, key, and value vectors distinct objects?
- Is the scale factor declared before scores are normalized?
- Does every admitted weight row sum to one within tolerance?
- Are excluded masked positions assigned zero output weight rather than described as low relevance?
- Is each output reproduced by summing recorded weighted value contributions?
- Does the value-only perturbation preserve scores and weights exactly?
- Does its output difference equal the perturbed value scaled by the fixed weight?
- Is graph path length kept distinct from runtime performance?
- Are attention weights kept distinct from causal contribution and semantic explanation?
- Is one-head evidence kept distinct from a complete transformer?

## Explicit Exclusions

This chapter does not train attention parameters, implement multi-head attention, add positional encodings, residual paths, normalization, feed-forward layers, or decoding. It does not benchmark recurrence against attention, infer causal importance from weights, claim that attention is explanation, or equate softmax weights with posterior beliefs.

## Narrative Transition

Chapter 10 changes the dependency path but does not yet produce a transformer. Chapter 11 assembles attention with the additional components and interfaces required by the architecture.

## Drafting Gate

The attention specification, executable probe, primary-source ledger, deterministic visual production package, and manuscript chapter pass probe, visual, link, analytics, test, and local error checks. Chapter 10 is verified and passes the Part III integration audit.