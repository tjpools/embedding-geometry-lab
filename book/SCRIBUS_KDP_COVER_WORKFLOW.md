# Scribus KDP Cover Workflow

This document turns the current manuscript into a concrete Scribus workflow for a KDP paperback cover.

## 1. Scribus Checklist

Use this sequence in Scribus. Do not improvise the document geometry before KDP gives you a template.

1. Freeze the interior first.
   - Current interior artifact: `embedding-geometry-6x9.pdf`
   - Current PDF page count: 161 pages
   - KDP may round the print count up to an even number, so confirm the final calculator output before locking the spine width.

2. Download the KDP paperback cover template.
   - Inputs to KDP cover calculator: trim size `6 x 9 in`, black-and-white interior, selected paper color, bleed cover.
   - Use the exact page count KDP reports, not an estimate.

3. Create the Scribus document from the template dimensions.
   - One page only
   - Units: inches
   - Turn on bleed and guides
   - Import the KDP template as a bottom reference layer

4. Create three working layers.
   - `template-lock`
   - `art`
   - `type`

5. Lock the template layer.
   - Never design directly on top of the imported KDP template.
   - Keep all guides visible while placing art and text.

6. Build the background first.
   - Extend any full-bleed color or image to the outer bleed edge.
   - Do not stop backgrounds at the trim line.

7. Place the front-cover art.
   - The current concept is the stickman-lifting-rock glyph in `cover.png`.
   - Treat that image as source concept art, not final print art.
   - The current file is `1024 x 1536`, which is only about `171 DPI` at `6 x 9 in`; it is not sufficient for a final print front cover.

8. Build title and author text with frames, not manual positioning.
   - Front cover: title, subtitle, author
   - Spine: title and author only
   - Avoid putting the subtitle on the spine; the spine is too narrow for it.

9. Reserve the back-cover barcode zone.
   - If KDP supplies the barcode, leave the lower-right back cover clear.
   - Safe placeholder: `2.0 x 1.2 in` white box in the lower-right back panel.

10. Keep live text inside the safe area.
   - Minimum distance from outside cover edge: `0.25 in`
   - Keep important text and symbols farther in when possible.

11. Flatten export complexity before final PDF.
   - Avoid live transparency where possible.
   - Convert special effects to simpler artwork before export.

12. Export a print PDF and proof it at 100%.
   - Confirm trim, spine centering, barcode clearance, and font embedding.
   - Run the PDF through KDP preview before finalizing.

## 2. Book-Specific Production Spec

The planning estimates are now superseded by the actual KDP template files:

- `PAPERBACK_6.000x9.000_161_BW_CREAM_en_US.pdf`
- `PAPERBACK_6.000x9.000_161_BW_CREAM_en_US.png`

### Current known inputs

- Title: `Embedding Geometry`
- Subtitle: `A Walkable Introduction to Reasoning, Structure, and the Tools That Shape Us`
- Author: `Terrence J McLaughlin`
- Interior trim size: `6 x 9 in`
- Current interior PDF page size: `6 x 9 in`
- Current interior PDF page count: `161`
- Current front-cover concept asset: `cover.png` at `1024 x 1536`

### Exact KDP geometry

The template gives the authoritative production geometry:

- Format: paperback
- Interior: black and white
- Paper: cream
- Trim: `6 x 9 in`
- Final page count: `161`
- Spine width: `0.403 in` (`10.22 mm`)
- Overall spread size: `12.653 x 9.250 in` (`321.37 x 234.95 mm`)
- Template PNG size: `7592 x 5550 px`
- Template resolution: `600 DPI`

These values replace the earlier planning estimates.

### Derived cover zones

Using the KDP template numbers, the spread breaks down as follows:

- Left bleed: `0.125 in`
- Back cover trim width: `6.000 in`
- Spine trim width: `0.403 in`
- Front cover trim width: `6.000 in`
- Right bleed: `0.125 in`
- Top bleed: `0.125 in`
- Bottom bleed: `0.125 in`

Full-width check:

- `0.125 + 6.000 + 0.403 + 6.000 + 0.125 = 12.653 in`

### Spine guidance

- KDP prints spine text on books over 79 pages, so this book qualifies.
- A `0.403 in` spine is still narrow.
- Use only:
  - `Embedding Geometry`
  - `Terrence J McLaughlin`
- Do not attempt to place the full subtitle on the spine.

### Back-cover constraints

