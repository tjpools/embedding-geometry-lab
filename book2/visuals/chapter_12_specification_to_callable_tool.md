# Chapter 12 Visual — From Specification to Callable Tool

**Status:** Verified August 14, 2026  
**Canonical source:** [chapter_12_specification_to_callable_tool.svg](chapter_12_specification_to_callable_tool.svg)  
**Generator:** [chapter_12_specification_to_callable_tool.py](chapter_12_specification_to_callable_tool.py)  
**Data source:** [../evidence/chapter_12_callable_tool_probe.py](../evidence/chapter_12_callable_tool_probe.py)

**Production exports:**

- [full-size color PNG](chapter_12_specification_to_callable_tool.png)
- [full-size grayscale PNG](chapter_12_specification_to_callable_tool_grayscale.png)
- [100-pixel thumbnail](chapter_12_specification_to_callable_tool_thumbnail.png)

## Structural Reveal

Callability is produced by preserved contracts across distinct architecture, framework, package, loader, runtime, and interface boundaries. A name or serialized parameter payload alone does not make an architecture callable.

## Caption

The valid path carries a deterministic architecture specification through a registered operation, a 381-byte structured JSON package, pre-construction loader validation, selected runtime capabilities, and a request/response boundary. The fixed request $(2,-1,0.5)$ produces exact response $(3.25,-1.5)$, identically after reload. A control changes only the declared input dimension while preserving parameters; validation returns `PARAMETER_SHAPE_MISMATCH` before construction or invocation. The fixture demonstrates contract preservation, not production compatibility, performance, model quality, or full inference.

## Alternative Text

A horizontal chain contains six labeled modules: specification, framework, model package, loader, runtime, and callable. The specification declares version 1.0 and dimensions three to two. The framework registry resolves an affine-row operation. The package is structured JSON with a byte length and shortened digest. The loader parses, validates shape and operation, and constructs only on a pass. The runtime supplies arithmetic and JSON capabilities. The callable accepts and returns vector version one. A valid-package panel reports `PACKAGE_VALID`, two constructions, and identical reload and reinvocation. A callable-exchange panel maps request values 2, negative 1, and 0.5 to response values 3.25 and negative 1.5. A dashed control path leads from the model package to a corrupt package whose declared input dimension changes from three to four while parameters remain unchanged. It ends at a rejection panel labeled `PARAMETER_SHAPE_MISMATCH`, constructed false, invoked false.

## Production Record

- Creator: Terrence J McLaughlin
- Created: August 14, 2026
- Originality: original programmatic composition generated from the verified Chapter 12 probe
- External assets: none
- Typeface: DejaVu Sans
- Palette: locked values from [../VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md)
- Format: SVG, 1200 × 760 view box
- Generator library: Python standard-library `xml.etree.ElementTree`
- Rasterizer: ImageMagick `convert`
- Deterministic SVG SHA-256: `2fbf954ad45a52e2978d8baa64a004a6d90b311ffbdb8b779fba0910b731bec2`

## Required Tests

| Test | Result |
|---|---|
| package byte count, digest prefix, validation result, response, and corrupt control derive from the verified probe | pass |
| SVG regenerates twice with identical SHA-256 | pass |
| SVG parses and declares a 1200 × 760 canvas | pass |
| 1200 × 760 color export is nonblank | pass |
| 1200 × 760 grayscale export preserves module and path distinctions | pass |
| six-stage contract chain and rejection branch remain recognizable at 100 pixels wide | pass |
| title, labels, connectors, panels, and footer do not clip or overlap at full size | pass |
| alternative text and caption communicate the result without relying on color | pass |
| figure explicitly excludes production compatibility, performance, quality, and full inference claims | pass |
| exactly one Chapter 12 visual anchor exists | pass |