# Chapter 10 Visual — Attention Opens Direct Paths

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_10_attention_direct_paths.svg](chapter_10_attention_direct_paths.svg)  
**Generator:** [chapter_10_attention_direct_paths.py](chapter_10_attention_direct_paths.py)  
**Data source:** [../evidence/chapter_10_attention_paths_probe.py](../evidence/chapter_10_attention_paths_probe.py)

**Production exports:**

- [full-size color PNG](chapter_10_attention_direct_paths.png)
- [full-size grayscale PNG](chapter_10_attention_direct_paths_grayscale.png)
- [100-pixel thumbnail](chapter_10_attention_direct_paths_thumbnail.png)

## Structural Reveal

Attention permits a value at one position to contribute to another position's output through one weighted combination edge rather than an intervening recurrent-state chain.

## Caption

The recurrent comparison carries position 1 through five state updates. For attention query 5, all five value vectors contribute directly to one output through normalized weights. Changing only value 1 leaves scores and weights unchanged while changing the output by its fixed weighted contribution. Edge counts describe the declared graphs, not measured execution time.

## Alternative Text

The upper lane shows x one entering hidden state one and proceeding through hidden states two, three, four, and five, labeled as five abstract edges. The lower lane shows value vectors one through five, with weights approximately 0.271, 0.134, 0.190, 0.134, and 0.271, each connected directly to output five. Their displayed weighted contributions sum to output approximately 0.463 and 0.187. A control band says that adding 0.4 and negative 0.2 to value one leaves scores and weights unchanged but changes output five by approximately 0.108 and negative 0.054. A causal-mask band says query two admits positions one and two while positions three through five are excluded by rule. A footer states that normalized weights are not a causal explanation.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 10 probe
- External assets: none
- Typeface: DejaVu Sans
- Format: SVG, 1200 × 760 view box
- Deterministic SVG SHA-256: `5446870861be900ef734f6ce152637b1230b54a6c01425ed8370588d70781d58`

## Required Tests

| Test | Result |
|---|---|
| weights, contributions, output, and control derive from the verified probe | pass |
| SVG parses and rasterizes | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export is nonblank | pass |
| recurrent chain and attention fan-in remain recognizable at 100 pixels wide | pass |
| path and mask distinctions do not rely on color alone | pass |
| full-size labels, arrows, contribution values, and bands do not clip or overlap | pass |
| graph edge counts remain distinct from measured runtime | pass |
| exactly one Chapter 10 anchor remains in the production package | pass |