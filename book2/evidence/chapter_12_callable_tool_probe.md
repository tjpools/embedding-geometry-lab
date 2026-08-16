# Chapter 12 Probe — From Specification to Callable Tool

**Status:** Verified August 14, 2026  
**Implementation:** [chapter_12_callable_tool_probe.py](chapter_12_callable_tool_probe.py)  
**Dependencies:** Python standard library only  
**Chapter brief:** [../chapter_briefs/chapter_12.md](../chapter_briefs/chapter_12.md)

## Claim Under Test

An architecture becomes callable only when distinct software contracts agree: a framework supplies the declared operation, a structured package binds dimensions to parameters and metadata, a loader validates before construction, a runtime supplies required capabilities, and a request/response interface translates across the callable boundary.

## Declared Fixture

The architecture specification is `book2.affine-row` version `1.0`. It declares operation `affine_row`, input dimension 3, and output dimension 2. The framework registry contains exactly that operation. The selected runtime advertises `float64_arithmetic` and `structured_json`.

The package is canonical structured JSON containing four top-level interfaces:

- manifest and required runtime capability
- architecture identifier, version, operation, and dimensions
- weight and bias parameter payload
- request and response schema names

Canonical serialization uses sorted object keys and compact separators. The resulting package is 381 bytes with SHA-256:

`886c2466502250a0cbb654622dd47237cc433e28cb3ed333be3cf07fa6f74107`

## Valid Load and Invocation

The loader parses with `json.loads`, then checks required fields, parameter shapes, operation availability, runtime capability, and interface schema. Construction occurs only after all checks pass with result `PACKAGE_VALID`.

The callable request is:

```json
{"schema":"vector.v1","values":[2.0,-1.0,0.5]}
```

The interface validator translates that document into internal row $(2.0,-1.0,0.5)$. For each output row $j$, the registered operation computes

$$
y_j=\sum_i x_iW_{ji}+b_j.
$$

With fixed weights and bias, the exact internal output and declared response values are

$$
(3.25,-1.5).
$$

Loading the same canonical package again and invoking the same request produces an identical validation result, internal rows, and response object.

## Corrupted-Package Control

The control changes only the architecture's declared input dimension from 3 to 4. It preserves the complete parameter payload byte-for-byte under canonical JSON serialization. Because each weight row still has length 3, package validation returns:

`PARAMETER_SHAPE_MISMATCH`

The result is recorded at `package_validation`. The loader construction count remains unchanged, no callable object is returned, and corrupt invocation count is zero. This distinguishes rejection before invocation from a later arithmetic failure.

## Validation Gates

- valid package accepted as `PACKAGE_VALID`
- callable tool constructed only after acceptance
- exact response values equal $(3.25,-1.5)$
- reload validation and reinvocation are identical
- corrupt control preserves the parameter payload
- corrupt dimension returns `PARAMETER_SHAPE_MISMATCH`
- corrupt package is rejected before construction
- corrupt package is rejected before invocation

All gates pass through embedded assertions.

## Evidence Boundary

This dependency-free fixture demonstrates one local contract chain. It is not a production framework, a real ecosystem package standard, an interoperability test, a performance benchmark, a model-quality evaluation, or full language-model inference. It does not tokenize or decode, does not trace Chapter 15 token-through-machine execution, and does not perform Chapter 16 limits analysis.