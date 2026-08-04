# Print Cover Typography Spec

Use this spec when fitting the Scribus cover. It defines hierarchy, case, line breaks, spacing intent, and fallback rules.

## Priority Order

Protect these in order:

1. Title legibility
2. Emblem prominence
3. Subtitle readability
4. Author clarity
5. Back-cover comfort

If a layout compromise is required, make it lower in the order above before touching anything higher.

## Front Cover

### Title

Text:

`Embedding Geometry`

Rules:

- Title case exactly as written
- Keep on two lines only if the chosen face demands it; preferred first attempt is one line
- Do not condense horizontally
- Do not use all caps
- Track very slightly open only if needed for calm, not for effect
- Visually center within the title frame, but bias slightly upward if optical balance demands it

Preferred line-break order:

1. `Embedding Geometry`
2. `Embedding` / `Geometry`

Avoid:

- decorative split treatments
- forced justification
- dramatic tracking

### Subtitle

Approved subtitle:

`A Walkable Introduction to AI Through Building, Testing, and Collaboration`

Short fallback:

`A Walkable Introduction to AI`

Rules:

- Sentence case exactly as written
- Prefer 3 balanced lines for the approved subtitle
- Prefer 2 lines for the short fallback
- Center align
- Keep leading open enough that it does not form a gray block
- Keep subtitle clearly subordinate to the title
- Use the short fallback only if the approved subtitle cannot fit without looking compressed or visually noisy

Preferred line-break order for approved subtitle:

1. `A Walkable Introduction to AI`
2. `Through Building, Testing,`
3. `and Collaboration`

Acceptable alternate:

1. `A Walkable Introduction`
2. `to AI Through Building,`
3. `Testing, and Collaboration`

Preferred line-break order for short fallback:

1. `A Walkable Introduction to`
2. `Reasoning and Structure`

### Author

Text:

`Terrence J McLaughlin`

Rules:

- Title case exactly as written
- One line only
- Center align
- Lighter visual weight than the title
- Slight tracking is acceptable if the line feels cramped
- Do not style it as a slogan

## Spine

Text:

- `Embedding Geometry`
- `Terrence J McLaughlin`

Rules:

- Keep the spine extremely conservative; this is a narrow spine
- Title first, author second
- Rotate as already specified in the Scribus workflow
- Use one text frame only if it fits cleanly; use two separate lines only if centering remains stable
- Do not include the subtitle on the spine
- If the spine feels crowded, reduce author emphasis before reducing title legibility

## Back Cover

### Header Question

Text:

`AI is not a mystery. It's a tool you can touch.`

Rules:

- Set apart from body text
- Keep as a compact block, not a stretched banner
- Prefer 2 to 4 lines depending on type size
- Avoid widows such as a final line containing only `see?`
- Maintain a visible pause below the header before the main copy begins

Preferred line-break order:

1. `AI is not a mystery.`
2. `It's a tool you can touch.`

### Body Copy

Rules:

- Left align
- Ragged right
- Do not justify
- Aim for comfortable paperback reading texture, not manifesto density
- Preserve paragraph break between the two body paragraphs
- Keep line length moderate within the established frame
- If fit becomes tight, reduce point size slightly before reducing line spacing aggressively

### Author Line

Text:

`Terrence J McLaughlin writes about reasoning, tools, and the changing structure of human-machine work.`

Rules:

- Keep visually separate from body copy
- Smaller than the header, at or slightly smaller than body size
- Do not italicize unless the rest of the back cover is extremely plain and needs one gentle register shift

## Style Direction

Choose typography that feels:

- serious
- lucid
- modern without startup gloss
- literary enough for a book
- technical enough for the subject

Avoid typography that feels:

- glossy tech branding
- futuristic gimmickry
- academic bureaucracy
- compressed or overdesigned

## Fitting Rules

Use this sequence when resolving crowding:

1. Adjust line breaks
2. Adjust tracking minimally
3. Adjust point size slightly
4. Use the short subtitle fallback

Do not:

- condense the title font
- reduce leading until the subtitle clumps
- shrink the emblem to save weak typography

## Final Check

The front cover should read as:

1. a serious title
2. a clean symbolic action
3. a legible promise of scope
4. a calm author credit

If any typographic move makes the cover feel louder than the idea, reject it.