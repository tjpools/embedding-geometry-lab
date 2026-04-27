#!/usr/bin/env python3
"""
Experiment 14 — Minimum Token Separation Across a Function Corpus
=================================================================================
Core question:
  What is the minimum token representation that allows the manifold to correctly
  cluster 4 distinct computational domains?

  At what granularity level does the transformer stop confusing:
    SphereVolume  (floating-point geometry: r³ × 4/3π)
    EasterDate    (modular arithmetic: Gaussian calendar algorithm)
    BaseAdd       (integer arithmetic: base conversion)
    MemProbe      (memory: RSS measurement via /proc)

Corpus:
  Each domain has two compiled variants:
    - ASM binary  (hand-written NASM, compiled via nasm + gcc)
    - CPP binary  (C++ source, compiled via g++)
  These are the SAME function expressed two ways → same-class pair.
  8 total embeddings. Correct clustering = 4 groups of 2.

Granularity levels:
  0  name only      — "SphereVolume", "EasterDate", "BaseAdd", "MemProbe"
  1  return type    — "double SphereVolume", "int EasterDate", ...
  2  key insn       — the single most domain-discriminating instruction
                      (atof for sphere, idiv/mod for easter, shr for base, fgets/sscanf for mem)
  3  first 5 insns  — prologue + first instructions
  4  full disasm    — complete function disassembly from objdump

Metrics at each level:
  - 8×8 pairwise L2 distance matrix
  - Within-class L2: distance between ASM and CPP variants of same domain
  - Between-class L2: distance between different domains (mean of off-diagonal blocks)
  - Separability ratio: between_class / within_class — if > 1, classes are separated
  - Silhouette-style score: (between - within) / max(between, within) ∈ [-1, 1]

Prediction from experiment 13:
  Function names (2-3 tokens) will be the most efficient.
  Return type (1 token) will carry significant discriminating power.
  Full disassembly will be noisiest (denominator dilution).
  The efficiency curve will again decrease with token count.

Output: experiments/assets/14_minimum_token_separation.png
Run:    source environment/intel-travel/bin/activate && python3 experiments/14_minimum_token_separation.py
=================================================================================
"""

import re
import subprocess
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
OUT_PNG        = EXPERIMENT_DIR / "assets" / "14_minimum_token_separation.png"
OUT_PNG.parent.mkdir(exist_ok=True)

ASM_BINS = {
    "SphereVolume": EXPERIMENT_DIR / "sphere" / "sphere_asm",
    "EasterDate":   EXPERIMENT_DIR / "easter" / "easter_asm",
    "BaseAdd":      EXPERIMENT_DIR / "base"   / "base_asm",
    "MemProbe":     EXPERIMENT_DIR / "mem"    / "mem_asm",
}
CPP_BINS = {
    "SphereVolume": EXPERIMENT_DIR / "sphere" / "sphere_cpp",
    "EasterDate":   EXPERIMENT_DIR / "easter" / "easter_cpp",
    "BaseAdd":      EXPERIMENT_DIR / "base"   / "base_cpp",
    "MemProbe":     EXPERIMENT_DIR / "mem"    / "mem_cpp",
}
# CPP static domain functions are inlined into main by the compiler.
# ASM exports named domain labels; CPP does not.
ASM_FUNC_NAMES = {
    "SphereVolume": "SphereVolume",
    "EasterDate":   "EasterDate",
    "BaseAdd":      "BaseAdd",
    "MemProbe":     "MemProbe",
}
CPP_FUNC_NAMES = {
    "SphereVolume": "main",
    "EasterDate":   "main",
    "BaseAdd":      "main",
    "MemProbe":     "main",
}

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_ID   = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE     = "cuda"
DTYPE      = torch.float16
MAX_TOKENS = 512

DOMAINS = ["SphereVolume", "EasterDate", "BaseAdd", "MemProbe"]

# Return types and key instructions — domain fingerprints
DOMAIN_META = {
    "SphereVolume": {
        "return_type": "double",
        "key_insn":    "mulsd  %xmm",     # SSE2 floating point multiply
        "description": "floating-point sphere volume: r³ × 4/3π",
    },
    "EasterDate": {
        "return_type": "int",
        "key_insn":    "idiv",             # signed integer division for modular arithmetic
        "description": "modular arithmetic: Gaussian Easter date algorithm",
    },
    "BaseAdd": {
        "return_type": "int",
        "key_insn":    "shr",              # bit shift for base conversion
        "description": "integer arithmetic: positional base conversion",
    },
    "MemProbe": {
        "return_type": "long",
        "key_insn":    "sscanf",           # reads /proc/self/status for RSS
        "description": "memory probe: RSS measurement via /proc",
    },
}


