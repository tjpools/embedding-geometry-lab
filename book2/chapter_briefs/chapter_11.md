# Chapter 11 Brief — The Transformer

**Status:** Verified; Part III integrated  
**Part:** III — Attention Becomes Architecture  
**Module:** `ai.transformer`  
**Visual anchor:** **Transformer Architectural Elevation**

## Reader Entry

Chapter 10 established scaled dot-product attention as one inspectable operator and separated scores, normalized weights, and value contributions. The reader may still treat attention as the entire transformer, treat one attention map as a complete explanation, or assume that adding component names automatically establishes a working architecture.

## Intended Exit

The reader can distinguish:

- incoming representation from positional information
- projection parameters from runtime activation values
- one attention head from multi-head composition
- concatenated head output from projected model output
- attention sublayer output from residual-plus-normalization output
- first residual/normalization interface from second residual/normalization interface
- positionwise feed-forward transformation from attention mixing across positions
- a deterministic architectural fixture from a trained production model
- component contribution controls from causal or semantic claims

## Central Question

What additional interfaces must be assembled around attention before the operation becomes a transformer block?

## Chapter Claim

A transformer block is an interface-constrained assembly: incoming representations combine with positional information, produce query/key/value projections, execute multiple attention heads, concatenate and project head outputs, then pass through residual-plus-normalization and a positionwise feed-forward stage with a second residual-plus-normalization interface. The chapter probe verifies these equations and component boundaries in a deterministic fixture. It does not train parameters, establish production performance, or claim that one block is a complete end-to-end model.

## Chapter Result

In the fixed four-position, four-dimensional, two-head fixture, each head produces distinct normalized attention rows and every row sums to one within tolerance. For query position 4, head 1 weights are approximately $(0.231425,0.224919,0.236720,0.306937)$ and head 2 weights are approximately $(0.316628,0.297562,0.194005,0.191805)$. After concatenation and output projection, the attention contribution at position 4 is approximately $(0.162918,-0.060338,0.457843,-0.006945)$. The final block output after the second normalization at position 4 is approximately $(0.255460,-1.698430,0.654426,0.788544)$. A no-attention control (zeroing the projected multi-head output before the first residual) changes the final output at every position, with per-position difference norms approximately $(0.905029,1.337468,0.464690,0.254784)$.

## Inherited Terms and Claims

From Chapter 8:

- coordinate interpretations require declared transformation and comparison rules

From Chapter 9:

- dependency structure is distinct from measured runtime behavior
- repeated computation paths require explicit execution interfaces

From Chapter 10:

- attention scores, normalized weights, and value vectors are distinct interfaces
- one attention operation is not yet a full transformer architecture
- attention weights are not by themselves causal explanations

## Dependency Alignment

**Incoming edges:**

| Source | Target | Inherited requirement |
|---|---|---|
| `ai.attention` | `ai.transformer` | Scaled dot-product attention is available as one operator. |
| `math.tensors` | `ai.transformer` | Multi-axis representation and projection shapes are available. |

**Outgoing edge:**

| Source | Target | Destination | Handoff |
|---|---|---:|---|
| `ai.transformer` | `programming.tools` | 12 | The architecture now exists as a constrained build target for frameworks, runtimes, and tooling. |

## Reader Movement

1. Start with fixed incoming representations and fixed positional vectors.
2. Form combined model-dimension inputs.
3. Apply fixed query, key, and value projections.
4. Split projected vectors into at least two heads.
5. Compute each head's scaled attention scores and normalized weights.
6. Form each head output from weighted value combinations.
7. Concatenate heads and apply output projection.
8. Apply first residual connection and declared normalization formula.
9. Apply positionwise feed-forward transformation.
10. Apply second residual connection and declared normalization formula.
11. Run a no-attention control that changes one component while preserving all others.
12. Carry the assembled architecture toward Chapter 12 without crossing into Chapter 15 token-through-machine flow or Chapter 16 limits framing.

## Evidence Plan

Create a dependency-free deterministic Python probe that records:

- incoming representations and positional vectors
- fixed projection matrices for $Q$, $K$, $V$, output projection, and feed-forward sublayers
- per-head score matrices and softmax-normalized rows
- concatenated head outputs and projected attention outputs
- first and second residual equations and both normalization outputs
- normalization row means and variances under

$$
\text{layer\_norm}(x)=\frac{x-\operatorname{mean}(x)}{\sqrt{\operatorname{var}(x)+\varepsilon}}
$$

- deterministic rerun equality
- a no-attention control showing output change caused by removing projected multi-head attention

The probe must state that the fixture is deterministic and fixed, not trained or production-equivalent.

## Visual Anchor

**Transformer Architectural Elevation** is one deterministic architectural trace showing:

- representation plus positional entry interface
- fixed $Q/K/V$ projections
- two distinct attention heads with normalized rows
- concatenation plus output projection
- first residual plus normalization
- positionwise feed-forward stage
- second residual plus normalization
- control panel showing output differences when attention contribution is removed

**Structural reveal:** attention is one component interface inside a larger constrained assembly. The transformer block arises from the ordered composition, not from attention alone.

The visual must explicitly label this as a deterministic fixture and avoid implying training quality, runtime benchmarks, or full model equivalence.

## Verification Questions

- Are representation and positional inputs declared separately before combination?
- Are all projection and sublayer dimensions recorded and validated?
- Does every attention row in every head normalize to one within tolerance?
- Are at least two heads present and numerically distinct?
- Do both residual equations hold exactly for recorded rows?
- Do both normalization stages satisfy the declared mean/variance properties?
- Is deterministic rerun equality confirmed?
- Does the no-attention control show nonzero output change while preserving other declared settings?
- Is the chapter explicit that this fixture is not trained and not production-equivalent?
- Is Book Two's architectural boundary preserved without stepping into Chapter 15 execution path or Chapter 16 limits?

## Explicit Exclusions

This chapter does not train weights, tune hyperparameters, benchmark kernels, compare hardware, execute tokenization or decoding pipelines, claim semantic interpretation from one block output, reproduce Chapter 15 end-to-end token-through-machine execution, or perform Chapter 16 limits analysis.

## Narrative Transition

Chapter 10 isolated attention. Chapter 11 assembles attention into a transformer block with explicit interfaces and controls. Chapter 12 will shift from block assembly to implementation-facing tool and runtime handoffs.

## Drafting Gate

The transformer-block specification, executable probe, source ledger, deterministic visual production package, and manuscript chapter pass probe, visual, link, analytics, and local error checks. Chapter 11 is verified and passes the Part III integration audit.