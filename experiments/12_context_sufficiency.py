#!/usr/bin/env python3
"""
Experiment 12 — Context Sufficiency Metric
=================================================================================
Core question:
  What is the minimum context k (in tokens) that, when prepended to the
  disassembly of an -O0 function pair, pushes their embedding L2 distance
  past the -O1 "naturally separated" threshold?

Background:
  Experiment 11 showed that at -O0, elaborate nothing (f_nothing) and
  simple something (f_something) have L2 = 6.05 — dangerously close.
  At -O1, the compiler strips the ABI frame, and L2 jumps to 12.66.

  The compiler did the disambiguation work for free. But in real inference,
  we don't always have a compiler. We have context.

  This experiment asks: how much context must we add to the -O0 pair to
  reproduce what -O1 achieved structurally?

Context Sufficiency Index (CSI):
  For a given context type C and budget k tokens:
    1. Prepend C[:k tokens] to each function's disassembly.
    2. Embed both with TinyLlama.
    3. Measure L2(nothing, something).
  
  CSI(C) = min k such that L2 ≥ TARGET_L2 (12.66, the -O1 threshold)

  If CSI is never reached within the budget → "insufficient"

Context types swept:
  1. "name"       — function name as comment:
                    nothing: "// function: f_nothing"
                    something: "// function: f_something"
  2. "return"     — return type annotation:
                    nothing: "// returns: void"
                    something: "// returns: int value 1"
  3. "intent"     — one-sentence description:
                    nothing: "// this function returns immediately without doing anything"
                    something: "// this function returns the integer value 1"
  4. "signature"  — full C signature:
                    nothing: "void f_nothing(void);"
                    something: "int f_something(void);"
  5. "call_site"  — calling context:
                    nothing: "// called as: f_nothing(); (result discarded)"
                    something: "// called as: int x = f_something(); (result used)"

For each type, we build a prefix at token budgets: 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64
We truncate the prefix to exactly k tokens by re-encoding from the tokenizer.

Manifold geometry interpretation:
  The CSI curve is the "navigation cost" of the context atlas.
  - A flat, never-crossing curve: that context type cannot separate these classes.
    It's topologically blind — the manifold folds those labels onto the same chart.
  - An early crossing: high-quality context that steers the embedding out of the
    confusable region quickly. Equivalent to a strong celestial fix — few sightings,
    precise position.
  - The gap between worst and best CSI types: the "quality spread" of the atlas.

Output: experiments/assets/12_context_sufficiency.png
Run:    source environment/intel-travel/bin/activate && python3 experiments/12_context_sufficiency.py
=================================================================================
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

transformers.logging.set_verbosity_error()

# ── Paths ──────────────────────────────────────────────────────────────────────
EXPERIMENT_DIR = Path(__file__).parent
OUT_PNG        = EXPERIMENT_DIR / "assets" / "12_context_sufficiency.png"
OUT_PNG.parent.mkdir(exist_ok=True)

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_ID   = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE     = "cuda"
DTYPE      = torch.float16
MAX_TOKENS = 512

# ── Threshold from Experiment 11 ───────────────────────────────────────────────
# -O0 baseline (confused):  L2 = 6.05
# -O1 threshold (separated): L2 = 12.66  ← we aim to reproduce via context
TARGET_L2  = 12.66
BASELINE_L2 = 6.05

# ── Token budgets to sweep ─────────────────────────────────────────────────────
TOKEN_BUDGETS = [0, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64]

# ── C source (bare -O0 disassembly reproduced at runtime) ─────────────────────
C_NOTHING = """\
void f_nothing(void) {
}
"""

C_SOMETHING = """\
int f_something(void) {
    return 1;
}
"""

# ── Context prefixes (full text — will be truncated to k tokens) ───────────────
CONTEXT_TYPES = {
    "name": {
        "nothing":   "// function: f_nothing",
        "something": "// function: f_something",
    },
    "return": {
        "nothing":   "// returns: void (no return value)",
        "something": "// returns: int value 1",
    },
    "intent": {
        "nothing":   "// this function returns immediately without doing anything",
        "something": "// this function returns the integer value 1",
    },
    "signature": {
        "nothing":   "void f_nothing(void);",
        "something": "int f_something(void);",
    },
    "call_site": {
        "nothing":   "// called as: f_nothing(); result discarded, side-effect only",
        "something": "// called as: int x = f_something(); result stored and used",
    },
}

# ── Compilation & disassembly ──────────────────────────────────────────────────

def compile_and_disassemble(source: str, func_name: str, opt: str = "-O0") -> str:
    """Compile C snippet, return objdump block for named function."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "fn.c")
        obj = os.path.join(tmpdir, "fn.o")
        with open(src, "w") as f:
            f.write(source)
        r = subprocess.run(
            ["gcc", opt, "-c", "-o", obj, src],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            return f"; gcc error:\n; {r.stderr.strip()}"
        r2 = subprocess.run(
            ["objdump", "-d", "--no-show-raw-insn", obj],
            capture_output=True, text=True
        )
    lines  = r2.stdout.splitlines()
    block  = []
    inside = False
    for line in lines:
        if re.search(rf"<{func_name}>:", line):
            inside = True
        if inside:
            block.append(line)
            if inside and len(block) > 2 and line.strip() == "" :
                break
    return "\n".join(block) if block else r2.stdout[:800]


# ── Embedding extraction ───────────────────────────────────────────────────────

def embed(text: str, tokenizer, model) -> np.ndarray:
    """
    Extract mean-pooled last hidden state from TinyLlama.
    Truncates input to MAX_TOKENS.
    """
    enc = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_TOKENS,
    ).to(DEVICE)
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hidden = out.hidden_states[-1]           # (1, seq_len, 2048)
    vec = hidden[0].mean(dim=0).float().cpu().numpy()
    return vec


