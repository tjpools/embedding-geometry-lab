#!/usr/bin/env python3
"""
Experiment 13 — Pure Semantic Geometry
=================================================================================
Core question:
  What is the L2 separation between elaborate-nothing and simple-something
  when the ABI frame is completely absent? No disassembly. No structural noise.
  Context is the entire input.

Experiment 12 showed code-dominated geometry:
  - ABI frame owned ~80% of the mean-pool denominator
  - Context acted as perturbation, peaked at L2=10.96 (intent, k=8)
  - Curves plateaued at prefix exhaustion, not manifold resistance
  - We were measuring: code-dominated geometry + context force

This experiment tests the limit case: context as ground state.
  lim_{k→∞} v(code + k·context) = v(context alone)

Three reference points after this experiment:
  -O0 code only:            L2 = 5.022  (ABI frame dominates, confused)
  exp12 peak (code+context): L2 = 10.96  (context force, denominator wins)
  exp13 context only:        L2 = ?      (pure semantic ceiling)

If exp13 L2 ≥ 12.66 → dilution was the entire barrier. Shallow basin. Metric failure.
                        Enough tokens of any content-carrying context escapes.
If exp13 L2 < 12.66  → genuine semantic proximity. The manifold folds void-nothing
                        and int-something together even without structural noise.
                        The confusion is in the learned representation itself.

Input representations (no disassembly — each is the ENTIRE input):
  Level 0  — type token:     "void"          vs "int"
  Level 1  — return annot:   "// returns: void"  vs "// returns: int value 1"
  Level 2  — signature:      "void f_nothing(void);"  vs "int f_something(void);"
  Level 3  — intent short:   "returns immediately"  vs "returns integer 1"
  Level 4  — intent full:    full one-sentence description
  Level 5  — call site:      "f_nothing(); // result discarded"  vs ...
  Level 6  — prose:          2-sentence natural language description
  Level 7  — prose long:     5-sentence description with type, usage, semantics

Secondary measurements:
  - Same-class baselines at each level (nothing×nothing', something×something')
  - Token count for each input (actual denominator size)
  - Per-token efficiency: L2 / token_count

Goal: locate the semantic ceiling and compare to code-dominated geometry.

Output: experiments/assets/13_pure_semantic_geometry.png
Run:    source environment/intel-travel/bin/activate && python3 experiments/13_pure_semantic_geometry.py
=================================================================================
"""

from pathlib import Path

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

transformers.logging.set_verbosity_error()

# ── Paths ──────────────────────────────────────────────────────────────────────
EXPERIMENT_DIR = Path(__file__).parent
OUT_PNG        = EXPERIMENT_DIR / "assets" / "13_pure_semantic_geometry.png"
OUT_PNG.parent.mkdir(exist_ok=True)

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_ID   = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE     = "cuda"
DTYPE      = torch.float16
MAX_TOKENS = 512

# ── Reference lines from prior experiments ────────────────────────────────────
REF_O0_CODE_ONLY  = 5.022   # exp 12: -O0 disassembly, no context
REF_O1_SEPARATED  = 12.66   # exp 11: -O1 disassembly, compiler stripped frame
REF_EXP12_PEAK    = 10.96   # exp 12: best peak (intent at k=8, code+context)

