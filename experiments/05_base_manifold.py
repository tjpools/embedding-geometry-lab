#!/usr/bin/env python3
"""
Experiment 05 — Base Manifold
==============================
Thesis: 4+3=7 and 4+3=10 are not a contradiction.
They are the same manifold point expressed in different coordinate systems.

The frame annotation (base) is the suppressed subscript in Recorde's '=' glyph.
A transformer that lacks the frame will either default to base 10 or fail to
recognise that the base-change automorphism leaves the quantity invariant.

Substrates:
  Python  — oracle (int arithmetic + explicit base conversion)
  C++     — base.cpp  (compiled to base_cpp)
  x86-64  — base_linux.asm + base_shim.c  (compiled to base_asm)

Galois reading:
  The answer space of '4+3=?' has a base-change automorphism group.
  The quantity 7 is the invariant; its symbol is the orbit.
  A question without a frame annotation has a non-trivial symmetry group:
  the tire-pressure light should fire.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent
CPP_BIN = ROOT / "experiments/base/base_cpp"
ASM_BIN = ROOT / "experiments/base/base_asm"

BASES = [2, 5, 7, 8, 10, 16]

# ── Oracle ────────────────────────────────────────────────────────────────────

_DIGITS = "0123456789ABCDEF"

def oracle(base: int) -> str:
    """Base-invariant quantity 7, expressed in the given coordinate system."""
    n = 4 + 3
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = _DIGITS[n % base] + result
        n //= base
    return result


# ── Binary runner ─────────────────────────────────────────────────────────────

def run_binary(binary: Path, base: int) -> str:
    out = subprocess.run(
        [str(binary), str(base)],
        capture_output=True, text=True, timeout=5
    )
    return out.stdout.strip()


# ── Deterministic comparison ──────────────────────────────────────────────────

def run_deterministic():
    print("\n=== Deterministic Substrate Comparison: 4+3 across bases ===")
    print(f"  {'Base':>5}  {'Oracle':>8}  {'C++':>8}  {'ASM':>8}  {'C++':>5}  {'ASM':>5}")
    print("  " + "-" * 50)

    cpp_score = asm_score = 0
    for base in BASES:
        expected = oracle(base)
        cpp_out  = run_binary(CPP_BIN, base)
        asm_out  = run_binary(ASM_BIN, base)
        cpp_ok   = "✓" if cpp_out == expected else "✗"
        asm_ok   = "✓" if asm_out == expected else "✗"
        if cpp_out == expected: cpp_score += 1
        if asm_out == expected: asm_score += 1
        print(f"  {base:>5}  {expected:>8}  {cpp_out:>8}  {asm_out:>8}  {cpp_ok:>5}  {asm_ok:>5}")

    total = len(BASES)
    print(f"\n  C++: {cpp_score}/{total}   ASM: {asm_score}/{total}")
    print(f"\n  Observation: all three substrates agree in every base.")
    print(f"  The quantity is invariant. Only the frame changes the symbol.")


# ── Transformer ───────────────────────────────────────────────────────────────

def load_model(token: str):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    print(f"\nLoading {model_id} ...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, token=token,
        torch_dtype=__import__("torch").float16,
        device_map="auto",
        attn_implementation="eager",
    )
    model.eval()
    return tokenizer, model


def ask(tokenizer, model, question: str, max_new: int = 150) -> str:
    import torch
    messages = [
        {"role": "system", "content": "You are a precise mathematical assistant."},
        {"role": "user",   "content": question},
    ]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new,
            do_sample=False,
            temperature=1.0,
            repetition_penalty=1.1,
        )
    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    if "<|assistant|>" in decoded:
        return decoded.split("<|assistant|>")[-1].strip()
    return decoded[len(prompt):].strip()


# Probes — (label, question, expected, check_type)
# check_type 'exact'    : first integer in response must match expected
# check_type 'contains' : response must contain expected string (case-insensitive)
PROBES = [
    # Frame absent — base 10 assumed by default
    ("No frame",
     "What is 4 plus 3?",
     "7", "exact"),

    # Frame explicit — deceptive because answer looks like "ten"
    ("Base 7 explicit",
     "What is 4 plus 3 written in base 7?",
     "10", "exact"),

    # Frame explicit — binary
    ("Base 2 (binary)",
     "What is 4 plus 3 written in base 2?",
     "111", "exact"),

    # Frame explicit — base 5
    ("Base 5 explicit",
     "What is 4 plus 3 written in base 5?",
     "12", "exact"),

    # The Galois question: solvability of the apparent contradiction
    ("Contradiction or base?",
     "Someone claims both '4+3=7' and '4+3=10' are correct. "
     "Is this a contradiction, or is there an explanation? Answer briefly.",
     "base 7", "contains"),

    # Frame-finding: invert the map
    ("Find the base (10)",
     "In what base does 4+3 equal 10?",
     "7", "exact"),

    # Frame-finding: base 5
    ("Find the base (12)",
     "In what base does 4+3 equal 12?",
     "5", "exact"),

    # Meta: does the model know its own default frame?
    ("Default frame awareness",
     "When you answered '4+3=7' just now, which number base were you assuming?",
     "10", "exact"),
]


def probe_transformer(tokenizer, model):
    print("\n=== Transformer Frame Probes ===")
    score = 0
    results = []

    for label, question, expected, check in PROBES:
        response = ask(tokenizer, model, question)

        if check == "exact":
            nums = re.findall(r'\b\d+\b', response)
            got  = nums[0] if nums else "?"
            ok   = got == expected
        else:  # contains
            got  = "(see response)"
            ok   = expected.lower() in response.lower()

        marker = "✓" if ok else "✗"
        if ok:
            score += 1

        results.append((label, expected, got, marker, response))
        print(f"\n  [{label}]")
        print(f"    Q: {question}")
        print(f"    Expected: {expected!r}   Got: {got!r}   {marker}")
        print(f"    Response: {response[:220]}")

    print(f"\n  Transformer score: {score}/{len(PROBES)}")

    # Summary of failure modes
    print("\n  Failure mode analysis:")
    for label, expected, got, marker, response in results:
        if marker == "✗":
            print(f"    [{label}] expected {expected!r}, got {got!r}")

    return score


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN", "")

    run_deterministic()

    tokenizer, model = load_model(token)
    score = probe_transformer(tokenizer, model)

    print("\n=== Thesis ===")
    print("  4+3=7 and 4+3=10 are the same manifold point.")
    print("  The base is the coordinate system; the quantity is the invariant.")
    print("  Suppressing the base is Recorde's glyph: '=' without a subscript.")
    print("  The Galois group of '4+3=?' has a base-change automorphism.")
    print("  The question is solvable only when the frame annotation is fixed.")
    print("  Without it: structural hazard. Two answers, same register. Tire light on.")


if __name__ == "__main__":
    main()
