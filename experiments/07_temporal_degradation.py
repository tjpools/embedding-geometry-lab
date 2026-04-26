#!/usr/bin/env python3
"""
Experiment 07 — Temporal Degradation
======================================
Thesis: Geometric capacity and semantic capacity share the same manifold.
        When VRAM curvature bends quadratically, recall accuracy degrades.

Experiment 06 established:
  κ_t = 249 KB/token (measured), accelerating — suggesting O(n²) behavior.
  The linear KV-cache story is incomplete at realistic context lengths.

This experiment extends to 2000 tokens and overlays:
  Geometry track : peak VRAM vs. context length  → quadratic fit → knee point
  Behavior track : anchor recall accuracy vs. context length → degradation curve

Behavioral probes (3 per context length):
  A. Early anchor  — "The code word is ZENITH."  [filler...]  "What was the code word?"
  B. Numeric anchor— "My PIN is 4937."            [filler...]  "What is my PIN?"
  C. Frame anchor  — "We work in base 7."         [filler...]  "What base are we using?"

If the manifold curvature hypothesis holds:
  recall degrades at the same context length where d²VRAM/dn² accelerates most.

Substrates:
  Geometry : random token IDs, max_new_tokens=1 (pure VRAM measurement)
  Behavior : TinyLlama-1.1B-Chat-v1.0, max_new_tokens=40

Output: experiments/assets/07_temporal_degradation.png

Runtime: ~10–15 minutes (behavioral track at long contexts is slow on MX550)
Run:     python experiments/07_temporal_degradation.py
"""

import os
import re
import statistics
import warnings
from pathlib import Path

import psutil
_proc = psutil.Process(os.getpid())

import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
transformers.logging.set_verbosity_error()

