# Book Two — Visual Language

**Status:** Locked August 12, 2026

Book Two is a visual system, not a manuscript decorated with pictures. Every visual must make an otherwise invisible structure inspectable and inherit the architectural language established by the cover.

## Visual Forms

### Structural diagrams

Use for architectures, dependencies, flows, interfaces, and module relationships.

### Execution traces

Use for attention patterns, token flows, inference steps, residual pathways, and memory behavior.

### Geometric plots

Use for embeddings, learned spaces, tensor slices, and optimization trajectories.

### Historical images

Use rarely, and only when provenance or conceptual origin is essential. Record the creator, source, license, and required attribution before publication. Historical images do not satisfy the chapter visual-anchor contract because each anchor must be original.

### Pictographs

Use a small recurring vocabulary for memory, constraint, transformation, flow, representation, and geometry. These symbols function as reusable glyphs, not standalone decoration.

## Production Style

The cover artwork is the production source of truth.

| Token | Value | Use |
|---|---|---|
| field | `#f7f7f3` | page and figure background |
| ink | `#141719` | structural lines, labels, and boundaries |
| representation | `#efd5d5` | inputs, outputs, tokens, and encoded forms |
| operation | `#efdcae` | attention and active transformation |
| constraint | `#efefb7` | normalization, limits, and enforced conditions |
| computation | `#b9ddea` | feed-forward work and numerical machinery |

Use flat color only. Do not use gradients, glow, shadows, ornamental shading, or three-dimensional effects. Color identifies function and must remain distinguishable in grayscale.

Use DejaVu Sans with `0` letter spacing. Module names are uppercase; flows and annotations are lowercase. Labels use a consistent optical size within each figure.

Use one consistent structural stroke weight within a figure. Use minimal curvature unless geometry or routing requires it. Arrows indicate flow, boxes indicate modules, circles indicate geometric points, dashed lines indicate constraints, and double lines indicate enforced boundaries.

## Pictograph Vocabulary

| Concept | Glyph construction |
|---|---|
| memory | three aligned storage cells with one retained mark |
| constraint | a dashed boundary crossing a path |
| transformation | an input shape, operator box, and changed output shape |
| flow | a directed line with one arrowhead |
| representation | a labeled object paired with a numerical cell row |
| geometry | three points joined by coordinate axes or distance lines |

The glyph construction remains stable across chapters. Context may change labels but not the underlying symbol.

## Chapter Contract

Each chapter includes exactly one original visual anchor. The canonical assignment is [VISUAL_MANIFEST.md](VISUAL_MANIFEST.md).

The anchor must:

- reveal something invisible
- use the book's visual grammar
- be pedagogically essential
- extend the cover's architectural thesis
- belong specifically to its chapter

The anchor must not:

- use generic AI imagery
- serve as decoration
- duplicate another chapter's reveal
- act as a placeholder
- absorb a diagram whose explanatory work belongs elsewhere

Supporting visual notation inside code listings, tables, equations, or exercises does not count as an additional anchor. Any proposed second figure must be integrated into the anchor as a labeled panel or omitted.

## Production Tests

Every anchor must pass these checks before publication:

1. **Structural reveal:** its caption can name the invisible relationship made visible.
2. **Chapter ownership:** removing it creates a specific explanatory loss in that chapter.
3. **Thumbnail:** its primary structure remains recognizable at approximately 100 pixels wide.
4. **Grayscale:** function remains legible without color.
5. **Accessibility:** labels, caption, and alternative text communicate the figure's purpose without relying on color alone.
6. **Originality:** source files and authorship are recorded in the production package.