- Keep all non-bleed text at least `0.25 in` from the outer edge.
- Keep critical text away from the spine fold as well.
- Leave the lower-right area clear for the barcode unless you are supplying your own.
- If KDP supplies the barcode, design around a `2.0 x 1.2 in` white box.

The actual template confirms the barcode exclusion box is exactly `2.000 x 1.200 in`.

### Asset requirements

- Minimum image resolution: `300 DPI`
- Recommended practical maximum: `600 DPI`
- Front cover at `6 x 9 in` should be at least `1800 x 2700`
- Full spread at `12.653 x 9.250 in` should be at least about `3796 x 2775` at `300 DPI`
- Full spread at template resolution is `7592 x 5550` at `600 DPI`
- Current `cover.png` is below final print resolution and should be redrawn, upscaled carefully, or recreated as vector art.

### Scribus document setup

- Document size: `12.653 x 9.250 in`
- Bleeds: `0.125 in` on all outer sides
- One-page spread PDF export
- Fonts embedded
- No crop marks
- No registration marks
- No visible template text
- No annotations or form objects

### Scribus coordinate map

Use the full spread with origin at the top-left corner of the document.

Horizontal guide positions:

- `0.000 in`: outer left bleed edge
- `0.125 in`: back-cover trim start
- `6.125 in`: back-cover trim end / spine start
- `6.528 in`: spine end / front-cover trim start
- `12.528 in`: front-cover trim end
- `12.653 in`: outer right bleed edge

Vertical guide positions:

- `0.000 in`: outer top bleed edge
- `0.125 in`: top trim line
- `9.125 in`: bottom trim line
- `9.250 in`: outer bottom bleed edge

Live-area guide positions:

- top safe line: `0.375 in`
- bottom safe line: `8.875 in`
- back-cover safe left: `0.375 in`
- back-cover safe right: `5.875 in`
- front-cover safe left: `6.778 in`
- front-cover safe right: `12.278 in`

Spine-safe guide positions:

- left spine-safe edge: `6.188 in`
- right spine-safe edge: `6.466 in`

These spine-safe edges apply a `0.0625 in` inset from each spine fold.

### Exact placement rectangles

Back-cover trim panel:

- `x = 0.125 in`
- `y = 0.125 in`
- `w = 6.000 in`
- `h = 9.000 in`

Back-cover live area:

- `x = 0.375 in`
- `y = 0.375 in`
- `w = 5.500 in`
- `h = 8.500 in`

Barcode exclusion box:

- `x = 3.875 in`
- `y = 7.675 in`
- `w = 2.000 in`
- `h = 1.200 in`

Spine trim panel:

- `x = 6.125 in`
- `y = 0.125 in`
- `w = 0.403 in`
- `h = 9.000 in`

Spine text safe box:

- `x = 6.188 in`
- `y = 0.375 in`
- `w = 0.278 in`
- `h = 8.500 in`

Front-cover trim panel:

- `x = 6.528 in`
- `y = 0.125 in`
- `w = 6.000 in`
- `h = 9.000 in`

Front-cover live area:

- `x = 6.778 in`
- `y = 0.375 in`
- `w = 5.500 in`
- `h = 8.500 in`

### Recommended frame plan

This is the first sensible placement pass for Scribus. Adjust aesthetically after the first proof, but start here.

Front-cover emblem rectangle:

- `x = 7.550 in`
- `y = 2.000 in`
- `w = 3.950 in`
- `h = 3.950 in`

Front-cover title frame:

- `x = 7.050 in`
- `y = 0.900 in`
- `w = 4.950 in`
- `h = 0.950 in`

Front-cover subtitle frame:

- `x = 7.050 in`
- `y = 5.950 in`
- `w = 4.950 in`
- `h = 1.150 in`

Front-cover author frame:

- `x = 7.050 in`
- `y = 7.550 in`
- `w = 4.950 in`
- `h = 0.500 in`

Spine title frame:

- center on the spine-safe box
- rotate `90 degrees`
- keep cap height conservative; this spine does not support aggressive sizing

Back-cover copy block:

- `x = 0.700 in`
- `y = 1.100 in`
- `w = 4.650 in`
- `h = 4.750 in`

Back-cover author line block:

- `x = 0.700 in`
- `y = 6.200 in`
- `w = 4.650 in`
- `h = 0.700 in`

Leave the barcode box untouched and let background art flow behind it only if that area stays visually tolerant of the white barcode patch.

### Scribus build sequence

