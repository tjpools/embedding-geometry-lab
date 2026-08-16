# Chapter 2 Source Ledger — Representation Becomes Numerical

**Status:** Source basis established August 12, 2026  
**Scope:** Text normalization, tokenization choices, vocabulary identifiers, subword units, and index-based vector lookup  
**Chapter brief:** [../chapter_briefs/chapter_02.md](../chapter_briefs/chapter_02.md)

## Source Standard

This ledger grounds the chapter's external technical framing. The toy vocabulary, permutation result, and unknown-token collapse remain grounded separately by [chapter_02_representation_probe.md](chapter_02_representation_probe.md).

Sources are used only for the claims named below. Documentation for a production tokenizer or embedding library does not establish that the chapter's illustrative vector was learned, carries semantic content, or is adequate for any task.

## Sources

### S1 — Unicode Normalization Forms

Ken Whistler, editor, "Unicode Normalization Forms," *Unicode Standard Annex #15*, revision 57, Unicode 17.0.0, July 30, 2025.

- URL: https://www.unicode.org/reports/tr15/tr15-57.html
- Accessed: August 12, 2026
- Authority: Normative annex of the Unicode Standard
- Supports: Canonical and compatibility equivalence; NFC as canonical decomposition followed by canonical composition; normalization as a declared transformation that can preserve or remove particular distinctions depending on the selected form
- Limitation: Unicode normalization does not define token boundaries, vocabulary membership, meaning, or task adequacy. Chapter 2 uses NFC and does not generalize compatibility-normalization behavior to NFC.

### S2 — Python Unicode and String Operations

Python Software Foundation, "`unicodedata` — Unicode Database" and "Built-in Types," Python 3 documentation.

- URLs: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize and https://docs.python.org/3/library/stdtypes.html#string-methods
- Accessed: August 12, 2026
- Authority: Official language and standard-library documentation
- Supports: The exact probe operations: `unicodedata.normalize("NFC", text)`, case folding for caseless matching, removal of leading and trailing whitespace by `str.strip()`, and whitespace-run splitting by `str.split()` without an explicit separator
- Limitation: These APIs document the probe's implementation semantics. They do not establish that case folding or whitespace tokenization is appropriate for every language, tokenizer, or application.

### S3 — Tokenizers Components

Hugging Face, "Components," Tokenizers documentation.

- URL: https://huggingface.co/docs/tokenizers/components
- Accessed: August 12, 2026
- Authority: Official documentation for a production tokenization library
- Supports: Normalizers, pre-tokenizers, models, post-processors, and decoders as configurable stages; multiple splitting policies; WordLevel mapping of input tokens to identifiers; differences among WordLevel, BPE, WordPiece, Unigram, and byte-level approaches
- Limitation: The available components are examples, not a universal pipeline. In particular, unknown-token behavior varies by model and policy, and byte-level tokenization can avoid an unknown token.

### S4 — Subword Units for Rare Words

Rico Sennrich, Barry Haddow, and Alexandra Birch, "Neural Machine Translation of Rare Words with Subword Units," in *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 1715–1725, Berlin, Germany, August 2016.

- DOI: https://doi.org/10.18653/v1/P16-1162
- URL: https://aclanthology.org/P16-1162/
- Accessed: August 12, 2026
- Authority: Primary peer-reviewed research paper
- Supports: Subword segmentation as a practical response to rare and unseen words and as an alternative to treating every complete word as one vocabulary item
- Limitation: The paper concerns neural machine translation and does not establish one uniquely correct segmentation policy or eliminate all representation loss.

### S5 — PyTorch Embedding Lookup

PyTorch Contributors, "Embedding," PyTorch 2.13 documentation.

- URL: https://docs.pytorch.org/docs/2.13/generated/torch.nn.Embedding.html
- Accessed: August 12, 2026
- Authority: Official documentation for a widely used machine-learning library
- Supports: An embedding as a lookup table with weight shape `(num_embeddings, embedding_dim)`; integer input indices selecting corresponding output vectors; the distinction between dictionary size and vector dimension
- Limitation: PyTorch embeddings may be trainable or initialized from supplied weights. The chapter's fixed table demonstrates lookup only and is not evidence of learning or semantic geometry.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Normalization applies a declared equivalence policy before token lookup. | S1, S2, S3 | The probe applies NFC, case folding, and whitespace trimming before splitting; each operation is an explicit policy choice. |
| Token boundaries depend on tokenizer rules. | S2, S3, S4 | Whitespace, punctuation, subword, and byte-level procedures can produce different token sequences from the same source text. |
| A vocabulary identifier is an assigned index. | S3 | In a WordLevel-style mapping, an input token is mapped to an identifier in the declared vocabulary. |
| An integer index can select a vector row. | S5 | A lookup table maps each admitted index to the corresponding fixed-length vector row. |
| Vocabulary design affects rare or unseen input handling. | S3, S4 | Whole-word, subword, and byte-level designs make different coverage and unknown-token tradeoffs. |
| The probe's unknown collapse is policy-specific. | S3 | Under this toy vocabulary's declared fallback, two absent tokens share one identifier and vector; other tokenizer designs need not behave this way. |

## Prohibited Inferences

The sources do not warrant claims that:

- tokenization discovers natural or unique word boundaries
- token identifiers contain intrinsic meaning or ordinal magnitude
- case folding, whitespace splitting, or the toy vocabulary is universally appropriate
- every tokenizer uses an unknown token or collapses unknown inputs identically
- every embedding table is learned
- the chapter's illustrative dense vector is semantic or geometrically meaningful
- preserving a selected lookup vector under consistent renumbering proves task adequacy
- numerical representation preserves every distinction present in source text

## Drafting Requirement

Every sourced technical or historical sentence in Chapter 2 must map to this ledger or trigger an explicit ledger update. The final bibliography must use the verified metadata recorded here.