# ── Representation levels ──────────────────────────────────────────────────────
# Each entry: (level_name, nothing_text, nothing_alt, something_text, something_alt)
# nothing_alt / something_alt are same-class controls for baseline measurement
REPRESENTATIONS = [
    (
        "type token",
        "void",
        "void",           # same-class: identical (measures self-similarity floor)
        "int",
        "int",
    ),
    (
        "return annot",
        "// returns: void",
        "// return type: void",
        "// returns: int value 1",
        "// return type: int, value is 1",
    ),
    (
        "signature",
        "void f_nothing(void);",
        "void g_nothing(void);",
        "int f_something(void);",
        "int g_something(void);",
    ),
    (
        "intent short",
        "returns immediately",
        "exits without doing anything",
        "returns integer 1",
        "returns the value one",
    ),
    (
        "intent full",
        "this function returns immediately without doing anything",
        "this function exits right away and produces no result",
        "this function returns the integer value 1",
        "this function produces the integer result one",
    ),
    (
        "call site",
        "f_nothing(); // result discarded, no side effects",
        "g_nothing(); // discarded, pure no-op",
        "int x = f_something(); // result stored and used",
        "int y = g_something(); // integer result assigned",
    ),
    (
        "prose",
        (
            "f_nothing is a void function that takes no arguments and has no body. "
            "It returns immediately without performing any computation or side effects."
        ),
        (
            "g_nothing accepts no parameters and returns nothing. "
            "The function body is empty and execution returns to the caller immediately."
        ),
        (
            "f_something is a function that takes no arguments and returns the integer value 1. "
            "It always produces the same result and has no side effects."
        ),
        (
            "g_something accepts no parameters and returns the integer value 2. "
            "The return value is a compile-time constant with no side effects."
        ),
    ),
    (
        "prose long",
        (
            "f_nothing is declared with return type void, meaning it produces no value. "
            "It accepts no arguments. The function body contains no statements. "
            "When called, execution enters the function frame and immediately returns. "
            "No registers are modified with computed values. "
            "The only observable effect is the call and return overhead."
        ),
        (
            "g_nothing has return type void and takes no parameters. "
            "Its body is empty. Calling it has no effect on program state. "
            "No computation is performed inside the function. "
            "It is a complete no-operation from a semantic standpoint. "
            "The function exists only as a callable symbol with no payload."
        ),
        (
            "f_something is declared with return type int and takes no arguments. "
            "Its body contains a single return statement: return 1. "
            "Every call to this function produces the integer value 1. "
            "The return value is a constant and requires no computation. "
            "The function is a pure, deterministic, side-effect-free computation."
        ),
        (
            "g_something is a function returning int with no parameters. "
            "Its single statement returns the integer literal 2. "
            "It is a constant function: every invocation produces the same result. "
            "There are no side effects. The result is always the value two. "
            "This function is semantically simple despite having a non-void return type."
        ),
    ),
]


# ── Embedding extraction ───────────────────────────────────────────────────────

def embed(text: str, tokenizer, model) -> tuple[np.ndarray, int]:
    """Return (mean-pooled last hidden state, token count)."""
    enc = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_TOKENS,
    ).to(DEVICE)
    n_tokens = enc["input_ids"].shape[1]
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hidden = out.hidden_states[-1]   # (1, seq_len, 2048)
    vec = hidden[0].mean(dim=0).float().cpu().numpy()
    return vec, n_tokens