Scribus is not available in this workspace, so the document has to be built manually in the Scribus GUI. Use this exact sequence.

1. Create a new custom document.
   - Units: `inches`
   - Width: `12.653 in`
   - Height: `9.250 in`
   - Facing pages: off
   - Page count: `1`
   - Margins: `0`
   - Bleeds: `0.125 in` on all sides

2. Create four layers in this order.
   - `template-lock`
   - `guides`
   - `art`
   - `type`

3. Place the KDP PNG on `template-lock`.
   - File: `PAPERBACK_6.000x9.000_161_BW_CREAM_en_US.png`
   - Position: `x = 0.000 in`, `y = 0.000 in`
   - Size: `w = 12.653 in`, `h = 9.250 in`
   - Lock the layer after placement

4. Add vertical guides.
   - `0.000 in`
   - `0.125 in`
   - `0.375 in`
   - `5.875 in`
   - `6.125 in`
   - `6.188 in`
   - `6.466 in`
   - `6.528 in`
   - `6.778 in`
   - `12.278 in`
   - `12.528 in`
   - `12.653 in`

5. Add horizontal guides.
   - `0.000 in`
   - `0.125 in`
   - `0.375 in`
   - `8.875 in`
   - `9.125 in`
   - `9.250 in`

6. Create temporary setup rectangles if you want visual scaffolding.
   - Back-cover live area: `x = 0.375`, `y = 0.375`, `w = 5.500`, `h = 8.500`
   - Barcode exclusion: `x = 3.875`, `y = 7.675`, `w = 2.000`, `h = 1.200`
   - Spine safe box: `x = 6.188`, `y = 0.375`, `w = 0.278`, `h = 8.500`
   - Front-cover live area: `x = 6.778`, `y = 0.375`, `w = 5.500`, `h = 8.500`

7. Create the front-cover frame skeleton.
   - Emblem rectangle on `art`: `x = 7.550`, `y = 2.000`, `w = 3.950`, `h = 3.950`
   - Title frame on `type`: `x = 7.050`, `y = 0.900`, `w = 4.950`, `h = 0.950`
   - Subtitle frame on `type`: `x = 7.050`, `y = 5.950`, `w = 4.950`, `h = 1.150`
   - Author frame on `type`: `x = 7.050`, `y = 7.550`, `w = 4.950`, `h = 0.500`

8. Create the spine text frame.
   - Position: `x = 6.188`, `y = 0.375`
   - Size: `w = 0.278`, `h = 8.500`
   - Rotation: `90 degrees`
   - Content target: title and author only

9. Create the back-cover text frames.
   - Copy block: `x = 0.700`, `y = 1.100`, `w = 4.650`, `h = 4.750`
   - Author line: `x = 0.700`, `y = 6.200`, `w = 4.650`, `h = 0.700`

10. Save the empty layout before styling.
   - Suggested filename: `embedding-geometry-cover.sla`

At that point the Scribus document is structurally complete. The next pass is content placement: vector emblem first, front-cover hierarchy second, spine fit third, back-cover copy last.

### Windows working-folder convention

If you build this in Windows Scribus, keep the file layout stable so linked assets do not break.

Recommended working folder:

- `C:\Users\tmcla\Documents\EmbeddingGeometryCoverWork`

Recommended structure:

- `templates/`
- `assets/`
- `exports/`
- `notes/`
- `scribus/`

Recommended Scribus filename:

- `scribus/embedding-geometry-cover-v01.sla`

Recommended export filenames:

- `exports/embedding-geometry-cover-proof-v01.pdf`
- `exports/embedding-geometry-cover-kdp-v01.pdf`

Recommended asset naming:

- keep the KDP template filenames unchanged
- store the final emblem as `assets/embedding-geometry-emblem-v01.svg`
- if you create alternates, use `v02`, `v03`, and so on

Do not move linked template or SVG files after the `.sla` is created unless you are prepared to relink them inside Scribus.

### Exact text for the first layout pass

Use this content for the initial fitted frames.

Front-cover title:

`Embedding Geometry`

Front-cover subtitle:

`A Walkable Introduction to Reasoning, Structure, and the Tools That Shape Us`

Front-cover author:

`Terrence J McLaughlin`

Spine text:

`Embedding Geometry`

Spine author:

`Terrence J McLaughlin`

Back-cover copy, preferred first pass:

`What if the most important thing about AI is not whether it is a mind, but what it lets us see?`

