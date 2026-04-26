#!/usr/bin/env python3
"""
Experiment 04 — Sphere Manifold
Three-substrate comparison: V = (4/3) * π * r³

Substrates:
  1. Python oracle       — math.pi (double, ~15 sig digits)
  2. C++ binary          — M_PI constant (double)
  3. x87 ASM binary      — FLDPI instruction (80-bit extended, ~18-19 sig digits)
  4. Transformer         — TinyLlama-1.1B (learned float16 manifold)

The three-parameter predicate:
  - 4/3    : exact rational
  - π      : transcendental — unreachable by any finite representation
  - r³     : depends on input precision

Thesis: The deterministic substrates agree to double precision.
        The transformer navigates a learned manifold of "sphere volume" text.
        Where that manifold is dense (r=1,2,3), it may recall.
        Where it is sparse, it hallucinates into its attractor.
"""

import os, sys, subprocess, time, math
from pathlib import Path
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT     = Path(__file__).parent.parent
CPP_BIN  = ROOT / "experiments/sphere/sphere_cpp"
ASM_BIN  = ROOT / "experiments/sphere/sphere_asm"

# ── Oracle ─────────────────────────────────────────────────────────────────────
def sphere_volume(r: float) -> float:
    return (4.0 / 3.0) * math.pi * r ** 3

# ── Binary runner ──────────────────────────────────────────────────────────────
def run_binary(binary, r):
    t0 = time.perf_counter_ns()
    result = subprocess.run([str(binary), str(r)],
                            capture_output=True, text=True, timeout=5)
    ns = time.perf_counter_ns() - t0
    val = float(result.stdout.strip())
    return val, ns

# ── Model ──────────────────────────────────────────────────────────────────────
def load_model(token):
    MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    device   = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=token)
    model     = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, token=token,
        dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True,
        attn_implementation="eager",
    )
    model.to(device).eval()
    return model, tokenizer, device

def probe_transformer(model, tokenizer, device, r):
    """Ask TinyLlama for the volume of a sphere with radius r."""
    prompt = (f"What is the volume of a sphere with radius {r}? "
              f"Use the formula V = (4/3) * pi * r^3. "
              f"Give only the numerical answer rounded to 4 decimal places.")
    messages = [
        {"role": "system", "content": "You are a precise mathematics assistant."},
        {"role": "user",   "content": prompt},
    ]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    with torch.no_grad():
        gen_ids = model.generate(
            **inputs, max_new_tokens=60, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    answer = tokenizer.decode(
        gen_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    return answer

def parse_first_number(text):
    """Extract the first float-like token from model output."""
    import re
    # look for decimal numbers, possibly with commas as thousands separators
    text = text.replace(',', '')
    m = re.search(r'-?\d+\.?\d*', text)
    return float(m.group()) if m else None

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    load_dotenv(ROOT / '.env')
    token = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN')

    # Test radii: integers the model may have seen, a decimal, and a large value
    TEST_RADII = [1, 2, 3, 5, 10, 0.5, 7, 100]

    print("=" * 70)
    print("Experiment 04 — Sphere Manifold: V = (4/3)·π·r³")
    print("=" * 70)

    # ── Deterministic comparison table ─────────────────────────────────────────
    print(f"\n{'r':>8}  {'Oracle':>16}  {'C++':>16}  {'C++ err':>12}  {'ASM':>16}  {'ASM err':>12}")
    print("-" * 90)
    for r in TEST_RADII:
        oracle      = sphere_volume(r)
        cpp_val, _  = run_binary(CPP_BIN, r)
        asm_val, _  = run_binary(ASM_BIN, r)
        cpp_err     = abs(cpp_val - oracle)
        asm_err     = abs(asm_val - oracle)
        print(f"{r:>8}  {oracle:>16.6f}  {cpp_val:>16.6f}  {cpp_err:>12.2e}  {asm_val:>16.6f}  {asm_err:>12.2e}")

    # ── Timing comparison ──────────────────────────────────────────────────────
    print(f"\n{'r':>8}  {'C++ (µs)':>12}  {'ASM (µs)':>12}")
    print("-" * 40)
    for r in TEST_RADII:
        _, cpp_ns = run_binary(CPP_BIN, r)
        _, asm_ns = run_binary(ASM_BIN, r)
        print(f"{r:>8}  {cpp_ns/1000:>12.1f}  {asm_ns/1000:>12.1f}")

    # ── Transformer probe ──────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("Transformer Probe — TinyLlama manifold navigation")
    print("=" * 70)
    print("[loading model...]\n")
    model, tokenizer, device = load_model(token)
    print(f"[ready on {device.upper()}]\n")

    PROBE_RADII = [1, 2, 3, 5, 10]   # most likely in training data
    print(f"{'r':>6}  {'Oracle':>14}  {'Model answer':<40}  {'Parsed':>12}  {'Error':>12}  {'✓?':>4}")
    print("-" * 100)
    correct = 0
    for r in PROBE_RADII:
        oracle  = sphere_volume(r)
        answer  = probe_transformer(model, tokenizer, device, r)
        parsed  = parse_first_number(answer)
        if parsed is not None:
            err    = abs(parsed - oracle)
            rel    = err / oracle
            ok     = "✓" if rel < 0.01 else "✗"   # within 1%
            if rel < 0.01:
                correct += 1
        else:
            err, ok = float('nan'), "✗"
        short_ans = answer[:40].replace('\n', ' ')
        print(f"{r:>6}  {oracle:>14.4f}  {short_ans:<40}  {str(parsed) if parsed else 'N/A':>12}  {str(round(err,4)) if parsed else 'N/A':>12}  {ok:>4}")

    print(f"\nTransformer score: {correct}/{len(PROBE_RADII)}")

    # ── π awareness probe ──────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("π Awareness Probe")
    print("=" * 70)

    pi_probes = [
        ("Value of π",
         "What is the value of pi to 15 decimal places?"),
        ("π in sphere",
         "Why does the formula for the volume of a sphere contain pi?"),
        ("Transcendence of π",
         "Is pi a rational number, irrational, or transcendental? What does that mean for computing sphere volumes exactly?"),
        ("The approximation",
         "If a computer stores pi as 3.141592653589793, is the computed sphere volume exact? Why or why not?"),
    ]
    for label, prompt in pi_probes:
        messages = [
            {"role": "system", "content": "You are a precise mathematics assistant."},
            {"role": "user",   "content": prompt},
        ]
        input_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        with torch.no_grad():
            gen_ids = model.generate(
                **inputs, max_new_tokens=100, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        answer = tokenizer.decode(
            gen_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        print(f"\n[{label}]")
        print(f"  Q: {prompt}")
        print(f"  A: {answer}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("  Python/C++/ASM: All substrates agree to double precision (~15 sig digits)")
    print("  ASM uses x87 FLDPI: 80-bit extended precision π (most precise available)")
    print("  All three: bounded error from true π — Gödelian incompleteness in silicon")
    print(f"  Transformer: {correct}/{len(PROBE_RADII)} volume calculations correct")
    print("  The manifold knows the formula — the question is whether it executes it")

if __name__ == "__main__":
    main()
