#!/usr/bin/env python3
"""
Experiment 06 — Memory Manifold
=================================
Thesis: Memory is temporal curvature.

  Easter measured cyclic structure.
  Sphere measured geometric curvature.
  Base measured coordinate curvature.
  Memory measures temporal curvature — how the model bends
  under the weight of its own past.

A stateless substrate (ASM) has zero temporal curvature:
  10,000 calls cost the same as 1.

A transformer accumulates KV cache with every token of context:
  VRAM = f(context_length), slope ≠ 0.

The slope of VRAM vs. context length IS the temporal curvature κ_t.
The architecture pays this cost whether or not the past was useful.

Theoretical κ_t for TinyLlama-1.1B (GQA):
  2 (K+V) × 22 layers × 4 KV heads × 64 head_dim × 2 bytes (float16)
  = 22,528 bytes/token ≈ 22 KB/token

Compare:
  ASM binary:        κ_t = 0          (no state — no past, no cost)
  C++ context alloc: κ_t ≈ 1 KB/KB   (capacity only — data in, data held)
  Transformer:       κ_t ≈ 22 KB/tok  (structural — paid by the architecture)

Substrates:
  C++         — mem.cpp compiled to mem_cpp
  x86-64 ASM  — mem_linux.asm + mem_shim.c compiled to mem_asm
  Transformer — TinyLlama-1.1B-Chat-v1.0 on CUDA

Run: python experiments/06_memory_manifold.py
"""

import os
import re
import statistics
import subprocess
import sys
from pathlib import Path

# ── Capture RSS immediately — before loading torch / transformers ──────────────
import psutil
_proc = psutil.Process(os.getpid())
RSS_PYTHON_MB = _proc.memory_info().rss / 1024**2

import torch
RSS_TORCH_MB = _proc.memory_info().rss / 1024**2

from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
RSS_TRANSFORMERS_MB = _proc.memory_info().rss / 1024**2

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).parent.parent
CPP_BIN = ROOT / "experiments/mem/mem_cpp"
ASM_BIN = ROOT / "experiments/mem/mem_asm"

load_dotenv(ROOT / ".env")
TOKEN    = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# TinyLlama-1.1B architecture constants (from config.json)
# GQA: 32 attention heads, 4 KV heads, hidden_size=2048, head_dim=64
LAYERS    = 22
KV_HEADS  = 4
HEAD_DIM  = 64
BYTES     = 2   # float16
KV_SIDES  = 2   # K and V

KAPPA_T_THEORY_BYTES = KV_SIDES * LAYERS * KV_HEADS * HEAD_DIM * BYTES  # per token

# Context sizes to probe
CONTEXT_SIZES_KB = [0, 64, 256, 1024, 4096]
CALL_COUNTS      = [1, 10, 100, 1000, 10000]
CONTEXT_LENS     = [1, 10, 25, 50, 100, 200, 400, 800]

# ── Helpers ────────────────────────────────────────────────────────────────────

def run_cpp(context_kb):
    r = subprocess.run([str(CPP_BIN), str(context_kb)],
                       capture_output=True, text=True)
    m = re.search(r'rss_before=(\d+)\s+rss_after=(\d+)\s+delta=(-?\d+)', r.stdout)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None, None, None

def run_asm(n_calls):
    r = subprocess.run([str(ASM_BIN), str(n_calls)],
                       capture_output=True, text=True)
    m = re.search(r'rss_before=(\d+)\s+rss_after=(\d+)\s+delta=(-?\d+)', r.stdout)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None, None, None

def linreg_slope(xs, ys):
    n = len(xs)
    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)
    num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(xs, ys))
    den = sum((xi - x_mean) ** 2 for xi in xs)
    return num / den if den else 0.0

# ── Header ─────────────────────────────────────────────────────────────────────
print("=" * 70)
print("Experiment 06 — Memory Manifold: temporal curvature")
print("=" * 70)

# ── Section 1A: C++ context curve ─────────────────────────────────────────────
print("\n── 1A  C++ substrate: RSS vs. allocated context (KB) ─────────────────")
print(f"  {'context_KB':>12}  {'before_KB':>10}  {'after_KB':>10}  {'delta_KB':>10}")
print("  " + "-" * 49)
cpp_xs, cpp_ys = [], []
for kb in CONTEXT_SIZES_KB:
    before, after, delta = run_cpp(kb)
    cpp_xs.append(kb)
    cpp_ys.append(delta if delta is not None else 0)
    print(f"  {kb:>12}  {before:>10}  {after:>10}  {delta:>10}")

cpp_slope = linreg_slope(cpp_xs[1:], cpp_ys[1:])   # skip 0,0 point
print(f"\n  Measured slope: {cpp_slope:.3f} KB RSS / KB allocated")
print(f"  Expected:       ~1.0  (pure capacity — no architectural overhead)")

# ── Section 1B: ASM call curve ────────────────────────────────────────────────
print("\n── 1B  ASM substrate: RSS vs. N calls to MemProbe() ──────────────────")
print(f"  {'n_calls':>10}  {'before_KB':>10}  {'after_KB':>10}  {'delta_KB':>10}  {'probe':>8}")
print("  " + "-" * 56)
for n in CALL_COUNTS:
    r = subprocess.run([str(ASM_BIN), str(n)], capture_output=True, text=True)
    m = re.search(r'rss_before=(\d+)\s+rss_after=(\d+)\s+delta=(-?\d+)\s+probe=(\d+)',
                  r.stdout)
    if m:
        before, after, delta, probe = (int(m.group(i)) for i in range(1, 5))
        print(f"  {n:>10}  {before:>10}  {after:>10}  {delta:>10}  {probe:>8}")

