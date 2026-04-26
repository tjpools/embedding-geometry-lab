#!/usr/bin/env python3
"""
Experiment 08 — Anchor Interference
=================================================================================
Two competing memory anchors planted in a ~1600-token context:

    ZENITH  at token position  0  (always)
    NADIR   at token position  k  (sweeps across [0, 100, 400, 800, 1200, 1500])

For each k, two separate queries are issued at the end of the context:
    Q1: "What was the FIRST special word I mentioned?"  → expect ZENITH
    Q2: "What was the LAST special word I mentioned?"   → expect NADIR

Four possible routing outcomes per k:
    (✓, ✓)  dual     — score matrix discriminates both attractors
    (✓, ✗)  primacy  — recency path collapsed (NADIR lost)
    (✗, ✓)  recency  — primacy path collapsed (ZENITH lost)
    (✗, ✗)  collapse — total routing failure

This distinguishes two failure modes:
    A. Both anchors encoded; query underspecification causes confusion
    B. One attractor overwrites the other in the routing graph

Geometric connection:
    From Exp 07:  VRAM(n) = 2.438e-4·n² + 0.0494·n + 2108.8
                  n² dominates for n > 101, equals linear at n ≈ 203
    Here n is fixed (~1600). The variable is attractor *separation* — the
    positional distance between ZENITH and NADIR in the context graph.
    As separation decreases, routing must discriminate increasingly similar
    positional embeddings. The score matrix is being asked to resolve two
    attractors on the same curved manifold.

Thesis crystallizer:
    Geometry (n² attention) and semantics (anchor competition) converge
    to the same object: routing discrimination on a curved manifold.
    Failure is not a matter of context length — it is a matter of whether
    the score matrix can resolve two nearby attractors.
=================================================================================
"""

import os
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

transformers.logging.set_verbosity_error()

# ── Constants ──────────────────────────────────────────────────────────────────
MODEL_ID    = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE      = "cuda"
DTYPE       = torch.float16
MAX_NEW     = 150
TARGET_CTX  = 1600        # total prompt tokens, fixed across all k

K_POSITIONS = [0, 100, 400, 800, 1200, 1500]

FILLER_UNIT = (
    "The weather today is mild and unremarkable. "
    "A gentle wind moves through the trees outside. "
    "The temperature is moderate and the sky is partly cloudy. "
    "Nothing of particular significance is happening at this moment. "
)

SYSTEM_PROMPT = (
    "You are a helpful assistant with a perfect memory for all special words "
    "mentioned in the conversation. When asked about special words, you recall "
    "them precisely and completely."
)

ANCHOR_A_TEXT = "The FIRST special word for this conversation is: ZENITH."
ANCHOR_B_TEXT = "The LAST special word for this conversation is: NADIR."

QUERY_FIRST = (
    "I introduced exactly two special words in this conversation. "
    "What was the very FIRST special word I mentioned, at the very beginning? "
    "Answer with just that word."
)
QUERY_LAST = (
    "I introduced exactly two special words in this conversation. "
    "What was the very LAST special word I mentioned, most recently before this question? "
    "Answer with just that word."
)

# From Exp 07 quadratic fit
QUAD_A = 2.438e-4   # MB / tok²
QUAD_B = 0.0494     # MB / tok
N_STAR = QUAD_B / QUAD_A   # n where n² term equals linear term (~203)

OUT_PNG  = os.path.join(os.path.dirname(__file__), "assets", "08_anchor_interference.png")