# ── Disassembly extraction ─────────────────────────────────────────────────────

def extract_function(binary: Path, func_name: str) -> list[str]:
    """Return list of instruction lines for func_name from binary."""
    r = subprocess.run(
        ["objdump", "-d", "--no-show-raw-insn", str(binary)],
        capture_output=True, text=True
    )
    lines  = r.stdout.splitlines()
    block  = []
    inside = False
    for line in lines:
        if re.search(rf"<{re.escape(func_name)}>:", line):
            inside = True
            continue
        if inside:
            if line.strip() == "" and block:
                break
            if re.search(r"<[A-Za-z_]", line) and block:
                break
            stripped = line.strip()
            if stripped and re.match(r"[0-9a-f]+:", stripped):
                # Extract just the instruction part (after the address)
                insn = re.sub(r"^[0-9a-f]+:\s*", "", stripped)
                if insn:
                    block.append(insn)
    return block


def find_key_insn_line(insns: list[str], key_fragment: str) -> str:
    """Find the first instruction line containing key_fragment."""
    for insn in insns:
        if key_fragment.lower() in insn.lower():
            return insn
    # Fall back to first non-prologue instruction
    for insn in insns:
        if insn not in ("endbr64", "push   %rbp", "mov    %rsp,%rbp"):
            return insn
    return insns[0] if insns else "nop"


# ── Representation builder ─────────────────────────────────────────────────────

def build_representations(domain: str, insns: list[str], variant: str) -> dict[str, str]:
    """Build all 5 granularity levels for a given domain's disassembly."""
    meta    = DOMAIN_META[domain]
    key_i   = find_key_insn_line(insns, meta["key_insn"])
    first5  = "\n".join(insns[:5])
    full    = "\n".join(insns)

    return {
        "name":      domain,
        "ret+name":  f"{meta['return_type']} {domain}",
        "key_insn":  key_i,
        "first5":    first5,
        "full":      full,
    }


# ── Embedding ──────────────────────────────────────────────────────────────────

def embed(text: str, tokenizer, model) -> tuple[np.ndarray, int]:
    enc = tokenizer(text, return_tensors="pt", truncation=True,
                    max_length=MAX_TOKENS).to(DEVICE)
    n   = enc["input_ids"].shape[1]
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    vec = out.hidden_states[-1][0].mean(dim=0).float().cpu().numpy()
    return vec, n