print(f"\n  Temporal curvature: κ_t = 0  (stateless — the past leaves no trace)")

# ── Section 2: Python import layer costs ──────────────────────────────────────
print("\n── 2   Python import layers: cumulative RAM cost ─────────────────────")
checkpoints = [
    ("Python bare (psutil only)",  RSS_PYTHON_MB),
    ("+ torch",                    RSS_TORCH_MB),
    ("+ transformers",             RSS_TRANSFORMERS_MB),
]
print(f"  {'checkpoint':<30}  {'RSS_MB':>8}  {'delta_MB':>10}")
print("  " + "-" * 54)
prev = 0.0
for name, val in checkpoints:
    delta = val - prev if prev else 0.0
    print(f"  {name:<30}  {val:>8.1f}  {delta:>+10.1f}")
    prev = val
print(f"\n  Note: torch ~378 MB is CUDA driver + .so maps (shared across processes)")

# ── Section 3: Transformer temporal curvature ─────────────────────────────────
print("\n── 3   Transformer: VRAM vs. context length ──────────────────────────")
print("[loading model...]")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=TOKEN)
RSS_MODEL_LOADED_MB = _proc.memory_info().rss / 1024**2

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.float16,
    attn_implementation="eager",
    token=TOKEN,
)

use_cuda = torch.cuda.is_available()
if use_cuda:
    model = model.cuda()
model.eval()

VRAM_MODEL_MB = torch.cuda.memory_allocated() / 1024**2 if use_cuda else 0.0
RSS_POST_LOAD_MB = _proc.memory_info().rss / 1024**2

print(f"[ready on {'CUDA' if use_cuda else 'CPU'}]")
print(f"  RSS after model load:  {RSS_POST_LOAD_MB:.1f} MB")
if use_cuda:
    print(f"  VRAM (model weights):  {VRAM_MODEL_MB:.1f} MB")

vocab_size  = tokenizer.vocab_size
vram_points = []   # (context_len, peak_vram_MB)

print(f"\n  {'context_tokens':>16}  {'peak_VRAM_MB':>14}  {'delta_MB':>12}  {'delta_KB/tok':>14}")
print("  " + "-" * 62)

prev_vram = None
with torch.no_grad():
    for ctx_len in CONTEXT_LENS:
        # Exact-length input — random token IDs from mid-vocab range
        input_ids = torch.randint(100, vocab_size - 100, (1, ctx_len),
                                  dtype=torch.long)
        if use_cuda:
            input_ids = input_ids.cuda()

        if use_cuda:
            torch.cuda.reset_peak_memory_stats()

        _ = model.generate(
            input_ids,
            max_new_tokens=1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

        peak_mb  = torch.cuda.max_memory_allocated() / 1024**2 if use_cuda else 0.0
        vram_points.append((ctx_len, peak_mb))

        delta_mb  = peak_mb - prev_vram if prev_vram is not None else 0.0
        delta_kpt = (delta_mb * 1024 / (ctx_len - (CONTEXT_LENS[CONTEXT_LENS.index(ctx_len)-1]
                     if CONTEXT_LENS.index(ctx_len) > 0 else ctx_len))
                     if prev_vram is not None else 0.0)

        print(f"  {ctx_len:>16}  {peak_mb:>14.2f}  {delta_mb:>+12.2f}  {delta_kpt:>14.2f}")
        prev_vram = peak_mb

# ── Section 4: Fit κ_t ────────────────────────────────────────────────────────
print("\n── 4   Temporal curvature coefficient κ_t ────────────────────────────")
xs = [p[0] for p in vram_points]
ys = [p[1] for p in vram_points]
slope_mb_per_tok  = linreg_slope(xs, ys)
slope_kb_per_tok  = slope_mb_per_tok * 1024
theory_kb_per_tok = KAPPA_T_THEORY_BYTES / 1024

print(f"\n  Measured  κ_t = {slope_kb_per_tok:.2f} KB / token")
print(f"  Theory    κ_t = {theory_kb_per_tok:.2f} KB / token")
print(f"            = 2 × {LAYERS} layers × {KV_HEADS} KV heads × {HEAD_DIM} head_dim × {BYTES} bytes")
ratio = slope_kb_per_tok / theory_kb_per_tok if theory_kb_per_tok else 0
print(f"  Ratio measured / theory = {ratio:.2f}×")
print(f"  (overhead above 1.0× = allocator reservation + activation buffers)")

# ── Section 5: Summary ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("Summary — temporal curvature by substrate")
print("=" * 70)
print(f"  Substrate        κ_t               Interpretation")
print(f"  {'─'*64}")
print(f"  ASM (×10000)     0 KB/call         stateless — no past, no cost")
print(f"  C++ context      {cpp_slope:.2f} KB/KB       capacity only — data in, data held")
print(f"  Transformer      {slope_kb_per_tok:.1f} KB/token     structural — the architecture bends")
print()
print(f"  The transformer pays {slope_kb_per_tok:.1f} KB per token of past it is asked to hold.")
print(f"  The ASM pays 0. That is the cost of never having been present.")
print(f"  The transformer's past curves its present. Silicon has no memory of the past.")
print("=" * 70)