COLOR = {
    "dual":         "#2ecc71",   # green  — both recalled
    "primacy wins": "#3498db",   # blue   — ZENITH only
    "recency wins": "#e67e22",   # orange — NADIR only
    "collapse":     "#e74c3c",   # red    — neither recalled
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def score_first(r: str) -> bool:
    return "zenith" in r.lower()

def score_last(r: str) -> bool:
    return "nadir" in r.lower()

def build_prompt(tokenizer, k_target: int, query: str) -> torch.Tensor:
    """
    Builds a chat-template prompt with:
      [ZENITH anchor] [filler × n_ab] [NADIR anchor] [filler × n_ba] [query]
    Total token count ≈ TARGET_CTX.
    k_target controls the approximate token position of NADIR.
    """
    filler_ids = tokenizer.encode(FILLER_UNIT, add_special_tokens=False)
    len_f = len(filler_ids)
    len_a = len(tokenizer.encode(ANCHOR_A_TEXT, add_special_tokens=False))
    len_b = len(tokenizer.encode(ANCHOR_B_TEXT, add_special_tokens=False))
    len_q = len(tokenizer.encode(query,         add_special_tokens=False))

    # Chat template overhead for TinyLlama system+user turn ≈ 35 tokens
    overhead = 35

    # Filler between anchors: fill from end-of-A to k_target
    gap = max(0, k_target - len_a)
    n_fill_ab = max(0, gap // len_f)

    # Filler after NADIR: fill remaining budget
    used = overhead + len_a + n_fill_ab * len_f + len_b + len_q
    n_fill_ba = max(0, (TARGET_CTX - used) // len_f)

    parts = [ANCHOR_A_TEXT]
    if n_fill_ab > 0:
        parts.append(" ".join([FILLER_UNIT] * n_fill_ab))
    parts.append(ANCHOR_B_TEXT)
    if n_fill_ba > 0:
        parts.append(" ".join([FILLER_UNIT] * n_fill_ba))
    parts.append(query)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": " ".join(parts)},
    ]
    ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    )
    if hasattr(ids, "input_ids"):
        ids = ids.input_ids
    return ids.to(DEVICE)

def run_probe(model, tokenizer, k: int, query: str, scorer):
    """Returns (correct: bool, response: str, actual_len: int, peak_vram_mb: float)."""
    torch.cuda.empty_cache()
    ids  = build_prompt(tokenizer, k, query)
    attn = torch.ones_like(ids)
    actual_len = ids.shape[1]

    torch.cuda.reset_peak_memory_stats()
    with torch.no_grad():
        out = model.generate(
            ids,
            attention_mask=attn,
            max_new_tokens=MAX_NEW,
            do_sample=False,
            temperature=1.0,
            pad_token_id=tokenizer.eos_token_id,
        )
    peak_vram = torch.cuda.max_memory_allocated() / (1024 ** 2)

    new_tokens = out[0, ids.shape[1]:]
    response   = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    correct    = scorer(response)
    return correct, response, actual_len, peak_vram

# ── Load model ─────────────────────────────────────────────────────────────────
print("=" * 70)
print("Experiment 08 — Anchor Interference")
print("=" * 70)
print()
print("[loading model...]")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, torch_dtype=DTYPE, device_map=DEVICE,
    attn_implementation="eager",
)
model.eval()
torch.cuda.empty_cache()
weights_mb = torch.cuda.memory_allocated() / (1024 ** 2)
print(f"[ready on CUDA]  weights: {weights_mb:.1f} MB VRAM\n")

# ── Interference sweep ─────────────────────────────────────────────────────────
print("── Anchor interference sweep ────────────────────────────────────────")
print(f"   ZENITH at position  0  (fixed)")
print(f"   NADIR  at position  k  (swept)")
print(f"   Total context: ~{TARGET_CTX} tokens per trial  (fixed)")
print(f"   Q1: first special word?  →  expect ZENITH")
print(f"   Q2: last special word?   →  expect NADIR")
print()
print(f"   {'k':>5}  {'actual':>6}  {'d(Z)':>5}  {'d(N)':>5}  {'Q1':>4}  {'Q2':>4}  {'routing':<18}  VRAM")
print(f"   {'─'*72}")

