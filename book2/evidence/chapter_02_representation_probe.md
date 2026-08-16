# Chapter 2 Probe — Representation Becomes Numerical

**Status:** Verified August 12, 2026  
**Implementation:** [chapter_02_representation_probe.py](chapter_02_representation_probe.py)  
**Dependencies:** Python standard library only

## Claims Under Test

1. A vocabulary identifier is an assigned index, not an intrinsic meaning of its token.
2. A representation policy can discard distinctions among different inputs.

## Input Policy

Source text:

```text
 OPEN 
```

Normalization:

1. Unicode NFC normalization
2. Unicode case folding
3. removal of leading and trailing whitespace

Tokenization splits the normalized text on whitespace. This is a declared toy tokenizer, not a model of every production tokenizer.

## Base Representation

| Token | Identifier | Illustrative vector |
|---|---:|---|
| `<unk>` | 0 | $(0.0,0.0,0.0)$ |
| `locked` | 1 | $(0.8,0.1,-0.2)$ |
| `unlocked` | 2 | $(0.6,0.4,0.3)$ |
| `open` | 3 | $(0.2,0.9,0.5)$ |

The vectors are fixed probe values. They are not learned embeddings and carry no semantic or geometric claim.

## Permuted Representation

| Token | Identifier | Illustrative vector |
|---|---:|---|
| `unlocked` | 0 | $(0.6,0.4,0.3)$ |
| `open` | 1 | $(0.2,0.9,0.5)$ |
| `<unk>` | 2 | $(0.0,0.0,0.0)$ |
| `locked` | 3 | $(0.8,0.1,-0.2)$ |

The token-to-identifier assignment changes. The table rows move consistently with that assignment.

## Assertions

For the token `open`:

$$
\operatorname{id}_{base}(open)=3
$$

and

$$
\operatorname{id}_{permuted}(open)=1.
$$

Therefore the one-hot coordinates differ:

$$
(0,0,0,1)\ne(0,1,0,0).
$$

Consistent table permutation preserves the selected vector:

$$
E_{base}[3]=E_{permuted}[1]=(0.2,0.9,0.5).
$$

For the distinct out-of-vocabulary inputs `ajar` and `obstructed`:

$$
\operatorname{id}_{base}(ajar)
=\operatorname{id}_{base}(obstructed)
=\operatorname{id}_{base}(<unk>)
=0.
$$

The policy therefore discards the distinction between those inputs after unknown-token mapping.

## Pass Conditions

- normalization produces the single token `open`
- the two vocabularies assign different identifiers to `open`
- their one-hot coordinates differ
- consistently permuted tables return the same vector for `open`
- two distinct unknown inputs return the same identifier and vector

## Observed Result

The probe passed every assertion:

| Measurement | Base | Permuted | Result |
|---|---:|---:|---|
| `open` identifier | 3 | 1 | changed |
| `open` one-hot coordinate | $(0,0,0,1)$ | $(0,1,0,0)$ | changed |
| selected vector | $(0.2,0.9,0.5)$ | $(0.2,0.9,0.5)$ | preserved |

`ajar` and `obstructed` both produced identifier `0` and vector $(0.0,0.0,0.0)$ under the declared unknown-token policy.

The result supports the two claims under test. It does not assign meaning to the preserved vector or generalize the toy policy to production tokenizers.

## Failure Conditions

- the selected vector changes under consistent permutation
- the test attributes semantics to an integer identifier
- the illustrative table is described as learned
- unknown-token collapse is generalized to tokenizers without such a policy
- storage layout, training, or learned geometry is inferred from the probe

## Scope

The probe establishes index arbitrariness under consistent permutation and one concrete form of information loss. It does not establish how production tokenizers segment text, how embeddings are trained, what vectors mean, or how representations are stored and executed.