`Embedding Geometry follows a direct encounter between human judgment and machine language as it unfolded inside the working realities of 2026. Rather than argue from hype or fear, Terrence J McLaughlin tracks what happens when a transformer model becomes usable enough to expose its real strengths, limits, and strange forms of collaboration.`

`The result is a book about tools, reasoning, authorship, and the structures that shape thought. Clear-eyed and exploratory, it offers a walkable path into the deeper geometry beneath the AI slogan.`

Back-cover author line:

`Terrence J McLaughlin writes about reasoning, tools, and the changing structure of human-machine work.`

This is the best first-pass text because it is tighter than version A and more likely to fit the back-cover frame cleanly.

### SVG construction plan

Build the first emblem as a simple vector drawing with filled shapes only. The goal is a stable `v01`, not a perfect final mark.

Artboard:

- `1000 x 1000` units
- transparent background

Color palette:

- figure: `#111111`
- rock: `#111111`
- gold: `#F2C94C`

Primary shape plan:

1. Head
   - circle centered near `x = 380`, `y = 355`
   - radius about `42`

2. Torso
   - slightly forward-leaning tapered rectangle or narrow polygon
   - approximate bounds: `x = 350..430`, `y = 395..610`

3. Rear leg
   - heavy diagonal bar from lower torso toward `x = 280`, `y = 790`

4. Front leg
   - bent diagonal bar from lower torso toward `x = 470`, `y = 785`

5. Rear arm
   - diagonal bar from upper torso toward underside of rock near `x = 360`, `y = 455`

6. Front arm
   - stronger diagonal bar from upper torso toward rock edge near `x = 505`, `y = 420`

7. Rock
   - irregular polygon centered around `x = 560`, `y = 330`
   - approximate overall size: `420` wide by `250` high
   - underside should leave a clear reveal gap toward the lower-left edge

8. Gold
   - rounded rectangle or faceted polygon centered near `x = 500`, `y = 565`
   - approximate size: `180` wide by `110` high

Geometric rules:

- keep all figure parts visually thick enough to survive thumbnail reduction
- avoid strokes if possible; use filled shapes
- use rounded corners where harsh corners make the glyph look brittle
- keep the figure/rock contact points visually obvious
- make the gold shape large enough to read immediately as the point of revelation

Composition rules:

- the figure should occupy roughly the left-middle of the emblem
- the rock should dominate the upper-right quadrant
- the gold should sit below the rock and slightly right of the torso
- preserve a strong triangular sense of force: feet, hands, lifted mass

Export targets:

- `assets/embedding-geometry-emblem-v01.svg`
- optional review PDF: `assets/embedding-geometry-emblem-v01.pdf`

When `v01` exists, place it into the emblem rectangle without further scaling experiments beyond fitting it proportionally inside the `3.950 x 3.950 in` frame.

## 3. Cover Copy Draft

This draft is deliberately tighter than the manuscript description. Back cover copy has to sell orientation, not explain the whole project.

### Front cover

- Title: `Embedding Geometry`
- Subtitle: `A Walkable Introduction to Reasoning, Structure, and the Tools That Shape Us`
- Author: `Terrence J McLaughlin`

### Spine

- `Embedding Geometry`
- `Terrence J McLaughlin`

### Back-cover copy, version A

In 2026, a familiar slogan met a live test.

This book is not a manifesto about artificial intelligence from a distance. It is a grounded account of what became visible when a human being worked directly with a modern transformer system and followed the results carefully enough to separate theater from structure.

What emerged was not an artificial person, but a new kind of working environment: part language, part tool runtime, part reasoning surface. From that encounter, a deeper picture comes into view. Intelligence is not a slogan, software is not neutral, and the shapes we build to think with eventually begin to think through us.

Embedding Geometry is a walkable introduction to reasoning, structure, and the tools that now mediate human judgment.

### Back-cover copy, version B

What if the most important thing about AI is not whether it is a mind, but what it lets us see?

Embedding Geometry follows a direct encounter between human judgment and machine language as it unfolded inside the working realities of 2026. Rather than argue from hype or fear, Terrence J McLaughlin tracks what happens when a transformer model becomes usable enough to expose its real strengths, limits, and strange forms of collaboration.

The result is a book about tools, reasoning, authorship, and the structures that shape thought. Clear-eyed and exploratory, it offers a walkable path into the deeper geometry beneath the AI slogan.

### Short author line options

- `Terrence J McLaughlin writes about reasoning, tools, and the changing structure of human-machine work.`
- `Terrence J McLaughlin documents the practical and philosophical consequences of working directly with modern language models.`