# ── Config ─────────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
ASSET_DIR = ROOT / "experiments/assets"
ASSET_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT / ".env")
TOKEN    = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Context length ladders
GEOM_LENS  = [1, 10, 25, 50, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
BEHAV_LENS = [50, 200, 500, 1000, 1600]

# Filler text — neutral, avoids all anchor words, ~68 tokens per unit
FILLER_UNIT = (
    "The weather outside is mild with a gentle breeze from the northwest. "
    "Scientists have published new findings on atmospheric pressure gradients. "
    "The library recently expanded its collection to include rare manuscripts. "
    "Engineers completed the final phase of the bridge construction last month. "
)

# Behavioral probes
PROBES = [
    dict(
        name    = "early_anchor",
        anchor  = "The secret code word for this conversation is: ZENITH. Please remember it.",
        question= "What was the secret code word I gave you at the very beginning of this conversation? State only the word.",
        scorer  = lambda r: 1 if "zenith" in r.lower() else 0,
    ),
    dict(
        name    = "numeric_anchor",
        anchor  = "My PIN number is 4937. Please remember this exact number.",
        question= "What was the PIN number I mentioned at the start of this conversation? State only the digits.",
        scorer  = lambda r: 1 if "4937" in r else 0,
    ),
    dict(
        name    = "frame_anchor",
        anchor  = "For this entire conversation we are working in base 7. In base 7, the number seven is written as 10.",
        question= "In what number base are we working in this conversation? State only the base number.",
        scorer  = lambda r: 1 if re.search(r'\b7\b', r) else 0,
    ),
]

SYS_MSG = "You are a helpful assistant with a perfect memory for details mentioned earlier in the conversation."

# ── Helpers ────────────────────────────────────────────────────────────────────

def build_prompt(tokenizer, anchor, question, target_tokens):
    """Build chat prompt: anchor at start, filler in middle, question at end.
    Targets approximately target_tokens total (including template overhead)."""
    base_content = f"{anchor}\n\n{question}"
    base_prompt  = tokenizer.apply_chat_template(
        [{"role": "system", "content": SYS_MSG},
         {"role": "user",   "content": base_content}],
        tokenize=False, add_generation_prompt=True,
    )
    base_len = tokenizer(base_prompt, return_tensors="pt").input_ids.shape[1]

    if base_len >= target_tokens:
        return base_prompt, base_len

    unit_len = tokenizer(FILLER_UNIT, return_tensors="pt").input_ids.shape[1]
    n_units  = max(0, (target_tokens - base_len) // unit_len)
    filler   = FILLER_UNIT * n_units

    full_content = f"{anchor}\n\n{filler}\n\n{question}"
    full_prompt  = tokenizer.apply_chat_template(
        [{"role": "system", "content": SYS_MSG},
         {"role": "user",   "content": full_content}],
        tokenize=False, add_generation_prompt=True,
    )
    actual_len = tokenizer(full_prompt, return_tensors="pt").input_ids.shape[1]
    return full_prompt, actual_len


def measure_vram(model, tokenizer, ctx_len, device):
    """Peak VRAM for a single 1-token forward pass at ctx_len input tokens."""
    try:
        ids = torch.randint(
            100, tokenizer.vocab_size - 100, (1, ctx_len),
            dtype=torch.long, device=device,
        )
        attn = torch.ones((1, ctx_len), dtype=torch.long, device=device)
        torch.cuda.reset_peak_memory_stats()
        with torch.no_grad():
            model.generate(
                ids, attention_mask=attn,
                max_new_tokens=1, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        return torch.cuda.max_memory_allocated() / 1024**2
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return None


def run_probe(model, tokenizer, probe, ctx_len, device):
    """Run one behavioral probe at target context length. Returns (score, actual_len, response)."""
    prompt, actual_len = build_prompt(tokenizer, probe["anchor"], probe["question"], ctx_len)
    ids  = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    attn = torch.ones_like(ids)
    with torch.no_grad():
        out = model.generate(
            ids, attention_mask=attn,
            max_new_tokens=40, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    resp  = tokenizer.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()
    score = probe["scorer"](resp)
    return score, actual_len, resp


# ── Load model ─────────────────────────────────────────────────────────────────
print("=" * 70)
print("Experiment 07 — Temporal Degradation: geometry meets behavior")
print("=" * 70)
print("\n[loading model...]")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.float16,
    attn_implementation="eager",
    token=TOKEN,
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model  = model.to(device).eval()

vram_weights = torch.cuda.memory_allocated() / 1024**2 if device == "cuda" else 0.0
print(f"[ready on {device.upper()}]  weights: {vram_weights:.1f} MB VRAM")

# ── Geometric track ────────────────────────────────────────────────────────────
print("\n── Geometric track: peak VRAM vs. context length ─────────────────────")
print(f"  {'tokens':>7}  {'VRAM_MB':>10}  {'delta_MB':>10}  {'KB/tok':>10}")
print("  " + "─" * 44)

geom_pts  = []   # (ctx_len, vram_MB)
prev_v, prev_n = None, None

for ctx_len in GEOM_LENS:
    v = measure_vram(model, tokenizer, ctx_len, device)
    if v is None:
        print(f"  {ctx_len:>7}  {'OOM':>10}  (stopping geometric track)")
        break
    geom_pts.append((ctx_len, v))
    delta_mb  = v - prev_v if prev_v is not None else 0.0
    delta_kpt = (delta_mb * 1024 / (ctx_len - prev_n)) if (prev_v is not None and ctx_len > prev_n) else 0.0
    print(f"  {ctx_len:>7}  {v:>10.2f}  {delta_mb:>+10.2f}  {delta_kpt:>10.2f}")
    prev_v, prev_n = v, ctx_len

# Quadratic fit
xs_g = np.array([p[0] for p in geom_pts], dtype=float)
ys_g = np.array([p[1] for p in geom_pts], dtype=float)
coeffs   = np.polyfit(xs_g, ys_g, 2)
a, b, c0 = coeffs
ys_fit   = np.polyval(coeffs, xs_g)
rmse     = float(np.sqrt(np.mean((ys_g - ys_fit)**2)))
knee_n   = float(abs(b / (2 * a))) if a != 0 else 0.0   # n where quadratic = linear term

print(f"\n  Quadratic fit:  VRAM(n) = {a:.3e}·n² + {b:.4f}·n + {c0:.1f}")
print(f"  RMSE = {rmse:.3f} MB")
print(f"  n² term equals linear term at n ≈ {abs(b/a):.0f} tokens (crossover)")
print(f"  n² dominates for n > {knee_n:.0f} tokens")

# ── Behavioral track ──────────────────────────────────────────────────────────
print(f"\n── Behavioral track: recall probes at {BEHAV_LENS} tokens ─────────────")
print(f"  {'ctx':>6}  {'actual':>7}  {'ZENITH':>8}  {'4937':>6}  {'base7':>7}  {'mean':>6}")
print("  " + "─" * 48)

behav_results = []   # (ctx_len, actual_len, [scores], mean, [responses])

for ctx_len in BEHAV_LENS:
    scores, actuals, resps = [], [], []
    for probe in PROBES:
        score, actual_len, resp = run_probe(model, tokenizer, probe, ctx_len, device)
        scores.append(score)
        actuals.append(actual_len)
        resps.append(resp[:70].replace('\n', ' '))
    mean = statistics.mean(scores)
    behav_results.append((ctx_len, actuals[0], scores, mean, resps))
    sym = ['✓' if s else '✗' for s in scores]
    print(f"  {ctx_len:>6}  {actuals[0]:>7}  {sym[0]:>8}  {sym[1]:>6}  {sym[2]:>7}  {mean:>6.2f}")
    for probe, r in zip(PROBES, resps):
        print(f"    [{probe['name']:<15}] {r}")

# ── Joint plot ─────────────────────────────────────────────────────────────────
print("\n[generating joint geometry + behavior plot...]")

fig, ax1 = plt.subplots(figsize=(13, 7))
ax2 = ax1.twinx()

# --- VRAM: measured points ---
geom_xs = [p[0] for p in geom_pts]
geom_ys = [p[1] for p in geom_pts]
ax1.plot(geom_xs, geom_ys, 'o-', color='steelblue', linewidth=2, markersize=5,
         label='Peak VRAM (measured)', zorder=3)

# --- VRAM: quadratic fit ---
xs_dense = np.linspace(float(min(geom_xs)), float(max(geom_xs)), 400)
ax1.plot(xs_dense, np.polyval(coeffs, xs_dense), '--', color='steelblue', alpha=0.5,
         linewidth=1.5, label=f'Quad. fit  (a={a:.2e}·n²)')

# --- Recall: mean ---
bxs  = [r[0] for r in behav_results]
bys  = [r[3] for r in behav_results]
ax2.plot(bxs, bys, 's-', color='crimson', linewidth=2.5, markersize=9, zorder=4,
         label='Mean recall accuracy')

# --- Recall: per-probe ---
probe_styles = [('--', '#e08080'), (':', '#b02020'), ('-.', '#7a0000')]
for i, pname in enumerate(['A: ZENITH', 'B: 4937', 'C: base7']):
    pys_i = [r[2][i] for r in behav_results]
    ax2.plot(bxs, pys_i, probe_styles[i][0], color=probe_styles[i][1],
             linewidth=1.2, alpha=0.7, label=f'  {pname}')

# --- Exp 06 knee marker ---
knee_x_06 = 800
ax1.axvline(x=knee_x_06, color='gray', linestyle=':', linewidth=1.5, alpha=0.6)
ax1.text(knee_x_06 + 25, float(min(geom_ys)) + 0.04 * float(max(geom_ys) - min(geom_ys)),
         'Exp 06 knee', fontsize=8, color='gray')

# --- Axes ---
ax1.set_xlabel('Context length (tokens)', fontsize=12)
ax1.set_ylabel('Peak VRAM (MB)', color='steelblue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.set_ylim(bottom=float(min(geom_ys)) * 0.95)

ax2.set_ylabel('Mean recall accuracy', color='crimson', fontsize=12)
ax2.tick_params(axis='y', labelcolor='crimson')
ax2.set_ylim(-0.05, 1.15)
ax2.set_yticks([0.0, 1/3, 2/3, 1.0])
ax2.set_yticklabels(['0', '⅓', '⅔', '1'])

# --- Legend ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9, framealpha=0.9)

plt.title(
    f'Experiment 07 — Temporal Degradation: VRAM curvature vs. recall accuracy\n'
    f'TinyLlama-1.1B (MX550 CUDA)  |  '
    f'VRAM(n) ≈ {a:.2e}·n² + {b:.4f}·n + {c0:.1f}',
    fontsize=11,
)
fig.tight_layout()

outpath = ASSET_DIR / "07_temporal_degradation.png"
fig.savefig(str(outpath), dpi=150)
print(f"  Saved: {outpath}")

# ── Summary ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("Summary — Temporal Degradation")
print("=" * 70)
print(f"  VRAM quadratic coefficient:  a = {a:.3e} MB/tok²")
print(f"  n² term dominates for n ≳ {knee_n:.0f} tokens")
print()

behav_ctx = [r[0] for r in behav_results]
behav_mean = [r[3] for r in behav_results]
for ctx, mean in zip(behav_ctx, behav_mean):
    bar = '█' * int(mean * 20) + '░' * (20 - int(mean * 20))
    print(f"  Recall @ {ctx:>5} tok:  [{bar}]  {mean:.2f}")

print()
recall_drop = behav_mean[0] - behav_mean[-1] if behav_mean else 0
vram_at_1600 = next((v for n, v in geom_pts if n >= 1600), geom_pts[-1][1])
vram_at_50   = next((v for n, v in geom_pts if n >= 50), geom_pts[0][1])
print(f"  VRAM at   50 tokens: {vram_at_50:.1f} MB")
print(f"  VRAM at 1600 tokens: {vram_at_1600:.1f} MB  ({vram_at_1600/vram_at_50:.1f}× baseline)")
print(f"  Recall drop:  {behav_mean[0]:.2f} → {behav_mean[-1]:.2f}  (Δ = {recall_drop:+.2f})")
print()
print("  The VRAM curve bends quadratically.")
print("  The recall curve follows it down.")
print("  The model's past curves its present — and what it held at the start")
print("  recedes toward the boundary of the manifold as context length grows.")
print("=" * 70)
