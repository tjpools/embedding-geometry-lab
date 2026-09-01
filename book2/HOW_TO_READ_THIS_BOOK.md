
# How to Read This Book

This book follows three journeys that developed at different rates and solved different problems: the conceptual lineage of artificial intelligence, the mathematics that made learning expressible and trainable, and the programming systems that made those ideas executable. They meet in the transformer, but meeting is not merging - the book preserves each lineage's distinct contribution rather than collapsing them into one vocabulary.

Sixteen chapters are organized into four parts. Part I builds shared structural vocabulary. Part II adds learning and scale. Part III assembles attention into architecture. Part IV brings the three journeys to one executable object and tests its measured limits. Each chapter closes with a probe - executable where appropriate, a worked derivation or primary source otherwise - so that a claim is never left standing on assertion alone.

Rust supplies the organizing flavor for the programming journey, because ownership, borrowing, traits, modules, and compilation keep architectural constraints visible. Rust is not literally a transformer, and attention is not literally borrowing; the comparison is methodological, not an identity claim.

Beside the narrative sits a second, terser layer: `man/`, a lookup reference in the Unix man-page tradition, one page per operation - `attention`, `softmax`, `gradient-descent`, `transformer-block`, and others. A man page does not teach; it states what an operation does, what it does not do, and where its evidence lives. Read it the way you would reach for a manual page mid-task: not to be taught again, but to confirm a contract you already half-remember. Start with `man/man.md` if you want the convention explained before the components.

You do not need to master every chapter before moving to the next. You need to keep enough of each part's handoff in view that later chapters can build on it without re-teaching it. Where a chapter reaches a boundary - what its evidence does not establish - it says so explicitly. Those boundaries are not evasions. They are where this book stops and Book Three's philosophical inquiry begins.