### Visual direction notes

The existing cover concept is strong because it compresses the book's thesis into one readable gesture: effort, lift, revelation.

For the print edition, preserve that symbolic clarity:

- Keep the stickman/rock/gold motif simple.
- Let the title carry the intellectual weight.
- Avoid decorative clutter or glossy tech tropes.
- Prefer a bold, legible composition over intricate detail.
- Use contrast that survives grayscale thumbnail viewing on Amazon.

## 4. Vector Art Brief

The front-cover motif should be rebuilt as a refined vector emblem. The goal is not to reinterpret the concept, but to formalize it into a reusable identity mark that survives print, thumbnail scale, and future editions.

### Core concept

Preserve the original symbolic action exactly:

- a human figure
- lifting a rock
- revealing a gold shape beneath

This is the book's thesis compressed into one gesture: effort, lift, revelation.

### Style direction

Aim for:

- universal glyph, not illustration
- bold silhouette, not detail
- geometric clarity, not sketchiness
- intentional negative space, not accidental gaps
- print-safe contrast, not gradients or effects

The emblem should work on:

- a serious nonfiction cover
- a narrow spine-adjacent composition
- a small Amazon thumbnail
- a future hardcover or digital edition
- slides, web headers, or other reuse contexts

Treat it as a reusable identity mark, not a one-off drawing.

### Figure geometry

The figure should be built from simple geometric primitives:

- circles, arcs, and straight segments
- proportions closer to an ISO-style pictogram than a cartoon
- a slight forward lean to imply effort
- limb angles that clearly show strain and lift
- a clean circular head
- joints implied by geometry rather than explicit markers

Avoid:

- facial features
- clothing
- hair
- fingers
- incidental detail that breaks the glyph abstraction

The figure must read instantly at very small size.

### Rock geometry

The rock should be:

- a single bold mass
- slightly irregular but still geometric
- large enough to imply weight
- positioned so the lift feels physically credible
- open enough underneath to make the reveal legible

Avoid:

- texture
- shading
- cracks
- gradients
- photographic cues

The rock has to read at thumbnail scale.

### Gold geometry

The revealed value should be:

- a simple bright geometric shape
- a rounded rectangle, circle, or clean faceted polygon
- clearly positioned under the lifted rock
- large enough to survive reduction
- flat in treatment, with no texture

It should read as "something valuable revealed," not as a literal nugget.

### Fill strategy

Preferred approach:

- pure silhouette
- filled shapes
- no strokes unless a specific constraint requires them
- figure, rock, and gold distinguished by silhouette and negative space

This is stronger than a stroke-built icon for print and thumbnail use.

### Composition and proportion

Design the emblem inside a square or near-square bounding box so it can be reused as a cover mark or logo.

Recommended proportions:

- figure height about `70-75%` of total emblem height
- rock width about `60-80%` of emblem width
- gold shape about `20-30%` of emblem width
- a slight rock tilt to imply lift and reveal
- negative space between figure and rock should be deliberate and stable

The composition should feel balanced but dynamic.

### Color strategy

For the master vector:

- primary shapes in pure black on transparent background
- gold shape in a flat warm yellow such as `#F2C94C`
- no gradients
- no opacity effects
- no filters or shadows

This keeps the art easy to recolor and safe for KDP print.

### Export requirements

Deliver the vector art in:

- `SVG` as the primary master
- `PDF` for Scribus placement
- `EPS` only if another tool requires it

All artwork should be:

- vector paths only
- free of raster content
- free of embedded images
- free of accidental clipping-mask complexity

### Deliverables

Prepare these variants:

- full emblem: figure, rock, gold
- monochrome version with no gold accent
- pure black silhouette version
- reversed white-on-dark version
- square bounding-box version
- loose version with no bounding box

## 5. Immediate Next Moves

1. Rebuild the front-cover motif as vector art using the brief above.
2. Create a Scribus document at `12.653 x 9.250 in` with `0.125 in` bleeds.
3. Place the KDP PNG on a locked template layer and add guides at the coordinates above.
4. Place the vector motif in the front-cover emblem rectangle and establish the title hierarchy around it.
5. Fit the spine title and author inside the spine-safe box only after the front panel feels balanced.
6. Flow the back-cover copy inside the back-cover copy block and keep the barcode rectangle clear.
7. Export a draft print PDF and inspect it in the KDP previewer before polishing.