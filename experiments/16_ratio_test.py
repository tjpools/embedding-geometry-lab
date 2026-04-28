"""
Experiment 16 — The Ratio Test
================================
A ratio test checks whether a tiny local signal is enough to separate two
global classes on the transformer manifold.

Formal definition:
  Given a concept pair (A, B), build representations at increasing token
  budgets t = 1, 2, 3, 5, 8, 13, 21 ... Measure L2(embed(A_t), embed(B_t))
  at each budget. Find the inflection point: the smallest t where L2 takes
  its largest single step. Report:

    inflection_token  — minimum sufficient signal
    L2_at_inflection  — separation achieved
    ratio             — L2_at_inflection / inflection_token  (boundary sharpness)

  A step-function curve (large ratio, early inflection) means the manifold
  has a crisp categorical boundary. A gradient curve means the distinction
  is diffuse or context-dependent.

Concept pair classes (5 domains, 4 pairs each = 20 pairs total):
  TYPE        — void/int, float/double, true/false, signed/unsigned
  NAVIGATION  — rhumb/geodesic, bearing/heading, knots/mph, chart/map
  PHILOSOPHY  — Leibniz/Newton, Berkeley/Hume, Riemann/Euclid, dx/delta_x
  COMPUTATION — recursive/iterative, compiled/interpreted, analog/digital, sync/async
  SCALE       — local/global, discrete/continuous, finite/infinite, serial/parallel

Each pair is built at 7 token budgets using a canonical scaffold:
  t=1   bare token A vs bare token B
  t=2   "A" vs "B"  (quoted, 1 meaningful + scaffolding)
  t=3   "A:" vs "B:"
  t=5   "concept: A." vs "concept: B."
  t=8   one-phrase description
  t=13  one-sentence definition
  t=21  two-sentence definition

The inflection point is the first budget where delta_L2 is maximized.

Prior results for calibration:
  Exp 13 — void vs int:     inflection ~2 tok, L2=40.15, ratio=20.1
  Exp 14 — function name:   inflection ~4 tok, L2=35.13, ratio=8.8
  Exp 15 — nav strategy:    inflection ~5 tok, L2=20.96, ratio=4.2

Thesis connection:
  The ratio test IS the instrument panel reading.
  High ratio = crisp manifold boundary = transformer recognizes, not computes.
  Low ratio = diffuse boundary = transformer needs more context to locate the chart.
  The ratio ranks concept classes by categorical sharpness in the learned manifold.
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

warnings.filterwarnings("ignore")

# ── Configuration ─────────────────────────────────────────────────────────────
MODEL_ID   = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"
ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# ── Concept pairs by class ────────────────────────────────────────────────────
# Each entry: (label, A, B, phrase_A, phrase_B, sentence_A, sentence_B)
# phrase  = ~5 tok description
# sentence = ~13 tok definition
# 2sentence = ~21 tok

CONCEPT_PAIRS = {
    "TYPE": [
        ("void/int",
         "void", "int",
         "concept: void.", "concept: int.",
         "void is the absence of a return value.",
         "int is an integer numeric type.",
         "void signals no value is returned by the function. It encodes absence.",
         "int encodes a signed integer value. It encodes presence of quantity."),
        ("float/double",
         "float", "double",
         "concept: float.", "concept: double.",
         "float is single-precision floating point.",
         "double is double-precision floating point.",
         "float stores 32-bit IEEE floating point. Precision is limited.",
         "double stores 64-bit IEEE floating point. Precision is extended."),
        ("true/false",
         "true", "false",
         "concept: true.", "concept: false.",
         "true is the Boolean affirmative value.",
         "false is the Boolean negative value.",
         "true encodes logical affirmation. The condition holds.",
         "false encodes logical negation. The condition does not hold."),
        ("signed/unsigned",
         "signed", "unsigned",
         "concept: signed.", "concept: unsigned.",
         "signed encodes negative and positive integers.",
         "unsigned encodes only non-negative integers.",
         "signed integers use one bit for the sign, allowing negative values.",
         "unsigned integers use all bits for magnitude, doubling positive range."),
    ],
    "NAVIGATION": [
        ("rhumb/geodesic",
         "rhumb", "geodesic",
         "path: rhumb line.", "path: geodesic.",
         "rhumb is a path of constant bearing.",
         "geodesic is the shortest path on a sphere.",
         "rhumb line holds constant bearing but is not the shortest path on Earth.",
         "geodesic follows Earth curvature and is the shortest path between two points."),
        ("bearing/heading",
         "bearing", "heading",
         "nav: bearing.", "nav: heading.",
         "bearing is direction to a fixed reference.",
         "heading is the direction the aircraft points.",
         "bearing is the angle to a target measured from north.",
         "heading is the direction the nose of the aircraft points at this moment."),
        ("knots/mph",
         "knots", "mph",
         "speed: knots.", "speed: mph.",
         "knots are nautical miles per hour.",
         "mph are statute miles per hour.",
         "knots measure speed in nautical miles per hour, native to sphere geometry.",
         "mph measure speed in statute miles per hour, native to flat-Earth roads."),
        ("chart/map",
         "chart", "map",
         "nav: chart.", "nav: map.",
         "chart is a navigational instrument.",
         "map is a flat representation of terrain.",
         "nautical chart encodes depth, hazards, and bearing references for navigation.",
         "map encodes terrain features on a flat projection, losing curvature information."),
    ],
    "PHILOSOPHY": [
        ("Leibniz/Newton",
         "Leibniz", "Newton",
         "thinker: Leibniz.", "thinker: Newton.",
         "Leibniz invented the calculus notation dx.",
         "Newton invented the calculus notation for fluxions.",
         "Leibniz developed the differential operator dx as pure syntax, independent of physics.",
         "Newton developed fluxions as rates of change tied to physical motion and time."),
        ("Berkeley/Hume",
         "Berkeley", "Hume",
         "thinker: Berkeley.", "thinker: Hume.",
         "Berkeley attacked the infinitesimal as contradiction.",
         "Hume attacked causation as mere habit of mind.",
         "Berkeley showed the infinitesimal was formally contradictory, demanding rigorous foundations.",
         "Hume showed causation cannot be derived from observation, only from habit and expectation."),
        ("Riemann/Euclid",
         "Riemann", "Euclid",
         "geometer: Riemann.", "geometer: Euclid.",
         "Riemann built geometry on curved surfaces.",
         "Euclid built geometry on flat parallel lines.",
         "Riemann defined geometry intrinsically on curved manifolds using the metric tensor.",
         "Euclid defined geometry extrinsically on flat planes using five postulates."),
        ("dx/Δx",
         "dx", "Δx",
         "operator: dx.", "operator: Δx.",
         "dx is the infinitesimal differential operator.",
         "Δx is the finite difference operator.",
         "dx encodes instantaneous local change as an operator, enabling the chain rule.",
         "Δx encodes finite difference between two states, without local structure."),
    ],
    "COMPUTATION": [
        ("recursive/iterative",
         "recursive", "iterative",
         "method: recursive.", "method: iterative.",
         "recursive calls itself to reduce the problem.",
         "iterative uses a loop to reduce the problem.",
         "recursive decomposition reduces a problem by self-reference until a base case.",
         "iterative decomposition reduces a problem by repeating a loop until termination."),
        ("compiled/interpreted",
         "compiled", "interpreted",
         "exec: compiled.", "exec: interpreted.",
         "compiled translates source to machine code ahead of time.",
         "interpreted translates source to machine code at runtime.",
         "compiled code is translated to native instructions before execution, maximising speed.",
         "interpreted code is translated line by line at runtime, maximising flexibility."),
        ("analog/digital",
         "analog", "digital",
         "signal: analog.", "signal: digital.",
         "analog encodes continuous values.",
         "digital encodes discrete values.",
         "analog signals are continuous functions of time, encoding infinite resolution.",
         "digital signals are discrete samples in time, encoding finite resolution."),
        ("sync/async",
         "sync", "async",
         "exec: sync.", "exec: async.",
         "sync waits for each operation to complete.",
         "async does not wait for each operation to complete.",
         "synchronous execution blocks until the current operation returns a result.",
         "asynchronous execution continues without blocking, handling results when ready."),
    ],
    "SCALE": [
        ("local/global",
         "local", "global",
         "scope: local.", "scope: global.",
         "local applies to the immediate neighborhood.",
         "global applies to the entire system.",
         "local scope means the property holds in the current neighborhood or frame.",
         "global scope means the property holds across the entire system or manifold."),
        ("discrete/continuous",
         "discrete", "continuous",
         "math: discrete.", "math: continuous.",
         "discrete consists of distinct countable elements.",
         "continuous consists of uncountably many elements.",
         "discrete mathematics counts distinct separable objects with no values between.",
         "continuous mathematics measures quantities that vary without gaps or jumps."),
        ("finite/infinite",
         "finite", "infinite",
         "quantity: finite.", "quantity: infinite.",
         "finite has a definite bound.",
         "infinite has no bound.",
         "finite quantities can be measured, counted, and bounded by a real number.",
         "infinite quantities have no upper bound; they exceed every finite measure."),
        ("serial/parallel",
         "serial", "parallel",
         "exec: serial.", "exec: parallel.",
         "serial executes one operation at a time.",
         "parallel executes multiple operations simultaneously.",
         "serial execution processes one instruction at a time in strict sequence.",
         "parallel execution processes multiple instructions simultaneously across cores."),
    ],
}

# Token budget levels — label and how to build the text
# (label, text_fn(A_terms, B_terms))
# A_terms = (bare, quoted, phrase, sentence, sentence2)
def build_levels(bare_a, bare_b, phrase_a, phrase_b, sent_a, sent_b, sent2_a, sent2_b):
    return [
        ("bare",     bare_a,                        bare_b),
        ("quoted",   f'"{bare_a}"',                 f'"{bare_b}"'),
        ("tagged",   f'{bare_a}:',                  f'{bare_b}:'),
        ("phrase",   phrase_a,                      phrase_b),
        ("sentence", sent_a,                        sent_b),
        ("extended", f"{sent_a} {sent2_a}",         f"{sent_b} {sent2_b}"),
    ]

LEVEL_NAMES = ["bare", "quoted", "tagged", "phrase", "sentence", "extended"]

# ── Model loading ─────────────────────────────────────────────────────────────
print("=" * 70)
print("Experiment 16 — The Ratio Test")
print("=" * 70)
print()
print(f"  Concept classes:  {len(CONCEPT_PAIRS)}")
print(f"  Pairs per class:  4")
print(f"  Token levels:     {len(LEVEL_NAMES)}")
print(f"  Total embeddings: {len(CONCEPT_PAIRS) * 4 * len(LEVEL_NAMES) * 2}")
print()
print(f"Loading {MODEL_ID} …")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.float16,
    device_map=DEVICE,
    attn_implementation="eager",
)
model.eval()
print("Model ready.")
print()

# ── Embedding function ─────────────────────────────────────────────────────────
@torch.no_grad()
def embed(text):
    ids = tokenizer(text, return_tensors="pt").input_ids.to(DEVICE)
    out = model(ids, output_hidden_states=True)
    h   = out.hidden_states[-1][0]
    return h.mean(dim=0).float().cpu().numpy(), ids.shape[1]

# ── Run all pairs ──────────────────────────────────────────────────────────────
print("Computing embeddings …")
results = {}   # (class, pair_label) → {level: (l2, tok_a, tok_b)}

for cls_name, pairs in CONCEPT_PAIRS.items():
    for (pair_label, bare_a, bare_b,
         phrase_a, phrase_b, sent_a, sent_b, sent2_a, sent2_b) in pairs:

        levels = build_levels(bare_a, bare_b, phrase_a, phrase_b,
                              sent_a, sent_b, sent2_a, sent2_b)
        level_results = {}
        prev_l2 = None

        for (lv_name, text_a, text_b) in levels:
            emb_a, tok_a = embed(text_a)
            emb_b, tok_b = embed(text_b)
            l2 = float(np.linalg.norm(emb_a - emb_b))
            avg_tok = (tok_a + tok_b) / 2
            level_results[lv_name] = (l2, tok_a, tok_b, avg_tok)

        results[(cls_name, pair_label)] = level_results
        # Quick progress line
        l2s = [v[0] for v in level_results.values()]
        toks = [v[3] for v in level_results.values()]
        peak_l2  = max(l2s)
        peak_lv  = LEVEL_NAMES[int(np.argmax(l2s))]
        peak_tok = toks[int(np.argmax(l2s))]
        print(f"  {cls_name:<12}  {pair_label:<18}  "
              f"peak L2={peak_l2:5.1f} @ {peak_lv} ({peak_tok:.0f} tok)")

print()

# ── Compute ratio metrics ──────────────────────────────────────────────────────
print("=" * 70)
print("RATIO ANALYSIS")
print("=" * 70)
print()

ratio_table = []   # (cls, pair, inflection_level, inflection_tok, l2_at_inf, ratio, step_size)

for (cls_name, pair_label), level_results in results.items():
    l2s  = [level_results[lv][0] for lv in LEVEL_NAMES]
    toks = [level_results[lv][3] for lv in LEVEL_NAMES]

    # Inflection = level with maximum L2 step (delta)
    deltas = [l2s[i] - l2s[i-1] for i in range(1, len(l2s))]
    inf_idx = int(np.argmax(deltas)) + 1  # +1 because deltas[0] = l2s[1]-l2s[0]
    inf_l2  = l2s[inf_idx]
    inf_tok = toks[inf_idx]
    inf_lv  = LEVEL_NAMES[inf_idx]
    step    = deltas[inf_idx - 1]
    ratio   = inf_l2 / inf_tok if inf_tok > 0 else 0.0

    ratio_table.append((cls_name, pair_label, inf_lv, inf_tok, inf_l2, ratio, step))

# Sort by ratio descending
ratio_table.sort(key=lambda r: r[5], reverse=True)

print(f"  {'Class':<12}  {'Pair':<18}  {'Inflection':<10}  "
      f"{'Tok':>4}  {'L2':>6}  {'Ratio':>7}  {'Step':>6}")
print(f"  {'-'*12}  {'-'*18}  {'-'*10}  {'-'*4}  {'-'*6}  {'-'*7}  {'-'*6}")

for (cls_name, pair_label, inf_lv, inf_tok, inf_l2, ratio, step) in ratio_table:
    bar = "█" * min(int(ratio), 25)
    print(f"  {cls_name:<12}  {pair_label:<18}  {inf_lv:<10}  "
          f"{inf_tok:4.0f}  {inf_l2:6.1f}  {ratio:7.2f}  {step:6.1f}  {bar}")

print()

# Class-level summary
print("Class summary (mean ratio):")
class_ratios = {}
for (cls_name, pair_label, inf_lv, inf_tok, inf_l2, ratio, step) in ratio_table:
    class_ratios.setdefault(cls_name, []).append(ratio)

class_summary = sorted([(cls, np.mean(rs)) for cls, rs in class_ratios.items()],
                        key=lambda x: x[1], reverse=True)
for cls, mean_ratio in class_summary:
    bar = "█" * min(int(mean_ratio), 25)
    print(f"  {cls:<12}  mean ratio = {mean_ratio:6.2f}  {bar}")
print()

# ── Plotting ───────────────────────────────────────────────────────────────────
CLASS_COLORS = {
    "TYPE":        "#ff7b72",
    "NAVIGATION":  "#79c0ff",
    "PHILOSOPHY":  "#ffa657",
    "COMPUTATION": "#7ee787",
    "SCALE":       "#d2a8ff",
}

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor("#0d1117")
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

ax_curves  = fig.add_subplot(gs[0, :2])   # L2 curves — wide
ax_ratios  = fig.add_subplot(gs[0, 2])    # ratio bar chart
ax_heatmap = fig.add_subplot(gs[1, :2])   # class × level heatmap
ax_txt     = fig.add_subplot(gs[1, 2])    # summary text

TEXT_COL = "#c9d1d9"
for ax in [ax_curves, ax_ratios, ax_heatmap, ax_txt]:
    ax.set_facecolor("#161b22")
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

# Panel 1: L2 curves per pair, coloured by class
x_ticks = list(range(len(LEVEL_NAMES)))
for (cls_name, pair_label), level_results in results.items():
    l2s = [level_results[lv][0] for lv in LEVEL_NAMES]
    col = CLASS_COLORS[cls_name]
    ax_curves.plot(x_ticks, l2s, '-o', color=col, alpha=0.55, linewidth=1.2,
                   markersize=3)

# Class legend
for cls, col in CLASS_COLORS.items():
    ax_curves.plot([], [], color=col, linewidth=2, label=cls)

ax_curves.set_xticks(x_ticks)
ax_curves.set_xticklabels(LEVEL_NAMES, color=TEXT_COL, fontsize=8)
ax_curves.set_ylabel("L2 distance", color=TEXT_COL, fontsize=8)
ax_curves.set_title("L2 Curves by Token Level — All 20 Pairs", color=TEXT_COL,
                    fontsize=10, pad=8)
ax_curves.tick_params(colors=TEXT_COL)
ax_curves.legend(fontsize=7, facecolor="#21262d", labelcolor=TEXT_COL,
                 edgecolor="#30363d", loc="upper right", ncol=2)

# Panel 2: Ratio bar chart (top 20, sorted)
pair_labels = [f"{r[0][:4]} {r[1][:12]}" for r in ratio_table]
ratios      = [r[5] for r in ratio_table]
colors      = [CLASS_COLORS[r[0]] for r in ratio_table]

y_pos = np.arange(len(pair_labels))
ax_ratios.barh(y_pos, ratios, color=colors, alpha=0.8, edgecolor="#30363d")
ax_ratios.set_yticks(y_pos)
ax_ratios.set_yticklabels(pair_labels, color=TEXT_COL, fontsize=6)
ax_ratios.set_xlabel("L2 / token ratio", color=TEXT_COL, fontsize=8)
ax_ratios.set_title("Boundary Sharpness Ranking", color=TEXT_COL, fontsize=10, pad=8)
ax_ratios.tick_params(colors=TEXT_COL)
ax_ratios.invert_yaxis()

# Panel 3: Heatmap — class × level, mean L2
heat_data = np.zeros((len(CLASS_COLORS), len(LEVEL_NAMES)))
cls_list  = list(CLASS_COLORS.keys())

for (cls_name, pair_label), level_results in results.items():
    ci = cls_list.index(cls_name)
    for li, lv in enumerate(LEVEL_NAMES):
        heat_data[ci, li] += level_results[lv][0]

# Average over 4 pairs per class
heat_data /= 4.0

im = ax_heatmap.imshow(heat_data, aspect="auto", cmap="viridis",
                        interpolation="nearest")
ax_heatmap.set_xticks(range(len(LEVEL_NAMES)))
ax_heatmap.set_xticklabels(LEVEL_NAMES, color=TEXT_COL, fontsize=8, rotation=20, ha="right")
ax_heatmap.set_yticks(range(len(cls_list)))
ax_heatmap.set_yticklabels(cls_list, color=TEXT_COL, fontsize=8)
ax_heatmap.set_title("Mean L2 by Class × Level", color=TEXT_COL, fontsize=10, pad=8)
ax_heatmap.tick_params(colors=TEXT_COL)
plt.colorbar(im, ax=ax_heatmap, label="mean L2").ax.yaxis.label.set_color(TEXT_COL)

# Panel 4: Summary text
ax_txt.axis("off")
summary = "Ratio Test Results\n" + "─"*32 + "\n"
summary += f"{'Class':<12}  {'Mean Ratio':>10}\n"
summary += "─"*32 + "\n"
for cls, mean_ratio in class_summary:
    bar = "█" * min(int(mean_ratio / 2), 12)
    summary += f"{cls:<12}  {mean_ratio:>10.2f}  {bar}\n"

summary += "\n" + "─"*32 + "\n"
summary += "Top 5 sharpest boundaries:\n"
for r in ratio_table[:5]:
    summary += f"  {r[1]:<16} {r[5]:.2f}\n"

summary += "\n" + "─"*32 + "\n"
summary += "Prior calibration:\n"
summary += "  void/int (exp13)  20.1\n"
summary += "  func name (exp14)  8.8\n"
summary += "  nav strat (exp15)  4.2\n"
summary += "\n"
summary += "Step-function = crisp boundary.\nGradient = diffuse boundary.\n"
summary += "High ratio = recognition.\nLow ratio = computation needed."

ax_txt.text(0.03, 0.97, summary, transform=ax_txt.transAxes,
            color=TEXT_COL, fontsize=7, fontfamily="monospace",
            verticalalignment="top", linespacing=1.5)

fig.suptitle(
    "Experiment 16 — The Ratio Test\n"
    "Manifold boundary sharpness: L2 / token at inflection point",
    color=TEXT_COL, fontsize=11, y=0.99
)

out_path = ASSETS_DIR / "16_ratio_test.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Plot saved → {out_path}")
print()

# ── Interpretation ─────────────────────────────────────────────────────────────
print("=" * 70)
print("INTERPRETATION")
print("=" * 70)
print()
print("  The ratio test measures manifold boundary sharpness:")
print("  L2_at_inflection / inflection_token = how crisp the categorical split is.")
print()
print("  Step-function signature: inflection is early, delta is large.")
print("  Gradient signature:      L2 drifts upward, no single jump.")
print()
print("  Class ranking (mean ratio, high = crisp boundary):")
for cls, mean_ratio in class_summary:
    print(f"    {cls:<12}  {mean_ratio:.2f}")
print()
print("  Thesis connection:")
print("    High ratio = recognition. The manifold already has the chart.")
print("    Low ratio  = the transformer needs context to locate the chart.")
print("    The physics engine integrates. The transformer recognises.")
print("    The ratio test measures which side of that boundary each concept pair is on.")
print("=" * 70)
