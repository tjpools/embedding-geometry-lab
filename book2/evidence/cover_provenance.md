# Book Two — Cover Provenance

**Status:** established August 31, 2026, closing the [BOOK_COVER.md](../BOOK_COVER.md) Production Rule gap.

## Production Rule Requirement

> The supplied diagram is a reference for structure, not automatically a publication asset. Before any external image is reproduced, record its creator, source, license, and required attribution.

## What Was Produced

`cover_front.svg`, `cover_front.png`, `cover_front_thumbnail.png`, and `cover_kindle.jpg` are original vector/raster artwork created for this book. No external image file was copied, traced, or reproduced. The SVG source is authored directly in this repository and is credited to Terrence J. McLaughlin, consistent with every chapter visual anchor in [visuals/](../visuals/).

## What Was Referenced

The cover's component layout — encoder stack, decoder stack, input/output embeddings, positional addition, attention, add-and-norm, feed-forward, and output probabilities, with cross-attention bridging encoder to decoder — follows the encoder-decoder Transformer architecture defined in Chapter 11's primary source:

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin, "Attention Is All You Need," *Advances in Neural Information Processing Systems 30*, 2017. https://arxiv.org/abs/1706.03762

This is a reference to a published architecture description, not to any single copyrighted illustration. The cover does not reproduce the paper's figure; it is an independently drawn elevation using the book's own visual language (palette, typography, rounded block treatment) defined in [VISUAL_LANGUAGE.md](../VISUAL_LANGUAGE.md). Internal labels are limited to `INPUT`, `ENCODER`, `ATTENTION`, `DECODER`, `MASKED ATTENTION`, `FEED FORWARD`, `ADD + NORM`, `PROBABILITIES`, and `OUTPUT` — component names for a published architecture, not expressive elements copied from any specific diagram.

## Rights Determination

No third-party image rights apply. No attribution line is required on the cover itself beyond the existing author credit. The paper citation above is carried in Chapter 11's source ledger and does not need separate cover-facing attribution, consistent with standard practice for citing a published architecture rather than reproducing copyrighted artwork.

## Gate Closed

This resolves the "rights/provenance" portion of the `release_readiness.md` cover release file gate. The remaining open item for that gate is confirming trim/bleed requirements for a print-format export; the current assets (1600×2560 PNG/JPG) are sized for ebook/Kindle use, not a print cover with spine and bleed.