def l2(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# ── Token-truncate a prefix to exactly k tokens ───────────────────────────────

def truncate_to_k_tokens(text: str, k: int, tokenizer) -> str:
    """Re-encode text and decode only the first k tokens."""
    if k == 0:
        return ""
    ids = tokenizer.encode(text, add_special_tokens=False)
    ids = ids[:k]
    return tokenizer.decode(ids, skip_special_tokens=True)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Experiment 12 — Context Sufficiency Metric")
    print("=" * 70)

    # ── Load model ─────────────────────────────────────────────────────────────
    print(f"\nLoading {MODEL_ID} …")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=DTYPE,
        device_map=DEVICE,
        attn_implementation="eager",
    )
    model.eval()
    print("Model ready.\n")

    # ── Compile -O0 baselines ──────────────────────────────────────────────────
    print("Compiling -O0 baselines …")
    asm_nothing   = compile_and_disassemble(C_NOTHING,   "f_nothing",   "-O0")
    asm_something = compile_and_disassemble(C_SOMETHING, "f_something", "-O0")

    print("\nf_nothing   (-O0):")
    for ln in asm_nothing.splitlines():
        print(f"  {ln}")
    print("\nf_something (-O0):")
    for ln in asm_something.splitlines():
        print(f"  {ln}")

    # ── Embed raw -O0 (k=0 baseline) ──────────────────────────────────────────
    print("\nEmbedding raw -O0 pair (no context) …")
    e_nothing_raw   = embed(asm_nothing,   tokenizer, model)
    e_something_raw = embed(asm_something, tokenizer, model)
    raw_l2 = l2(e_nothing_raw, e_something_raw)
    print(f"  Raw -O0 L2 = {raw_l2:.3f}  (experiment 11 reference: {BASELINE_L2:.3f})")

    # ── Sweep context types × token budgets ────────────────────────────────────
    print(f"\nSweeping {len(CONTEXT_TYPES)} context types × {len(TOKEN_BUDGETS)} token budgets …")
    print(f"Target L2 = {TARGET_L2:.2f}  (the -O1 threshold from experiment 11)\n")

    results = {}   # {ctx_type: [(k, l2_val), ...]}
    csi     = {}   # {ctx_type: minimum k that crossed threshold, or None}

    for ctx_type, prefixes in CONTEXT_TYPES.items():
        print(f"  Context type: '{ctx_type}'")
        prefix_n = prefixes["nothing"]
        prefix_s = prefixes["something"]

        curve   = []
        crossed = None

        for k in TOKEN_BUDGETS:
            pfx_n = truncate_to_k_tokens(prefix_n, k, tokenizer)
            pfx_s = truncate_to_k_tokens(prefix_s, k, tokenizer)

            text_n = (pfx_n + "\n" + asm_nothing).strip()   if pfx_n else asm_nothing
            text_s = (pfx_s + "\n" + asm_something).strip() if pfx_s else asm_something

            en = embed(text_n, tokenizer, model)
            es = embed(text_s, tokenizer, model)
            d  = l2(en, es)
            curve.append((k, d))

            if crossed is None and d >= TARGET_L2:
                crossed = k

            print(f"    k={k:3d}  L2={d:.3f}{'  ← CROSSED' if k == crossed else ''}")

        results[ctx_type] = curve
        csi[ctx_type]     = crossed
        print(f"  CSI('{ctx_type}') = {crossed if crossed is not None else 'never'}\n")

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("Context Sufficiency Index (CSI) summary")
    print("  (minimum tokens to reach -O1 L2 threshold = {:.2f})".format(TARGET_L2))
    print("=" * 70)
    sorted_csi = sorted(csi.items(), key=lambda x: x[1] if x[1] is not None else 9999)
    for ctx_type, k in sorted_csi:
        bar = "█" * (k // 2 if k else 0) if k is not None else "──── never"
        label = f"k={k:3d}  {bar}" if k is not None else "       (never crossed)"
        print(f"  {ctx_type:12s}  {label}")

    # ── Plot ───────────────────────────────────────────────────────────────────
    print(f"\nGenerating plot → {OUT_PNG}")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor("#0d1117")
    for ax in axes:
        ax.set_facecolor("#161b22")
        for spine in ax.spines.values():
            spine.set_color("#30363d")

    COLORS = {
        "name":      "#58a6ff",
        "return":    "#3fb950",
        "intent":    "#d2a8ff",
        "signature": "#ffa657",
        "call_site": "#ff7b72",
    }

    # Panel 1: L2 curves vs token budget
    ax = axes[0]
    for ctx_type, curve in results.items():
        ks  = [c[0] for c in curve]
        l2s = [c[1] for c in curve]
        ax.plot(ks, l2s, "o-", color=COLORS[ctx_type],
                linewidth=2, markersize=5, label=ctx_type)

    ax.axhline(TARGET_L2,  color="#f0f6fc", linewidth=1.5, linestyle="--",
               alpha=0.8, label=f"-O1 threshold ({TARGET_L2:.2f})")
    ax.axhline(BASELINE_L2, color="#8b949e", linewidth=1.0, linestyle=":",
               alpha=0.7, label=f"-O0 raw ({BASELINE_L2:.2f})")

    ax.set_xlabel("Context token budget  k", color="#8b949e", fontsize=11)
    ax.set_ylabel("L2 distance  (nothing ↔ something)", color="#8b949e", fontsize=11)
    ax.set_title("Context Sufficiency Curves", color="#f0f6fc", fontsize=13, pad=12)
    ax.tick_params(colors="#8b949e")
    ax.legend(fontsize=9, facecolor="#161b22", edgecolor="#30363d",
              labelcolor="#c9d1d9")
    ax.set_xlim(left=-1)
    ax.set_ylim(bottom=0)

    # Panel 2: CSI bar chart
    ax2 = axes[1]
    ctx_order = [ct for ct, _ in sorted_csi]
    csi_vals  = [csi[ct] if csi[ct] is not None else max(TOKEN_BUDGETS) * 1.4
                 for ct in ctx_order]
    bar_colors = [COLORS[ct] for ct in ctx_order]
    y_pos = np.arange(len(ctx_order))

    bars = ax2.barh(y_pos, csi_vals, color=bar_colors, height=0.5, alpha=0.85)

    # Mark "never" bars differently
    for i, (ct, k) in enumerate(sorted_csi):
        if k is None:
            bars[i].set_hatch("///")
            bars[i].set_alpha(0.3)
            ax2.text(max(TOKEN_BUDGETS) * 1.45, y_pos[i], "never",
                     va="center", ha="right", color="#8b949e", fontsize=9)
        else:
            ax2.text(csi_vals[i] + 0.5, y_pos[i], f"k={k}",
                     va="center", ha="left", color="#f0f6fc", fontsize=9)

    ax2.axvline(TARGET_L2 * 0, color="#f0f6fc", linewidth=0)   # invisible anchor
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(ctx_order, color="#c9d1d9", fontsize=10)
    ax2.set_xlabel("Tokens to sufficiency  (CSI)", color="#8b949e", fontsize=11)
    ax2.set_title("Context Sufficiency Index", color="#f0f6fc", fontsize=13, pad=12)
    ax2.tick_params(colors="#8b949e")
    ax2.invert_yaxis()

    # Annotation box
    best_type = sorted_csi[0][0] if sorted_csi[0][1] is not None else "none"
    best_k    = sorted_csi[0][1]
    anno_text = (
        f"Target: L2 ≥ {TARGET_L2:.2f}\n"
        f"(compiler -O1 threshold)\n\n"
        f"Best CSI: '{best_type}'\n"
        f"at k = {best_k} tokens" if best_k is not None
        else f"No context type reached\nthe threshold within budget"
    )
    ax2.text(0.97, 0.04, anno_text,
             transform=ax2.transAxes,
             ha="right", va="bottom",
             fontsize=9, color="#c9d1d9",
             bbox=dict(facecolor="#21262d", edgecolor="#30363d",
                       boxstyle="round,pad=0.5"))

    plt.suptitle(
        "Experiment 12 — Context Sufficiency Metric\n"
        "Minimum context to reproduce compiler -O1 separation in embedding space",
        color="#f0f6fc", fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"Plot saved → {OUT_PNG}")

    # ── Final interpretation ───────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print(f"  -O0 raw L2:         {raw_l2:.3f}  (confused — ABI frames too similar)")
    print(f"  -O1 target L2:      {TARGET_L2:.3f}  (separated — compiler did the work)")
    print()

    reached = [(ct, k) for ct, k in sorted_csi if k is not None]
    if reached:
        best_type, best_k = reached[0]
        print(f"  Fastest separation: '{best_type}' context at k={best_k} tokens")
        print()
        print("  Reading the atlas:")
        for ct, k in sorted_csi:
            if k is not None:
                ratio = k / best_k if best_k > 0 else 1.0
                print(f"    {ct:12s}  k={k:3d}  ({ratio:.1f}× best)")
            else:
                print(f"    {ct:12s}  never reached (manifold fold — type is topologically blind)")
    else:
        print("  No context type crossed the threshold within the token budget.")
        print("  Interpretation: the -O0 ABI frame noise dominates all short labels.")
        print("  The manifold has folded elaborate-nothing onto simple-something")
        print("  so deeply that short context cannot navigate out of that basin.")

    print()
    print("  Thesis:")
    print("    The CSI is the 'chart correction cost' — the navigational effort")
    print("    required to steer the embedding out of the confusion basin created")
    print("    by structural similarity at -O0.")
    print("    The compiler buys this for free by stripping the ABI frame.")
    print("    Context must pay the same cost in tokens.")
    print("=" * 70)


if __name__ == "__main__":
    main()