results = []
for k in K_POSITIONS:
    first_ok, resp_first, actual_len, vram_f = run_probe(
        model, tokenizer, k, QUERY_FIRST, score_first
    )
    last_ok,  resp_last,  _,          vram_l = run_probe(
        model, tokenizer, k, QUERY_LAST,  score_last
    )

    d_zenith = actual_len            # distance from ZENITH to query end
    d_nadir  = actual_len - k        # distance from NADIR  to query end

    if   first_ok and last_ok:  routing = "dual"
    elif first_ok:              routing = "primacy wins"
    elif last_ok:               routing = "recency wins"
    else:                       routing = "collapse"

    sym_f = "✓" if first_ok else "✗"
    sym_l = "✓" if last_ok  else "✗"
    vram  = max(vram_f, vram_l)

    print(f"   {k:>5}  {actual_len:>6}  {d_zenith:>5}  {d_nadir:>5}  "
          f"{sym_f:>4}  {sym_l:>4}  {routing:<18}  {vram:.1f} MB")
    print(f"         [Q1/first] {resp_first[:88]}")
    print(f"         [Q2/last ] {resp_last[:88]}")
    print()

    results.append(dict(
        k=k, actual=actual_len, d_zenith=d_zenith, d_nadir=d_nadir,
        first_ok=first_ok, last_ok=last_ok, routing=routing,
        resp_first=resp_first, resp_last=resp_last, vram=vram,
    ))

# ── Plot ───────────────────────────────────────────────────────────────────────
print("[generating anchor interference plot...]")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
fig.suptitle(
    "Experiment 08 — Anchor Interference: Routing on a Curved Manifold",
    fontsize=12, fontweight="bold"
)

# ── Panel 1: context timeline showing anchor positions ─────────────────────────
ax1.set_title("Context layout and routing outcome per k", fontsize=10)

for i, r in enumerate(results):
    y = i
    # full context bar
    ax1.barh(y, r["actual"], color="#ecf0f1", edgecolor="#bdc3c7", height=0.55, left=0)
    # ZENITH marker
    ax1.scatter([5], [y], color="#3498db", s=100, zorder=5, marker="^",
                label="ZENITH (pos 0)" if i == 0 else "")
    # NADIR marker
    nadir_x = max(r["k"], 10)
    ax1.scatter([nadir_x], [y], color="#e67e22", s=100, zorder=5, marker="v",
                label="NADIR (pos k)"  if i == 0 else "")
    # Separator line between the two anchors
    if r["k"] > 0:
        ax1.annotate("", xy=(nadir_x, y), xytext=(5, y),
                     arrowprops=dict(arrowstyle="-", color="#95a5a6",
                                     lw=1, linestyle="dashed"))
    # outcome badge
    outcome = ("✓✓" if r["first_ok"] and r["last_ok"] else
               "✓✗" if r["first_ok"] else
               "✗✓" if r["last_ok"]  else "✗✗")
    ax1.text(r["actual"] + 15, y, outcome, va="center", fontsize=11,
             color=COLOR[r["routing"]], fontweight="bold")
    # routing label
    ax1.text(-20, y, f"k={r['k']:4d}", va="center", ha="right", fontsize=8,
             color="#555")

ax1.set_yticks([])
ax1.set_xlabel("Token position in context", fontsize=9)
ax1.set_xlim(-120, TARGET_CTX + 80)
ax1.set_ylim(-0.6, len(results) - 0.4)
ax1.invert_yaxis()
ax1.legend(loc="lower right", fontsize=8)

# Annotate quadratic crossover from Exp 07
ax1.axvline(N_STAR, color="#9b59b6", lw=1.2, linestyle=":", alpha=0.7,
            label=f"n*={N_STAR:.0f} (quadratic crossover)")
ax1.text(N_STAR + 5, len(results) - 0.6,
         f"n*≈{N_STAR:.0f}\n(n² crossover)", fontsize=7,
         color="#9b59b6", va="bottom")

# ── Panel 2: recall accuracy vs attractor distance from query ─────────────────
ax2.set_title("Recall accuracy vs NADIR distance from query end", fontsize=10)

d_nadirs = [r["d_nadir"]  for r in results]
first_sc = [1 if r["first_ok"] else 0 for r in results]
last_sc  = [1 if r["last_ok"]  else 0 for r in results]

