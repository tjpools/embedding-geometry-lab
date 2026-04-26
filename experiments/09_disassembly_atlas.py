#!/usr/bin/env python3
"""
Experiment 09 — Disassembly Atlas
=================================================================================
A compiled binary is a Monster Group.

The source code encodes a clear mathematical intent: sphere volume, V = 4/3·π·r³.
Compilation destroys that global structure. What remains is a sequence of local
opcode charts — basic blocks of machine instructions — each linearizing a tiny
fragment of the computation, globally incoherent in isolation.

This experiment asks: how many local charts does TinyLlama need before it can
infer the global mathematical intent?

The arc mirrors Conway working with the Monster:
  1 block  → noise (no coherent inference)
  k blocks → partial signal (arithmetic emerging)
  N blocks → convergence (sphere volume identified)

The rhumb line is the first response that mentions any computation at all.
The great circle is the response that correctly identifies V = 4/3·π·r³.

Disassembly backend:
  PRIMARY  — Ghidra 12.0.4 headless (C-like pseudocode, richer signal)
  FALLBACK — objdump -d (raw x86-64 opcodes, sparser signal)

  The experiment auto-detects which backend is available.
  Ghidra produces the better atlas. objdump still works — it just
  takes more charts before the model converges.

  To install Ghidra (Java 21 required, already present):
    wget https://github.com/NationalSecurityAgency/ghidra/releases/download/\
Ghidra_12.0.4_build/ghidra_12.0.4_PUBLIC_20260303.zip -O /tmp/ghidra.zip
    unzip /tmp/ghidra.zip -d ~/
    export GHIDRA_HOME=~/ghidra_12.0.4_PUBLIC

Thesis crystallizer:
  Conway never saw the Monster globally. He read local character tables,
  local symmetries, local combinatorial shadows — and inferred the shape.
  TinyLlama reads local opcode blocks and infers the mathematics.
  The Polynesian navigator reads local swells and infers the island.
  The destination was always present in the local data.
  Training reveals the geodesic that the geometry already implied.

Target binary: experiments/sphere/sphere_asm
  Source:  experiments/sphere/sphere.cpp   (V = 4/3·π·r³)
  Build:   gcc sphere.cpp -o sphere_asm -lm

Output: experiments/assets/09_disassembly_atlas.png
Run:    python experiments/09_disassembly_atlas.py
=================================================================================
"""

import os
import re
import subprocess
import shutil
import tempfile
import textwrap
import warnings
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
BINARY_PATH    = EXPERIMENT_DIR / "sphere" / "sphere_asm"
OUT_PNG        = EXPERIMENT_DIR / "assets" / "09_disassembly_atlas.png"

GHIDRA_HOME    = Path(os.environ.get("GHIDRA_HOME",
                      Path.home() / "ghidra_12.0.4_PUBLIC"))
GHIDRA_HEADLESS = GHIDRA_HOME / "support" / "analyzeHeadless"

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE   = "cuda"
DTYPE    = torch.float16
MAX_NEW  = 120

# ── Scoring: keywords indicating convergence toward "sphere volume" ─────────────
# Weighted by specificity — higher weight = stronger signal toward global intent
KEYWORD_WEIGHTS = {
    # Tier 3 — high specificity
    "sphere volume":   3.0,
    "4/3":             3.0,
    "four.thirds":     3.0,
    "volume of a sphere": 3.0,
    # Tier 2 — medium specificity
    "sphere":          2.0,
    "volume":          1.5,
    "radius":          1.5,
    "pi":              1.0,
    "3.14":            1.0,
    "cubic":           1.0,
    # Tier 1 — weak signal
    "math":            0.3,
    "formula":         0.3,
    "geometric":       0.5,
    "computes":        0.2,
    "calculates":      0.2,
}
MAX_POSSIBLE_SCORE = sum(KEYWORD_WEIGHTS.values())

SYSTEM_PROMPT = (
    "You are a reverse engineering expert with deep knowledge of mathematics "
    "and x86-64 assembly. When shown disassembled machine code, you identify "
    "the mathematical function being computed. Be concise and specific."
)

QUERY_TEMPLATE = (
    "The following is disassembled x86-64 machine code from a Linux binary "
    "(one or more basic blocks). Based ONLY on the code shown, what "
    "mathematical computation does this program perform? "
    "Name the formula if you recognize it.\n\n"
    "--- DISASSEMBLY ---\n"
    "{blocks}\n"
    "--- END ---\n\n"
    "Mathematical function being computed:"
)