def l2(a, b):
    return float(np.linalg.norm(a - b))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Experiment 14 — Minimum Token Separation Across a Function Corpus")
    print("=" * 70)

    # Load model
    print(f"\nLoading {MODEL_ID} …")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=DTYPE, device_map=DEVICE, attn_implementation="eager"
    )
    model.eval()
    print("Model ready.\n")

    # Extract disassembly for all 8 (domain × variant) combinations
    print("Extracting disassembly …")
    corpus = {}   # {(domain, variant): [insn lines]}
    for domain in DOMAINS:
        for variant, bins, func_names in [
            ("asm", ASM_BINS, ASM_FUNC_NAMES),
            ("cpp", CPP_BINS, CPP_FUNC_NAMES),
        ]:
            insns = extract_function(bins[domain], func_names[domain])
            corpus[(domain, variant)] = insns
            print(f"  {domain:14s} [{variant}] — {len(insns)} instructions")
            for i in insns[:3]:
                print(f"    {i}")
            print()

    # Build representations at all granularity levels
    LEVELS = ["name", "ret+name", "key_insn", "first5", "full"]
    keys   = [(d, v) for d in DOMAINS for v in ("asm", "cpp")]   # 8 items

    print("\nEmbedding all 8 × 5 = 40 representations …")
    # embeddings[level][key] = (vec, n_tokens)
    embeddings = {lv: {} for lv in LEVELS}
    token_counts = {lv: [] for lv in LEVELS}

    for domain in DOMAINS:
        for variant in ("asm", "cpp"):
            key   = (domain, variant)
            insns = corpus[key]
            reps  = build_representations(domain, insns, variant)
            for lv in LEVELS:
                vec, n = embed(reps[lv], tokenizer, model)
                embeddings[lv][key] = (vec, n)
                token_counts[lv].append(n)
                print(f"  {domain:14s} [{variant}] {lv:10s}  {n:3d} tok")

    # Compute 8×8 L2 matrices and separability at each level
    print("\n" + "=" * 70)
    print("SEPARABILITY ANALYSIS")
    print("=" * 70)

    separability = {}   # {level: score}
    within_means = {}
    between_means = {}
    matrices = {}

    for lv in LEVELS:
        mat = np.zeros((8, 8))
        for i, ki in enumerate(keys):
            for j, kj in enumerate(keys):
                vi = embeddings[lv][ki][0]
                vj = embeddings[lv][kj][0]
                mat[i, j] = l2(vi, vj)
        matrices[lv] = mat

        # Within-class: ASM vs CPP of same domain (4 pairs on off-diagonal of 2×2 blocks)
        within = []
        for di, domain in enumerate(DOMAINS):
            i = di * 2       # asm index
            j = di * 2 + 1   # cpp index
            within.append(mat[i, j])

        # Between-class: different domains (all pairs where domain differs)
        between = []
        for di in range(len(DOMAINS)):
            for dj in range(len(DOMAINS)):
                if di == dj:
                    continue
                for vi in range(2):
                    for vj in range(2):
                        between.append(mat[di*2+vi, dj*2+vj])

        wm = np.mean(within)
        bm = np.mean(between)
        score = (bm - wm) / max(bm, wm)   # silhouette-style ∈ [-1, 1]

        within_means[lv]  = wm
        between_means[lv] = bm
        separability[lv]  = score

        avg_tok = np.mean([embeddings[lv][k][1] for k in keys])
        print(f"\n  Level: '{lv}'  (avg {avg_tok:.1f} tokens)")
        print(f"    within-class  L2 = {wm:.3f}")
        print(f"    between-class L2 = {bm:.3f}")
        print(f"    separability     = {score:.3f}  {'✓ SEPARATED' if score > 0 else '✗ confused'}")
        print(f"    ratio            = {bm/wm:.2f}×")

    # Best level
    best_lv = max(separability, key=separability.get)
    print(f"\n  Best separability: '{best_lv}' = {separability[best_lv]:.3f}")

    # Per-domain diagnosis at best level
    print(f"\n  Confusion matrix at best level ('{best_lv}'):")
    print(f"  {'':16s}" + "".join(f"{d[:8]:>10s}" for d in DOMAINS))
    for di, da in enumerate(DOMAINS):
        row = f"  {da:16s}"
        for dj, db in enumerate(DOMAINS):
            vals = [matrices[best_lv][di*2+vi, dj*2+vj]
                    for vi in range(2) for vj in range(2)]
            row += f"{np.mean(vals):>10.2f}"
        print(row)

    # ── Plot ───────────────────────────────────────────────────────────────────
    print(f"\nGenerating plot → {OUT_PNG}")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.patch.set_facecolor("#0d1117")
    for ax in axes.flat:
        ax.set_facecolor("#161b22")
        for spine in ax.spines.values():
            spine.set_color("#30363d")

    COLORS = ["#58a6ff", "#3fb950", "#ffa657", "#ff7b72"]
    DOMAIN_COLORS = {d: COLORS[i] for i, d in enumerate(DOMAINS)}

    # Panels 0-3: heatmaps for each of first 4 levels
    LEVEL_LABELS = {
        "name":     "Level 0: Name only",
        "ret+name": "Level 1: Return type + name",
        "key_insn": "Level 2: Key instruction",
        "first5":   "Level 3: First 5 instructions",
        "full":     "Level 4: Full disassembly",
    }

    domain_variant_labels = [f"{d[:6]}\n[{v}]" for d, v in keys]

    for idx, lv in enumerate(LEVELS[:4]):
        ax = axes.flat[idx]
        mat = matrices[lv]
        im = ax.imshow(mat, cmap="plasma", aspect="auto")
        ax.set_xticks(range(8))
        ax.set_yticks(range(8))
        ax.set_xticklabels(domain_variant_labels, fontsize=7, color="#c9d1d9", rotation=45, ha="right")
        ax.set_yticklabels(domain_variant_labels, fontsize=7, color="#c9d1d9")
        ax.set_title(f"{LEVEL_LABELS[lv]}\nsep={separability[lv]:.3f}",
                     color="#f0f6fc", fontsize=9, pad=6)

        # Annotate cells
        for i in range(8):
            for j in range(8):
                ax.text(j, i, f"{mat[i,j]:.1f}", ha="center", va="center",
                        fontsize=6, color="white" if mat[i,j] < mat.max()*0.6 else "black")

        # Draw domain block borders
        for d in range(4):
            rect = plt.Rectangle((d*2-0.5, d*2-0.5), 2, 2,
                                  fill=False, edgecolor=COLORS[d], linewidth=2)
            ax.add_patch(rect)

    # Panel 4: separability curve + token efficiency
    ax4 = axes[1, 1]
    lv_labels  = [LEVEL_LABELS[lv].split(":")[1].strip() for lv in LEVELS]
    sep_vals   = [separability[lv] for lv in LEVELS]
    avg_tokens = [np.mean([embeddings[lv][k][1] for k in keys]) for lv in LEVELS]

    ax4_twin = ax4.twinx()
    ax4_twin.set_facecolor("#161b22")

    ax4.plot(range(len(LEVELS)), sep_vals, "o-", color="#58a6ff",
             linewidth=2.5, markersize=8, zorder=5, label="separability")
    ax4_twin.bar(range(len(LEVELS)), avg_tokens, alpha=0.25, color="#ffa657",
                 label="avg tokens")

    ax4.axhline(0, color="#8b949e", linewidth=1, linestyle="--", alpha=0.6)
    ax4.set_xticks(range(len(LEVELS)))
    ax4.set_xticklabels(lv_labels, rotation=25, ha="right", color="#c9d1d9", fontsize=8)
    ax4.set_ylabel("Separability score", color="#58a6ff", fontsize=10)
    ax4_twin.set_ylabel("Avg token count", color="#ffa657", fontsize=10)
    ax4.set_title("Separability vs Token Budget", color="#f0f6fc", fontsize=10, pad=8)
    ax4.tick_params(colors="#8b949e")
    ax4_twin.tick_params(colors="#ffa657")
    ax4.set_ylim(-1, 1)

    # annotate best
    best_idx = LEVELS.index(best_lv)
    ax4.annotate(f"best: {best_lv}\n{separability[best_lv]:.3f}",
                 (best_idx, sep_vals[best_idx]),
                 textcoords="offset points", xytext=(8, -20),
                 color="#f0f6fc", fontsize=8,
                 arrowprops=dict(arrowstyle="->", color="#f0f6fc"))

    # Panel 5: within vs between L2 by level
    ax5 = axes[1, 2]
    x = np.arange(len(LEVELS))
    w = 0.35
    ax5.bar(x - w/2, [within_means[lv]  for lv in LEVELS], w,
            color="#3fb950", alpha=0.85, label="within-class L2")
    ax5.bar(x + w/2, [between_means[lv] for lv in LEVELS], w,
            color="#ff7b72", alpha=0.85, label="between-class L2")
    ax5.set_xticks(x)
    ax5.set_xticklabels(lv_labels, rotation=25, ha="right", color="#c9d1d9", fontsize=8)
    ax5.set_ylabel("L2 distance", color="#8b949e", fontsize=10)
    ax5.set_title("Within vs Between Class L2", color="#f0f6fc", fontsize=10, pad=8)
    ax5.tick_params(colors="#8b949e")
    ax5.legend(fontsize=8, facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

    # Legend patches for domains
    patches = [mpatches.Patch(color=COLORS[i], label=DOMAINS[i]) for i in range(4)]
    fig.legend(handles=patches, loc="lower center", ncol=4, fontsize=9,
               facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9",
               bbox_to_anchor=(0.5, 0.0))

    plt.suptitle(
        "Experiment 14 — Minimum Token Separation Across a Function Corpus\n"
        "SphereVolume · EasterDate · BaseAdd · MemProbe  ×  ASM + CPP variants",
        color="#f0f6fc", fontsize=12, y=1.01
    )
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Plot saved → {OUT_PNG}")

    # Final summary
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print(f"  Corpus: {len(DOMAINS)} domains × 2 variants (ASM + CPP) = 8 embeddings")
    print(f"  Note: CPP domain code is inlined into 'main' by the compiler.")
    print(f"        ASM exports named labels (SphereVolume, EasterDate, etc.).")
    print(f"        Levels 0-1 use the domain name for both variants (by design).")
    print(f"        Levels 2-4 use ASM named function vs CPP 'main' body.")
    print(f"  Best separating level: '{best_lv}'")
    print(f"  Separability score:    {separability[best_lv]:.3f}")
    print()
    print("  Separability by level (high = well separated):")
    for lv in LEVELS:
        bar = "█" * max(0, int(separability[lv] * 20))
        print(f"    {lv:12s}  {separability[lv]:+.3f}  {bar}")
    print()

    if separability["name"] > 0:
        print("  ✓ Function names alone separate the domains.")
        print("    The manifold encodes domain identity in the name token.")
    else:
        print("  ✗ Function names alone do NOT separate the domains.")
        print("    Name tokens are insufficient — structural content required.")

    if separability["ret+name"] > separability["name"]:
        print("  ✓ Return type adds discriminating power beyond name alone.")
    else:
        print("  — Return type does not improve over name alone.")

    print()
    print("  Thesis connection:")
    print("    Experiment 13: 'void' vs 'int' = L2 40.15. Type token is the richest signal.")
    print("    Experiment 14: does that hold across semantically distinct domains,")
    print("                   or was it specific to the nothing/something pair?")
    print("=" * 70)


if __name__ == "__main__":
    main()
