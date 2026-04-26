"""
Experiment 03 — Easter Manifold
=================================
Three computational substrates. One algorithm. Same answer.

  Manifold 1: C++         — Gauss algorithm as typed, compiled procedure
  Manifold 2: x86-64 ASM — Gauss algorithm as raw register arithmetic on silicon
  Manifold 3: Transformer — TinyLlama navigates a learned semantic manifold

Thesis: metric matured from Leibniz → Riemann → Minsky → Transformers.
This experiment makes the difference in geometry visible.

Run:  python experiments/03_easter_manifold.py
"""

import os
import re
import subprocess
import time
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Configuration ──────────────────────────────────────────────────────────────
TEST_YEARS   = list(range(2020, 2031))
MODEL_ID     = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
EASTER_DIR   = os.path.join(os.path.dirname(__file__), "easter")
CPP_BIN      = os.path.join(EASTER_DIR, "easter_cpp")
ASM_BIN      = os.path.join(EASTER_DIR, "easter_asm")
ASSETS_DIR   = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ── Known Easter dates for verification (published tables) ────────────────────
KNOWN = {
    2020: (4, 12), 2021: (4,  4), 2022: (4, 17), 2023: (4,  9),
    2024: (3, 31), 2025: (4, 20), 2026: (4,  5), 2027: (3, 28),
    2028: (4, 16), 2029: (4,  1), 2030: (4, 21),
}
MONTH_NAME = {3: "March", 4: "April"}

# ══════════════════════════════════════════════════════════════════════════════
# Manifold 1 — Python oracle (Gauss Gregorian algorithm)
# Variable names match the assembly source exactly.
# ══════════════════════════════════════════════════════════════════════════════
def gauss_easter(year: int) -> tuple[int, int]:
    """Return (month, day) for Easter Sunday in the given Gregorian year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day   = (h + l - 7 * m + 114) % 31 + 1
    return month, day


# ══════════════════════════════════════════════════════════════════════════════
# Manifold helpers — run compiled binary, return (month, day, nanoseconds)
# ══════════════════════════════════════════════════════════════════════════════
def run_binary(binary: str, year: int) -> tuple[int, int, int]:
    t0 = time.perf_counter_ns()
    result = subprocess.run(
        [binary, str(year)],
        capture_output=True, text=True, timeout=5
    )
    t1 = time.perf_counter_ns()
    month, day = map(int, result.stdout.strip().split())
    return month, day, (t1 - t0)


# ══════════════════════════════════════════════════════════════════════════════
# Manifold 3 — Transformer probe
# ══════════════════════════════════════════════════════════════════════════════
def load_model(token):
    print(f"\n[load] {MODEL_ID} from cache...")
    t0 = time.time()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        token=token,
        dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True,
        attn_implementation="eager",   # required for output_attentions=True
    )
    model.to(device)
    model.eval()
    print(f"[load] done in {time.time()-t0:.1f}s  device={device.upper()}")
    return model, tokenizer, device


def probe_transformer(model, tokenizer, device, year: int) -> dict:
    """
    Run two passes for a given year:
      1. Generation pass  — get model's answer
      2. Prefill-only pass with output_attentions=True — capture attention geometry
    Returns dict with answer text, correctness flag, and attention tensor.
    """
    prompt = f"What is the date of Easter Sunday in {year}? Reply with just the month and day, e.g. 'April 20'."
    messages = [
        {"role": "system", "content": "You are a precise calendar assistant."},
        {"role": "user",   "content": prompt},
    ]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # ── Pass 1: generate answer ────────────────────────────────────────────
    with torch.no_grad():
        gen_ids = model.generate(
            **inputs,
            max_new_tokens=20,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    answer = tokenizer.decode(
        gen_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    ).strip()

    # ── Pass 2: prefill-only for attention geometry ────────────────────────
    with torch.no_grad():
        out = model(**inputs, output_attentions=True)

    # attention: tuple of (batch, heads, seq, seq) per layer
    # Stack to (n_layers, heads, seq, seq), squeeze batch dim
    attn = torch.stack([a[0] for a in out.attentions])   # (L, H, S, S)

    # Find token positions for the year digits in the input
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    year_str = str(year)
    year_positions = [
        i for i, t in enumerate(tokens)
        if year_str in t.replace("▁", "").replace("Ġ", "")
    ]

    return {
        "answer":         answer,
        "attn":           attn.cpu().float(),
        "tokens":         tokens,
        "year_positions": year_positions,
    }


def score_answer(answer: str, oracle_month: int, oracle_day: int) -> bool:
    """Check if the transformer's answer contains the correct month and day."""
    text = answer.lower()
    month_hit = MONTH_NAME.get(oracle_month, "").lower() in text
    # Accept numeric month too
    if not month_hit:
        month_hit = str(oracle_month) in text
    day_hit = str(oracle_day) in text
    return month_hit and day_hit


