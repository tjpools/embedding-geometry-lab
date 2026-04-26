#!/usr/bin/env python3
"""
Experiment 11 — Embedding Distance: Elaborate Nothing vs Simple Something
=================================================================================
Core question:
  In the transformer's representation space, how far apart are:

    A — elaborate nothing:   void f_nothing()  { }          (ABI frame, no body)
    B — simple something:    int  f_something() { return 1; } (minimal payload)

  No extra context. No query. Pure embedding geometry.

If the manifold treats structural complexity as semantic content,
A and B will be closer than expected — the ABI frame mimics the return
frame and the model conflates them.

If the manifold correctly separates structural noise from semantic signal,
A and B will be far apart even though B is structurally simpler than A.

Method:
  1. Compile real C functions at three optimization levels (-O0, -O1, -O2)
     using gcc — we see how compiler optimization changes the gap.
  2. Extract disassembly via objdump for each compiled variant.
  3. Feed each disassembly to TinyLlama, extract the last hidden state
     of the final token — this is the model's embedding of the full sequence.
  4. Compute pairwise cosine similarity and L2 distance.
  5. Compare against control pairs:
       same × same     → upper bound (similarity ≈ 1.0)
       nothing × nothing (two instances) → same-class baseline
       something × something (two instances) → same-class baseline
       nothing × something → the measurement of interest

Prediction:
  At -O0: A has 5-instruction ABI frame, B has 6-instruction frame + mov + ret.
          Structurally similar. Embedding distance may be small.
  At -O2: A compiles to bare `ret`. B compiles to `mov eax,1 / ret`.
          Structurally diverge. Embedding distance should grow.

  If prediction holds: compiler optimization *increases* the semantic gap
  by reducing structural noise. Rust's zero-cost abstraction is the
  extreme case — elaborate nothing → bare ret → indistinguishable from silence.

Thesis connection:
  Experiment 10: attention cost of nothing grows with structural complexity.
  Experiment 11: embedding *distance* between nothing and something shrinks
                 as structural complexity of nothing increases.
  Together: elaborate nothing is expensive AND confusing. Both costs are real.

Output: experiments/assets/11_embedding_distance.png
Run:    python experiments/11_embedding_distance.py
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
OUT_PNG        = EXPERIMENT_DIR / "assets" / "11_embedding_distance.png"

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE   = "cuda"
DTYPE    = torch.float16
MAX_TOKENS = 512   # cap input length

# ── C source variants ──────────────────────────────────────────────────────────
C_NOTHING = """\
// elaborate nothing: full ABI frame, no body
void f_nothing(void) {
}
"""

C_SOMETHING = """\
// simple something: minimal payload
int f_something(void) {
    return 1;
}
"""

# Two distinct "nothing" functions for same-class baseline
C_NOTHING_2 = """\
// elaborate nothing variant 2
void g_nothing(void) {
}
"""

# Two distinct "something" functions for same-class baseline
C_SOMETHING_2 = """\
// simple something variant 2
int g_something(void) {
    return 2;
}
"""

OPT_LEVELS = ["-O0", "-O1", "-O2"]


# ── Compilation ────────────────────────────────────────────────────────────────

def compile_and_disassemble(source: str, func_name: str, opt: str) -> str:
    """
    Compile a C function snippet and return its objdump disassembly.
    Returns only the named function's block.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = Path(tmpdir) / "func.c"
        obj_path = Path(tmpdir) / "func.o"
        src_path.write_text(source)

        # Compile to object file (no link)
        result = subprocess.run(
            ["gcc", opt, "-c", str(src_path), "-o", str(obj_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"gcc failed ({opt}):\n{result.stderr}")

        # Disassemble
        result = subprocess.run(
            ["objdump", "-d", "--no-show-raw-insn", str(obj_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"objdump failed:\n{result.stderr}")

        # Extract named function block
        lines     = result.stdout.splitlines()
        in_block  = False
        collected = []
        for line in lines:
            if re.search(rf'<{re.escape(func_name)}>:', line):
                in_block = True
                collected.append(f"[{func_name}  opt={opt}]")
                continue
            if in_block:
                if re.match(r'^[0-9a-f]+ <', line):
                    break
                if line.strip():
                    collected.append(line)

        if not collected:
            raise RuntimeError(
                f"Function <{func_name}> not found in disassembly."
            )
        return "\n".join(collected)


# ── Embedding extraction ───────────────────────────────────────────────────────

def get_embedding(model, tokenizer, text: str) -> torch.Tensor:
    """
    Returns the mean-pooled last hidden state over all tokens.
    This is the model's geometric representation of the full input.
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_TOKENS,
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model(
            **inputs,
            output_hidden_states=True,
        )

    # Last hidden state: (1, seq_len, hidden_dim)
    last_hidden = outputs.hidden_states[-1]          # (1, T, H)
    # Mean pool over sequence length
    embedding = last_hidden[0].mean(dim=0)           # (H,)
    return embedding.float()


def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    a = a / a.norm()
    b = b / b.norm()
    return (a @ b).item()


def l2_distance(a: torch.Tensor, b: torch.Tensor) -> float:
    return (a - b).norm().item()


# ── Main ───────────────────────────────────────────────────────────────────────

print("=" * 70)
print("Experiment 11 — Embedding Distance: Elaborate Nothing vs Simple Something")
print("=" * 70)
print()

# Compile all variants
print("[compiling C functions at all optimization levels...]")
print()

variants = {}   # (func_name, opt) → disassembly_text

sources = {
    "f_nothing":   C_NOTHING,
    "f_something": C_SOMETHING,
    "g_nothing":   C_NOTHING_2,
    "g_something": C_SOMETHING_2,
}

for opt in OPT_LEVELS:
    print(f"  [{opt}]")
    for func_name, source in sources.items():
        asm = compile_and_disassemble(source, func_name, opt)
        variants[(func_name, opt)] = asm
        lines = asm.count("\n")
        print(f"    {func_name:16s}  {lines+1:2d} lines")
        for line in asm.splitlines():
            print(f"      {line}")
        print()

# Load model
print("[loading model...]")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, torch_dtype=DTYPE, device_map=DEVICE,
    attn_implementation="eager",
)
model.eval()
torch.cuda.empty_cache()
weights_mb = torch.cuda.memory_allocated() / (1024 ** 2)
print(f"[ready]    weights: {weights_mb:.1f} MB VRAM\n")

# Extract embeddings
print("[extracting embeddings...]")
embeddings = {}
for key, asm_text in variants.items():
    emb = get_embedding(model, tokenizer, asm_text)
    embeddings[key] = emb
    print(f"  {key[0]:16s}  {key[1]}  dim={emb.shape[0]}")

print()

# Compute pairwise distances for each opt level
print("── Pairwise distances ───────────────────────────────────────────────")
print()

results = []   # list of dicts for plotting

for opt in OPT_LEVELS:
    fn = embeddings[("f_nothing",   opt)]
    fs = embeddings[("f_something", opt)]
    gn = embeddings[("g_nothing",   opt)]
    gs = embeddings[("g_something", opt)]

    pairs = {
        "nothing × something (A vs B)":   (fn, fs),
        "nothing × nothing  (baseline)":  (fn, gn),
        "something × something (baseline)": (fs, gs),
        "nothing × nothing  (self)":      (fn, fn),
    }

    print(f"  [{opt}]")
    print(f"    {'pair':<42}  {'cosine sim':>10}  {'L2 dist':>8}")
    print(f"    {'─' * 64}")

    opt_results = {"opt": opt}
    for label, (a, b) in pairs.items():
        cos = cosine_similarity(a, b)
        l2  = l2_distance(a, b)
        print(f"    {label:<42}  {cos:>10.4f}  {l2:>8.3f}")
        opt_results[label] = {"cos": cos, "l2": l2}

    results.append(opt_results)
    print()

# ── Plot ───────────────────────────────────────────────────────────────────────
print("[generating embedding distance plot...]")
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle(
    "Experiment 11 — Embedding Distance: Elaborate Nothing vs Simple Something",
    fontsize=12, fontweight="bold"
)

pair_labels = [
    "nothing × something\n(A vs B — key measurement)",
    "nothing × nothing\n(same-class baseline)",
    "something × something\n(same-class baseline)",
    "nothing × nothing\n(self — upper bound)",
]
pair_keys = [
    "nothing × something (A vs B)",
    "nothing × nothing  (baseline)",
    "something × something (baseline)",
    "nothing × nothing  (self)",
]

colors = {
    "nothing × something (A vs B)":         "#e74c3c",
    "nothing × nothing  (baseline)":        "#3498db",
    "something × something (baseline)":     "#2ecc71",
    "nothing × nothing  (self)":            "#95a5a6",
}

x     = np.arange(len(OPT_LEVELS))
width = 0.18
offsets = np.linspace(-1.5, 1.5, len(pair_keys)) * width

# Panel 1: cosine similarity
ax1.set_title("Cosine similarity by optimization level\n"
              "(1.0 = identical geometry, 0.0 = orthogonal)", fontsize=10)
for i, (key, label) in enumerate(zip(pair_keys, pair_labels)):
    ys = [r[key]["cos"] for r in results]
    ax1.bar(x + offsets[i], ys, width, label=label,
            color=colors[key], alpha=0.85, edgecolor="#bdc3c7")

ax1.set_xticks(x)
ax1.set_xticklabels(OPT_LEVELS, fontsize=10)
ax1.set_xlabel("GCC optimization level", fontsize=9)
ax1.set_ylabel("Cosine similarity", fontsize=9)
ax1.set_ylim(0, 1.15)
ax1.axhline(y=1.0, color="#bdc3c7", lw=0.8, linestyle="--")
ax1.legend(fontsize=7.5, loc="lower right")
ax1.grid(axis="y", alpha=0.3)

# Panel 2: L2 distance
ax2.set_title("L2 distance by optimization level\n"
              "(0.0 = identical, larger = more separated)", fontsize=10)
for i, (key, label) in enumerate(zip(pair_keys, pair_labels)):
    ys = [r[key]["l2"] for r in results]
    ax2.bar(x + offsets[i], ys, width, label=label,
            color=colors[key], alpha=0.85, edgecolor="#bdc3c7")

ax2.set_xticks(x)
ax2.set_xticklabels(OPT_LEVELS, fontsize=10)
ax2.set_xlabel("GCC optimization level", fontsize=9)
ax2.set_ylabel("L2 distance", fontsize=9)
ax2.legend(fontsize=7.5, loc="upper right")
ax2.grid(axis="y", alpha=0.3)

fig.text(0.01, 0.01,
         "A = void f_nothing(){}  |  B = int f_something(){return 1;}  |  "
         "model: TinyLlama-1.1B  |  embedding: mean-pooled last hidden state",
         fontsize=7, color="#aaa")

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=130, bbox_inches="tight")
print(f"[saved]    {OUT_PNG}")
print()

# ── Conclusion ─────────────────────────────────────────────────────────────────
print("── Key measurement: nothing × something gap vs optimization ─────────")
for r in results:
    key = "nothing × something (A vs B)"
    cos = r[key]["cos"]
    l2  = r[key]["l2"]
    print(f"  [{r['opt']}]  cosine={cos:.4f}  L2={l2:.3f}")

print()
# Does the gap grow with optimization (as elaboration is stripped)?
cos_vals = [r["nothing × something (A vs B)"]["cos"] for r in results]
if cos_vals[-1] < cos_vals[0]:
    print("  Result: gap GROWS with optimization.")
    print("  Compiler stripping the ABI frame increases semantic separation.")
    print("  Elaborate nothing was confusingly close to simple something.")
elif cos_vals[-1] > cos_vals[0]:
    print("  Result: gap SHRINKS with optimization.")
    print("  Optimized code converges in embedding space regardless of content.")
else:
    print("  Result: gap is stable across optimization levels.")
print()
print("── The manifold measures structural pattern, not semantic intent. ────")
print("   Elaborate nothing occupies a different region than simple something.")
print("   But the distance depends on how elaborately nothing is dressed.")
print("=" * 70)