ax2.plot(d_nadirs, first_sc, "o-", color="#3498db",
         label="Q1: first  (ZENITH, always ~1600 away)", lw=2, ms=9, zorder=4)
ax2.plot(d_nadirs, last_sc,  "s-", color="#e67e22",
         label="Q2: last   (NADIR, distance varies)",    lw=2, ms=9, zorder=4)

# Color band per outcome
for r in results:
    x = r["d_nadir"]
    ax2.axvspan(x - 55, x + 55, alpha=0.12, color=COLOR[r["routing"]], zorder=2)

ax2.set_xlabel("Token distance: NADIR → query end  (right = close to query)", fontsize=9)
ax2.set_ylabel("Recall accuracy (binary)", fontsize=9)
ax2.set_ylim(-0.25, 1.4)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(["wrong (0)", "correct (1)"])
ax2.invert_xaxis()  # left=far from query, right=close

# Routing legend
patches = [mpatches.Patch(color=v, label=k) for k, v in COLOR.items()]
legend_queries = ax2.legend(loc="upper right", fontsize=8)
ax2.legend(handles=patches, fontsize=8, loc="upper left")
ax2.add_artist(legend_queries)

# Annotate the ZENITH distance reference
ax2.axhline(1, color="#aaa", lw=0.8, linestyle="--", zorder=1)
ax2.text(d_nadirs[-1] + 30, 1.05, "perfect", fontsize=7, color="#aaa")

plt.tight_layout()
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved: {OUT_PNG}\n")

# ── Summary ────────────────────────────────────────────────────────────────────
print("=" * 70)
print("Summary — Anchor Interference")
print("=" * 70)
print()
print(f"  {'k':>5}  {'d(ZENITH)':>9}  {'d(NADIR)':>8}  {'Q1':>4}  {'Q2':>4}  routing")
print(f"  {'─'*55}")
for r in results:
    sym_f = "✓" if r["first_ok"] else "✗"
    sym_l = "✓" if r["last_ok"]  else "✗"
    print(f"  {r['k']:>5}  {r['d_zenith']:>9}  {r['d_nadir']:>8}  "
          f"{sym_f:>4}  {sym_l:>4}  {r['routing']}")
print()

# Find crossover
dual_all = all(r["first_ok"] and r["last_ok"] for r in results)
if dual_all:
    print("  All probes: dual routing success (✓✓) across all k.")
    print("  Both attractors discriminated at every tested separation.")
    print()
    print("  Interpretation: the score matrix resolves two competing attractors")
    print("  even when both are ancient (k=0) or maximally separated (k=1500).")
    print("  Routing failure within 1600 tokens requires more than anchor spacing.")
else:
    first_non_dual = next((r for r in results if r["routing"] != "dual"), None)
    if first_non_dual:
        print(f"  First non-dual result at k={first_non_dual['k']}: {first_non_dual['routing']}")
        print(f"  NADIR distance from query at failure: {first_non_dual['d_nadir']} tokens")
    # Pattern analysis
    primacy_only = [r for r in results if r["routing"] == "primacy wins"]
    recency_only = [r for r in results if r["routing"] == "recency wins"]
    collapses    = [r for r in results if r["routing"] == "collapse"]
    if recency_only:
        print(f"  Recency wins at k = {[r['k'] for r in recency_only]}")
        print("  → ZENITH path collapsed when NADIR was farther from query.")
    if primacy_only:
        print(f"  Primacy wins at k = {[r['k'] for r in primacy_only]}")
    if collapses:
        print(f"  Routing collapse at k = {[r['k'] for r in collapses]}")
        print("  → Both attractors lost. Score matrix failed to route either path.")

print()
print(f"  Quadratic crossover (from Exp 07): n* ≈ {N_STAR:.0f} tokens")
print(f"  n² term has dominated VRAM for every token in this context.")
print()
print("  Two attractors. One manifold.")
print("  The question is not whether the manifold curves —")
print("  it is whether the curvature resolves or conflates.")
print("=" * 70)