def save_attention_heatmap(attn: torch.Tensor, year: int, year_positions: list):
    """
    Save two subplots:
      Left:  per-layer average attention (mean over heads and query positions)
      Right: attention to year-digit tokens, averaged across layers
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"Transformer Attention Geometry — Easter {year}", fontsize=13)

    # Left: (L, S) — mean over heads and query dim
    layer_avg = attn.mean(dim=1).mean(dim=1)   # (L, S)
    ax = axes[0]
    im = ax.imshow(layer_avg.numpy(), aspect='auto', cmap='viridis')
    ax.set_title("Per-layer avg attention\n(mean over heads + queries)")
    ax.set_xlabel("Key token position")
    ax.set_ylabel("Layer")
    plt.colorbar(im, ax=ax)

    # Right: attention from all query positions to year-digit key positions
    if year_positions:
        year_attn = attn[:, :, :, year_positions].mean(dim=-1)  # (L, H, S)
        head_layer_avg = year_attn.mean(dim=-1)                  # (L, H)
        ax2 = axes[1]
        im2 = ax2.imshow(head_layer_avg.numpy(), aspect='auto', cmap='plasma')
        ax2.set_title(f"Attention to year '{year}' tokens\n(per layer × head)")
        ax2.set_xlabel("Head")
        ax2.set_ylabel("Layer")
        plt.colorbar(im2, ax=ax2)
    else:
        axes[1].text(0.5, 0.5, "Year tokens not\nisolated in sequence",
                     ha='center', va='center', transform=axes[1].transAxes)

    path = os.path.join(ASSETS_DIR, f"easter_attention_{year}.png")
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()
    return path


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    token = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN')

    print("=" * 70)
    print("Experiment 03 — Easter Manifold")
    print("Three substrates. One algorithm. Same answer.")
    print("=" * 70)

    # ── Verify Python oracle against published tables ──────────────────────
    print("\n[oracle] Verifying Python oracle against published Easter dates...")
    oracle_ok = True
    for year, (km, kd) in KNOWN.items():
        m, d = gauss_easter(year)
        status = "✓" if (m == km and d == kd) else "✗"
        if m != km or d != kd:
            oracle_ok = False
            print(f"  {status} {year}: got {MONTH_NAME[m]} {d}, expected {MONTH_NAME[km]} {kd}")
    if oracle_ok:
        print("  All 11 years match published tables ✓")

    # ── Load transformer ───────────────────────────────────────────────────
    model, tokenizer, device = load_model(token)

    # ── Three-way comparison table ─────────────────────────────────────────
    print("\n" + "=" * 70)
    print(f"{'Year':<6} {'C++ result':<14} {'C++ ns':>10}  "
          f"{'ASM result':<14} {'ASM ns':>10}  "
          f"{'Oracle':<14} {'Transformer answer':<28} {'✓?'}")
    print("-" * 70)

    results = []
    for year in TEST_YEARS:
        # C++
        cpp_m, cpp_d, cpp_ns = run_binary(CPP_BIN, year)
        cpp_str = f"{MONTH_NAME[cpp_m]} {cpp_d}"

        # ASM
        asm_m, asm_d, asm_ns = run_binary(ASM_BIN, year)
        asm_str = f"{MONTH_NAME[asm_m]} {asm_d}"

        # Oracle
        ora_m, ora_d = gauss_easter(year)
        ora_str = f"{MONTH_NAME[ora_m]} {ora_d}"

        # Transformer
        probe = probe_transformer(model, tokenizer, device, year)
        correct = score_answer(probe["answer"], ora_m, ora_d)
        mark = "✓" if correct else "✗"

        print(f"{year:<6} {cpp_str:<14} {cpp_ns:>10,}  "
              f"{asm_str:<14} {asm_ns:>10,}  "
              f"{ora_str:<14} {probe['answer'][:28]:<28} {mark}")

        results.append({
            "year": year,
            "oracle": (ora_m, ora_d),
            "correct": correct,
            "attn": probe["attn"],
            "year_positions": probe["year_positions"],
        })

    # ── Summary ────────────────────────────────────────────────────────────
    n_correct = sum(r["correct"] for r in results)
    print("-" * 70)
    print(f"\n[summary] Transformer accuracy: {n_correct}/{len(TEST_YEARS)} years correct")

    # ── Attention heatmaps ─────────────────────────────────────────────────
    print("\n[geometry] Saving attention heatmaps...")
    for r in results:
        path = save_attention_heatmap(r["attn"], r["year"], r["year_positions"])
        print(f"  saved: {path}")

    # ── Manifold narrative ─────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("Manifold Narrative")
    print("=" * 70)
    print("""
  C++:         (19*a + b - d - g + 15) % 30
               Gauss variables, typed arithmetic, compiled to x86-64.
               The algorithm is readable, portable, deterministic.
               The CPU executes integer division; the modulus is explicit.

  x86-64 ASM:  IMUL R11D, 19  /  IDIV EBX (30)  /  MOV R14D, EDX
               The same formula as bare register operations on silicon.
               No abstraction layer. The algorithm IS the instruction stream.
               Leibniz's dx expressed as IDIV.

  Transformer: No modulus operator. No integer division.
               Attention heads define a learned bilinear form M = Wq'Wk.
               The model routes through a continuous semantic manifold —
               a high-dimensional space shaped by training on human text —
               and arrives (or not) in the neighborhood of the correct date.

  Three geodesics. Three substrates. One algorithm.
  The geometry of how each substrate "gets there" is the experiment.
""")
    print("[done] Experiment 03 complete.")


if __name__ == "__main__":
    main()
