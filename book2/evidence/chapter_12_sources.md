# Chapter 12 Source Ledger — From Paper to Tool

**Status:** Source basis established August 14, 2026  
**Scope:** architecture specification, structured JSON parsing, deterministic digests, and bounded model-package contracts  
**Chapter brief:** [../chapter_briefs/chapter_12.md](../chapter_briefs/chapter_12.md)

## Source Standard

The Chapter 12 probe is authoritative for every fixture field, digest, validation code, counter, and output. Primary architecture work and official technical documentation support only the surrounding contract distinctions. No source is used to claim production compatibility, performance, model quality, or ecosystem reliability.

## Sources

### S1 — Attention Is All You Need

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin, “Attention Is All You Need,” *Advances in Neural Information Processing Systems 30*, 2017.

- URL: https://arxiv.org/abs/1706.03762
- Accessed: August 14, 2026
- Authority: primary peer-reviewed Transformer architecture paper
- Supports: the architecture specification inherited from Chapter 11 includes declared attention, projection, residual, normalization, and feed-forward relationships
- Limitation: the paper does not define this chapter's fixture package, loader, runtime registry, or callable API.

### S2 — Python `json` Documentation

Python Software Foundation, “`json` — JSON encoder and decoder,” Python 3 standard-library documentation.

- URL: https://docs.python.org/3/library/json.html
- Accessed: August 14, 2026
- Authority: official Python documentation
- Supports: parsing JSON documents into Python structures with `json.loads`; deterministic key ordering and compact separators are explicit encoder options
- Limitation: JSON syntax alone does not validate this fixture's architecture, shape, runtime, or interface semantics.

### S3 — Python `hashlib` Documentation

Python Software Foundation, “`hashlib` — Secure hashes and message digests,” Python 3 standard-library documentation.

- URL: https://docs.python.org/3/library/hashlib.html
- Accessed: August 14, 2026
- Authority: official Python documentation
- Supports: computing a SHA-256 hexadecimal digest over serialized bytes
- Limitation: equal digests are used here as deterministic artifact identity; the digest does not establish semantic correctness, provenance, or security of an ecosystem package.

### S4 — ONNX Intermediate Representation Specification

ONNX project, “ONNX Intermediate Representation,” official specification documentation.

- URL: https://onnx.ai/onnx/repo-docs/IR.html
- Accessed: August 14, 2026
- Authority: official model-format specification
- Supports: a real model package can distinguish model metadata, graph/operator structure, tensor shape/type information, and serialized tensor data; versioned contracts matter to interpretation
- Limitation: the Chapter 12 JSON fixture is not ONNX, does not claim ONNX compatibility, and does not exercise an ONNX runtime or operator set.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| A published architecture and an executable tool are distinct artifacts. | S1, probe | The architecture supplies an implementation target; callability additionally requires operations, parameters, loading, runtime capabilities, and an interface. |
| Structured parsing precedes semantic validation. | S2, probe | `json.loads` recovers structured fields, after which fixture-specific validators check contracts. |
| A serialized package can be identified deterministically. | S2, S3, probe | Canonical encoder options plus SHA-256 produce a reproducible digest for the exact fixture bytes. |
| Model formats bind several kinds of information. | S4 | Official ONNX documentation illustrates that graph, metadata, type/shape, operators, and tensor data are separate package concerns. |
| Corrupt metadata can be rejected before invocation. | probe | Changing one declared dimension while preserving parameters causes a specific pre-construction validation failure. |

## Prohibited Inferences

These sources and the fixture do not warrant claims that the package is compatible with ONNX or any production framework, that its validator covers real ecosystem failure modes, that deterministic output implies model quality, that SHA-256 proves package trust, that a successful local call predicts performance, or that the probe executes complete Transformer inference.