def l2(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Experiment 13 — Pure Semantic Geometry")
    print("=" * 70)

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

    print("Reference points from prior experiments:")
    print(f"  -O0 code only (exp 12 baseline): L2 = {REF_O0_CODE_ONLY:.3f}")
    print(f"  exp12 peak (intent k=8):         L2 = {REF_EXP12_PEAK:.3f}")
    print(f"  -O1 compiler separated (exp 11): L2 = {REF_O1_SEPARATED:.3f}")
    print()

    results = []  # list of dicts

    for level_name, n_text, n_alt, s_text, s_alt in REPRESENTATIONS:
        print(f"─── Level: '{level_name}' ─────────────────────────────────────")

        en,  tok_n  = embed(n_text,  tokenizer, model)
        en2, tok_n2 = embed(n_alt,   tokenizer, model)
        es,  tok_s  = embed(s_text,  tokenizer, model)
        es2, tok_s2 = embed(s_alt,   tokenizer, model)

        cross_l2  = l2(en, es)
        base_n_l2 = l2(en, en2)
        base_s_l2 = l2(es, es2)
        avg_tokens = (tok_n + tok_s) / 2
        efficiency = cross_l2 / avg_tokens if avg_tokens > 0 else 0.0

        print(f"  nothing text ({tok_n} tok):  {n_text[:60]!r}")
        print(f"  something text ({tok_s} tok): {s_text[:60]!r}")
        print(f"  L2(nothing × something) = {cross_l2:.3f}")
        print(f"  L2(nothing × nothing')  = {base_n_l2:.3f}  [same-class baseline]")
        print(f"  L2(something × something') = {base_s_l2:.3f}  [same-class baseline]")
        print(f"  L2 / token (efficiency) = {efficiency:.3f}")

        above_o0     = cross_l2 > REF_O0_CODE_ONLY
        above_exp12  = cross_l2 > REF_EXP12_PEAK
        above_o1     = cross_l2 > REF_O1_SEPARATED

        print(f"  > -O0 baseline?  {'YES' if above_o0    else 'no'}")
        print(f"  > exp12 peak?    {'YES' if above_exp12 else 'no'}")
        print(f"  > -O1 threshold? {'YES ← CEILING EXCEEDED' if above_o1 else 'no'}")
        print()

        results.append({
            "level":      level_name,
            "cross_l2":   cross_l2,
            "base_n":     base_n_l2,
            "base_s":     base_s_l2,
            "tok_n":      tok_n,
            "tok_s":      tok_s,
            "avg_tokens": avg_tokens,
            "efficiency": efficiency,
            "above_o1":   above_o1,
        })

    # ── Summary ────────────────────────────────────────────────────────────────
    print("=" * 70)
    print("SUMMARY — Pure Semantic L2 vs Reference Points")
    print("=" * 70)
    print(f"  {'level':<16} {'tokens':>6}  {'L2':>7}  {'vs -O0':>8}  {'vs exp12':>9}  {'vs -O1':>7}")
    print(f"  {'-'*16} {'-'*6}  {'-'*7}  {'-'*8}  {'-'*9}  {'-'*7}")
    for r in results:
        vs_o0    = f"+{r['cross_l2']-REF_O0_CODE_ONLY:.2f}" if r['cross_l2'] > REF_O0_CODE_ONLY    else f"{r['cross_l2']-REF_O0_CODE_ONLY:.2f}"
        vs_exp12 = f"+{r['cross_l2']-REF_EXP12_PEAK:.2f}"  if r['cross_l2'] > REF_EXP12_PEAK      else f"{r['cross_l2']-REF_EXP12_PEAK:.2f}"
        vs_o1    = f"+{r['cross_l2']-REF_O1_SEPARATED:.2f}" if r['cross_l2'] > REF_O1_SEPARATED    else f"{r['cross_l2']-REF_O1_SEPARATED:.2f}"
        mark     = " ← CEILING EXCEEDED" if r['above_o1'] else ""
        print(f"  {r['level']:<16} {r['avg_tokens']:>6.0f}  {r['cross_l2']:>7.3f}  {vs_o0:>8}  {vs_exp12:>9}  {vs_o1:>7}{mark}")

    # ── Interpretation ─────────────────────────────────────────────────────────
    best = max(results, key=lambda r: r["cross_l2"])
    print()
    print(f"  Best pure-semantic L2: {best['cross_l2']:.3f}  at level '{best['level']}'")
    print()
    if best["above_o1"]:
        print("  RESULT: Context-only embedding EXCEEDS the -O1 threshold.")
        print("  → The manifold CAN separate these concepts cleanly.")
        print("  → Experiment 12 failure was DILUTION, not topology.")
        print("  → The -O0 ABI frame created a metric basin, not a topological trap.")
        print("  → Basin is shallow. A sufficiently context-rich representation escapes.")
    elif best["cross_l2"] > REF_EXP12_PEAK:
        print("  RESULT: Context-only exceeds exp12 peak but not the -O1 threshold.")
        print("  → Removing the ASM denominator helps — dilution was real.")
        print("  → But the semantic ceiling is below the compiler's structural gap.")
        print("  → Partial dilution effect. The manifold also has genuine semantic proximity.")
    else:
        print("  RESULT: Context-only DOES NOT exceed even the exp12 peak.")
        print("  → The manifold folds void-nothing and int-something close SEMANTICALLY.")
        print("  → This is not a metric failure. This is geometric proximity in learned space.")
        print("  → The -O1 compiler gap cannot be reproduced by any short context.")
        print("  → The confusion is in the representation itself.")

    print()
    print("  Thesis:")
    print("    Experiment 11: compiler -O1 separation = L2 12.66")
    print("    Experiment 12: code-dominated geometry — context force limited by dilution")
    print("    Experiment 13: pure semantic ceiling — the confusion basin quantified")
    print(f"                   ceiling = {best['cross_l2']:.3f} at '{best['level']}'")
    print("=" * 70)

    # ── Plot ───────────────────────────────────────────────────────────────────
    print(f"\nGenerating plot → {OUT_PNG}")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor("#0d1117")
    for ax in axes:
        ax.set_facecolor("#161b22")
        for spine in ax.spines.values():
            spine.set_color("#30363d")

    levels     = [r["level"] for r in results]
    cross_l2s  = [r["cross_l2"] for r in results]
    base_ns    = [r["base_n"] for r in results]
    base_ss    = [r["base_s"] for r in results]
    avg_toks   = [r["avg_tokens"] for r in results]
    x          = np.arange(len(levels))
    w          = 0.28

    # Panel 1: L2 per representation level
    ax = axes[0]
    bars = ax.bar(x,       cross_l2s, w, label="nothing × something",  color="#58a6ff", alpha=0.9)
    ax.bar(x + w, base_ns,   w, label="nothing × nothing'",   color="#3fb950", alpha=0.7)
    ax.bar(x + 2*w, base_ss, w, label="something × something'", color="#d2a8ff", alpha=0.7)

    # Highlight bars that exceed -O1
    for i, (bar, r) in enumerate(zip(bars, results)):
        if r["above_o1"]:
            bar.set_edgecolor("#ffa657")
            bar.set_linewidth(2)

    ax.axhline(REF_O1_SEPARATED, color="#f0f6fc", linewidth=1.5, linestyle="--",
               alpha=0.9, label=f"-O1 threshold ({REF_O1_SEPARATED:.2f})")
    ax.axhline(REF_EXP12_PEAK,  color="#ffa657", linewidth=1.2, linestyle="-.",
               alpha=0.7, label=f"exp12 peak ({REF_EXP12_PEAK:.2f})")
    ax.axhline(REF_O0_CODE_ONLY, color="#8b949e", linewidth=1.0, linestyle=":",
               alpha=0.7, label=f"-O0 raw ({REF_O0_CODE_ONLY:.2f})")

    ax.set_xticks(x + w)
    ax.set_xticklabels(levels, rotation=30, ha="right", color="#c9d1d9", fontsize=9)
    ax.set_ylabel("L2 distance", color="#8b949e", fontsize=11)
    ax.set_title("Pure Semantic L2 by Representation Level", color="#f0f6fc",
                 fontsize=12, pad=10)
    ax.tick_params(colors="#8b949e")
    ax.legend(fontsize=8, facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")
    ax.set_ylim(bottom=0)

    # Panel 2: L2 vs token count (efficiency scatter)
    ax2 = axes[1]
    sc = ax2.scatter(avg_toks, cross_l2s,
                     c=["#ffa657" if r["above_o1"] else "#58a6ff" for r in results],
                     s=90, zorder=5, edgecolors="#f0f6fc", linewidths=0.5)

    for r in results:
        ax2.annotate(r["level"], (r["avg_tokens"], r["cross_l2"]),
                     textcoords="offset points", xytext=(5, 3),
                     color="#8b949e", fontsize=8)

    ax2.axhline(REF_O1_SEPARATED, color="#f0f6fc", linewidth=1.5, linestyle="--",
                alpha=0.9, label=f"-O1 threshold ({REF_O1_SEPARATED:.2f})")
    ax2.axhline(REF_EXP12_PEAK,  color="#ffa657", linewidth=1.2, linestyle="-.",
                alpha=0.7, label=f"exp12 peak ({REF_EXP12_PEAK:.2f})")
    ax2.axhline(REF_O0_CODE_ONLY, color="#8b949e", linewidth=1.0, linestyle=":",
                alpha=0.7, label=f"-O0 raw ({REF_O0_CODE_ONLY:.2f})")

    ax2.set_xlabel("Token count (avg of both inputs)", color="#8b949e", fontsize=11)
    ax2.set_ylabel("L2 distance  (nothing × something)", color="#8b949e", fontsize=11)
    ax2.set_title("Semantic Efficiency: L2 vs Token Count", color="#f0f6fc",
                  fontsize=12, pad=10)
    ax2.tick_params(colors="#8b949e")
    ax2.legend(fontsize=8, facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

    # Annotation: basin diagnosis
    best_l2 = best["cross_l2"]
    if best_l2 >= REF_O1_SEPARATED:
        diagnosis = "Basin: METRIC\nDilution was the barrier\nContext-only escapes"
        diag_color = "#3fb950"
    elif best_l2 > REF_EXP12_PEAK:
        diagnosis = "Basin: MIXED\nDilution + semantic proximity\nPartial context escape"
        diag_color = "#ffa657"
    else:
        diagnosis = "Basin: SEMANTIC\nManifold folds these concepts\nNo context type escapes"
        diag_color = "#ff7b72"

    ax2.text(0.97, 0.05, diagnosis,
             transform=ax2.transAxes, ha="right", va="bottom",
             fontsize=9, color=diag_color,
             bbox=dict(facecolor="#21262d", edgecolor="#30363d", boxstyle="round,pad=0.5"))

    plt.suptitle(
        "Experiment 13 — Pure Semantic Geometry\n"
        "Context as ground state: no disassembly, no ABI frame, no dilution attractor",
        color="#f0f6fc", fontsize=11, y=1.01
    )
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Plot saved → {OUT_PNG}")


if __name__ == "__main__":
    main()