# ── Disassembly backend ────────────────────────────────────────────────────────

def detect_backend() -> str:
    """Returns 'ghidra' if Ghidra headless is available, else 'objdump'."""
    if GHIDRA_HEADLESS.exists():
        return "ghidra"
    if shutil.which("objdump"):
        return "objdump"
    raise RuntimeError("No disassembly backend found. Install Ghidra or objdump.")


def extract_blocks_objdump(binary: Path) -> list[dict]:
    """
    Parse objdump -d output into basic blocks.
    Each block is a dict: {addr, label, instructions: [str], raw_text: str}
    """
    result = subprocess.run(
        ["objdump", "-d", "--no-show-raw-insn", str(binary)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"objdump failed: {result.stderr}")

    blocks = []
    current_label = None
    current_addr  = None
    current_insns = []

    for line in result.stdout.splitlines():
        # Function / label header: "0000000000001149 <main>:"
        label_match = re.match(r'^([0-9a-f]+)\s+<([^>]+)>:', line)
        if label_match:
            if current_label and current_insns:
                blocks.append(_make_block(current_addr, current_label, current_insns))
            current_addr  = label_match.group(1)
            current_label = label_match.group(2)
            current_insns = []
            continue

        # Instruction line: "  1149:   push   %rbp"
        insn_match = re.match(r'^\s+([0-9a-f]+):\s+(.+)', line)
        if insn_match and current_label:
            current_insns.append(f"  {insn_match.group(1)}: {insn_match.group(2).strip()}")

    if current_label and current_insns:
        blocks.append(_make_block(current_addr, current_label, current_insns))

    return blocks


def extract_blocks_ghidra(binary: Path) -> list[dict]:
    """
    Run Ghidra headless analysis and extract decompiled pseudocode blocks.
    Falls back to basic block extraction from the Ghidra listing output.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir  = Path(tmpdir) / "ghidra_project"
        project_dir.mkdir()
        script_path  = Path(tmpdir) / "ExtractBlocks.py"

        # Minimal Ghidra script to dump basic block pseudocode
        script_path.write_text(textwrap.dedent("""\
            # ExtractBlocks.py — Ghidra headless script
            from ghidra.app.decompiler import DecompInterface
            from ghidra.util.task import ConsoleTaskMonitor

            ifc = DecompInterface()
            ifc.openProgram(currentProgram)
            monitor = ConsoleTaskMonitor()

            listing = currentProgram.getListing()
            funcs   = list(currentProgram.getFunctionManager().getFunctions(True))

            for func in funcs:
                name = func.getName()
                if name.startswith("__") or name in ("_start", "frame_dummy"):
                    continue
                result = ifc.decompileFunction(func, 60, monitor)
                if result and result.decompiledFunction:
                    code = result.decompiledFunction.getC()
                    print("===FUNC:{}===".format(name))
                    print(code)
                    print("===END===")
        """))

        cmd = [
            str(GHIDRA_HEADLESS),
            str(project_dir), "TmpProject",
            "-import", str(binary),
            "-postScript", str(script_path),
            "-scriptPath", str(tmpdir),
            "-noanalysis",  # use default analysis
            "-deleteProject",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr

    # Parse func blocks from output
    blocks = []
    current_name  = None
    current_lines = []
    for line in output.splitlines():
        if line.startswith("===FUNC:"):
            current_name  = line[8:].rstrip("===").strip()
            current_lines = []
        elif line.startswith("===END===") and current_name:
            blocks.append(_make_block("ghidra", current_name, current_lines))
            current_name  = None
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)

    if not blocks:
        # Ghidra produced no parseable output — fall back to objdump
        print("[warn] Ghidra produced no parseable blocks; falling back to objdump")
        return extract_blocks_objdump(binary)

    return blocks


def _make_block(addr: str, label: str, insns: list[str]) -> dict:
    raw = "\n".join(insns)
    return {"addr": addr, "label": label, "instructions": insns, "raw_text": raw}


def extract_blocks(binary: Path, backend: str) -> list[dict]:
    if backend == "ghidra":
        return extract_blocks_ghidra(binary)
    return extract_blocks_objdump(binary)


def filter_to_interesting(blocks: list[dict]) -> list[dict]:
    """
    Keep only blocks that appear to contain real computational content.
    Filter out plt stubs, crt startup, and empty blocks.
    """
    skip_labels = {"_start", "frame_dummy", "__do_global_dtors_aux",
                   "__libc_csu_init", "__libc_csu_fini", "register_tm_clones",
                   "deregister_tm_clones"}
    skip_patterns = re.compile(r'^(\.plt|__|\.|_dl_|call_weak_fn)')

    filtered = []
    for b in blocks:
        if b["label"] in skip_labels:
            continue
        if skip_patterns.match(b["label"]):
            continue
        if len(b["instructions"]) < 2:
            continue
        filtered.append(b)
    return filtered


# ── Scoring ────────────────────────────────────────────────────────────────────

def score_response(response: str) -> float:
    """
    Returns a normalized convergence score in [0, 1].
    Higher = closer to correctly identifying sphere volume formula.
    """
    r = response.lower()
    total = 0.0
    for kw, weight in KEYWORD_WEIGHTS.items():
        if kw in r:
            total += weight
    return min(total / MAX_POSSIBLE_SCORE, 1.0)


def is_converged(response: str) -> bool:
    """True if the model has clearly identified sphere volume."""
    r = response.lower()
    return ("sphere" in r and "volume" in r) or ("4/3" in r) or ("4.0/3.0" in r)


# ── LLM inference ──────────────────────────────────────────────────────────────

def query_llm(model, tokenizer, blocks_text: str) -> str:
    prompt = QUERY_TEMPLATE.format(blocks=blocks_text)
    messages = [
        {"role": "system",  "content": SYSTEM_PROMPT},
        {"role": "user",    "content": prompt},
    ]
    ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    )
    if hasattr(ids, "input_ids"):
        ids = ids.input_ids
    ids = ids.to(DEVICE)

    with torch.no_grad():
        out = model.generate(
            ids,
            attention_mask=torch.ones_like(ids),
            max_new_tokens=MAX_NEW,
            do_sample=False,
            temperature=1.0,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = out[0, ids.shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


# ── Main ───────────────────────────────────────────────────────────────────────

print("=" * 70)
print("Experiment 09 — Disassembly Atlas")
print("=" * 70)
print()

# 1. Detect backend
backend = detect_backend()
print(f"[backend]  {backend}")

# 2. Check binary exists
if not BINARY_PATH.exists():
    print(f"\n[warn] Binary not found: {BINARY_PATH}")
    print("       Building from source...")
    src = EXPERIMENT_DIR / "sphere" / "sphere.cpp"
    result = subprocess.run(
        ["gcc", str(src), "-o", str(BINARY_PATH), "-lm", "-O1"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Build failed:\n{result.stderr}")
    print(f"       Built: {BINARY_PATH}")

print(f"[binary]   {BINARY_PATH}")
print()

# 3. Extract blocks
print("[disassembling...]")
all_blocks = extract_blocks(BINARY_PATH, backend)
interesting = filter_to_interesting(all_blocks)

print(f"[blocks]   {len(all_blocks)} total, {len(interesting)} computational")
print()
for i, b in enumerate(interesting):
    print(f"  Block {i:2d}  <{b['label']}>  ({len(b['instructions'])} instructions)")
print()

if not interesting:
    raise RuntimeError("No computational blocks found in binary.")

# 4. Load model
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

# 5. Atlas sweep — reveal blocks one at a time, accumulate
print("── Atlas sweep ──────────────────────────────────────────────────────")
print("   Revealing blocks one at a time. Measuring convergence to")
print("   sphere volume formula (V = 4/3·π·r³).")
print()
print(f"   {'N':>3}  {'blocks revealed':<22}  {'score':>6}  {'converged?':>10}  response")
print(f"   {'─'*78}")

results = []
converged_at = None

for n in range(1, len(interesting) + 1):
    visible = interesting[:n]
    blocks_text = "\n\n".join(
        f"[block {i}: <{b['label']}>]\n{b['raw_text']}"
        for i, b in enumerate(visible)
    )
    torch.cuda.empty_cache()
    response = query_llm(model, tokenizer, blocks_text)
    s        = score_response(response)
    conv     = is_converged(response)

    labels_shown = ", ".join(f"<{b['label']}>" for b in visible)
    conv_sym     = "✓ YES" if conv else "·"

    if conv and converged_at is None:
        converged_at = n

    print(f"   {n:>3}  {labels_shown:<22}  {s:>6.3f}  {conv_sym:>10}  "
          f"{response[:60].replace(chr(10), ' ')}")

    results.append(dict(
        n=n, labels=labels_shown, score=s, converged=conv, response=response
    ))

print()
if converged_at:
    print(f"[convergence]  Great circle reached at N = {converged_at} block(s).")
else:
    print(f"[convergence]  Model did not fully converge with {len(interesting)} blocks.")
    print(f"               Peak score: {max(r['score'] for r in results):.3f}")
print()

# 6. Plot — convergence curve
print("[generating atlas convergence plot...]")
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
fig.suptitle(
    "Experiment 09 — Disassembly Atlas: Local Charts → Global Intent",
    fontsize=12, fontweight="bold"
)

ns     = [r["n"]     for r in results]
scores = [r["score"] for r in results]
convs  = [r["converged"] for r in results]

# ── Panel 1: convergence curve ─────────────────────────────────────────────────
ax1.set_title("Atlas convergence: rhumb line → great circle", fontsize=10)
ax1.plot(ns, scores, color="#3498db", lw=2.5, marker="o", markersize=7,
         label="inference score", zorder=3)
ax1.axhline(y=0.0, color="#ecf0f1", lw=0.5)

# Mark convergence
for r in results:
    if r["converged"]:
        ax1.axvline(x=r["n"], color="#2ecc71", lw=1.5, linestyle="--", alpha=0.7,
                    label=f"converged (N={r['n']})" if r["n"] == converged_at else "")
        ax1.scatter([r["n"]], [r["score"]], color="#2ecc71", s=120, zorder=5, marker="*")

# Rhumb line annotation — first nonzero score
for r in results:
    if r["score"] > 0:
        ax1.annotate("rhumb line\n(first signal)",
                     xy=(r["n"], r["score"]),
                     xytext=(r["n"] + 0.3, r["score"] + 0.05),
                     fontsize=8, color="#e67e22",
                     arrowprops=dict(arrowstyle="->", color="#e67e22", lw=1.2))
        break

ax1.set_xlabel("Number of basic blocks revealed (N)", fontsize=9)
ax1.set_ylabel("Convergence score  (0 = noise,  1 = great circle)", fontsize=9)
ax1.set_xlim(0.5, len(interesting) + 0.5)
ax1.set_ylim(-0.05, 1.1)
ax1.set_xticks(ns)
ax1.legend(fontsize=8)
ax1.grid(axis="y", alpha=0.3)

# ── Panel 2: block charter — visual atlas map ──────────────────────────────────
ax2.set_title(f"Block atlas  (backend: {backend})", fontsize=10)

bar_colors = ["#2ecc71" if r["converged"] else "#3498db" for r in results]

bars = ax2.barh(
    [f"N={r['n']}  <{interesting[r['n']-1]['label']}>" for r in results],
    scores,
    color=bar_colors, edgecolor="#bdc3c7", height=0.6
)

for i, r in enumerate(results):
    ax2.text(
        r["score"] + 0.01, i,
        f"{r['score']:.3f}  {'← great circle' if r['converged'] else ''}",
        va="center", fontsize=7.5,
        color="#2ecc71" if r["converged"] else "#555"
    )

ax2.set_xlabel("Convergence score", fontsize=9)
ax2.set_xlim(0, 1.3)
ax2.invert_yaxis()
ax2.axvline(x=0, color="#bdc3c7", lw=0.5)

# Legend patches
rhumb_patch = mpatches.Patch(color="#3498db", label="partial signal (rhumb line)")
great_patch = mpatches.Patch(color="#2ecc71", label="convergence (great circle)")
ax2.legend(handles=[rhumb_patch, great_patch], fontsize=8, loc="lower right")

# Backend watermark
fig.text(0.01, 0.01,
         f"binary: sphere_asm  |  backend: {backend}  |  model: TinyLlama-1.1B-Chat",
         fontsize=7, color="#aaa")

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=130, bbox_inches="tight")
print(f"[saved]    {OUT_PNG}")
print()

# 7. Print full responses for deepest convergence point
best = max(results, key=lambda r: r["score"])
print("── Best inference ───────────────────────────────────────────────────")
print(f"   N = {best['n']}  blocks  |  score = {best['score']:.3f}")
print(f"   blocks: {best['labels']}")
print()
print("   Response:")
for line in best["response"].splitlines():
    print(f"     {line}")
print()
print("── Conway's method: local charts, global inference. ─────────────────")
print("   The destination was present in the local data.")
print("   Training revealed the geodesic that was already implied.")
print("=" * 70)
