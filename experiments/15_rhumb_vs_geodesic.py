"""
Experiment 15 — Rhumb Line vs Geodesic: SFO → HND
====================================================
The opening story of "The Book": fly from San Francisco to Tokyo.
Your pocket ruler says west. The instrument panel says northwest.

Two navigation strategies:
  Rhumb line  — constant bearing, Mercator flat-Earth assumption (e^I, no update)
  Geodesic    — great circle, sphere curvature corrected (Jacobian, local update)

Physical ground truth:
  SFO: 37.6213°N, 122.3790°W
  HND: 35.5494°N, 139.7798°E

  Rhumb:    ~5,195 NM  bearing ~263° (due west, slight south)
  Geodesic: ~4,468 NM  bearing ~316° (northwest, over Alaska)
  Delta:    ~727 NM shorter on geodesic  (~14% savings)

Probe question: does the transformer manifold separate these two navigation
strategies? At what representation level does separation emerge?

Representation levels (5):
  0  coords      — raw lat/lon pair only
  1  bearing     — bearing + distance string
  2  waypoints   — 5-point route description
  3  prose       — navigation instruction paragraph
  4  reasoning   — full rhumb-vs-geodesic explanation

The philosophical connection:
  Rhumb = e^I path: uniform, no differential structure, no curvature update.
  Geodesic = Jacobian path: local correction at each step.
  The manifold should know the difference — the question is how many tokens
  it needs before the distinction registers.
"""

import math
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────────────────────
MODEL_ID      = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE        = "cuda" if torch.cuda.is_available() else "cpu"
ASSETS_DIR    = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# Airport coordinates
SFO = (37.6213, -122.3790)   # lat, lon
HND = (35.5494,  139.7798)   # lat, lon  (Tokyo Haneda)

N_WAYPOINTS = 5   # intermediate points on each path

# ── Geodesy helpers ──────────────────────────────────────────────────────────
def to_rad(deg): return math.radians(deg)
def to_deg(rad): return math.degrees(rad)

def haversine_nm(lat1, lon1, lat2, lon2):
    """Great circle distance in nautical miles."""
    R = 3440.065
    dlat = to_rad(lat2 - lat1)
    dlon = to_rad(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def initial_bearing(lat1, lon1, lat2, lon2):
    """Initial bearing (forward azimuth) of great circle path, degrees 0-360."""
    lat1, lon1, lat2, lon2 = map(to_rad, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return (to_deg(math.atan2(x, y)) + 360) % 360

def rhumb_bearing(lat1, lon1, lat2, lon2):
    """Constant bearing of rhumb line, degrees 0-360."""
    lat1, lat2 = to_rad(lat1), to_rad(lat2)
    dlon = to_rad(lon2 - lon1)
    # Normalise dlon to [-π, π]
    if abs(dlon) > math.pi:
        dlon = -(2*math.pi - dlon) if dlon > 0 else (2*math.pi + dlon)
    dpsi = math.log(math.tan(math.pi/4 + lat2/2) / math.tan(math.pi/4 + lat1/2))
    q = (lat2 - lat1) / dpsi if abs(dpsi) > 1e-10 else math.cos(lat1)
    return (to_deg(math.atan2(dlon, dpsi)) + 360) % 360

def rhumb_distance_nm(lat1, lon1, lat2, lon2):
    """Rhumb line distance in nautical miles."""
    R = 3440.065
    lat1, lat2 = to_rad(lat1), to_rad(lat2)
    dlat = lat2 - lat1
    dlon = abs(to_rad(lon2 - lon1))
    if dlon > math.pi:
        dlon = 2*math.pi - dlon
    dpsi = math.log(math.tan(math.pi/4 + lat2/2) / math.tan(math.pi/4 + lat1/2))
    q = dlat / dpsi if abs(dpsi) > 1e-10 else math.cos(lat1)
    d = math.sqrt(dlat**2 + q**2 * dlon**2)
    return R * d

def geodesic_waypoints(lat1, lon1, lat2, lon2, n):
    """Intermediate waypoints along the great circle."""
    pts = []
    for i in range(n+2):
        f = i / (n+1)
        # Spherical interpolation
        lat1r, lon1r = to_rad(lat1), to_rad(lon1)
        lat2r, lon2r = to_rad(lat2), to_rad(lon2)
        d = 2 * math.asin(math.sqrt(
            math.sin((lat2r-lat1r)/2)**2 +
            math.cos(lat1r)*math.cos(lat2r)*math.sin((lon2r-lon1r)/2)**2
        ))
        if d < 1e-10:
            pts.append((lat1, lon1))
            continue
        A = math.sin((1-f)*d) / math.sin(d)
        B = math.sin(f*d) / math.sin(d)
        x = A*math.cos(lat1r)*math.cos(lon1r) + B*math.cos(lat2r)*math.cos(lon2r)
        y = A*math.cos(lat1r)*math.sin(lon1r) + B*math.cos(lat2r)*math.sin(lon2r)
        z = A*math.sin(lat1r) + B*math.sin(lat2r)
        lat = to_deg(math.atan2(z, math.sqrt(x**2+y**2)))
        lon = to_deg(math.atan2(y, x))
        pts.append((lat, lon))
    return pts[1:-1]  # drop endpoints

def rhumb_waypoints(lat1, lon1, lat2, lon2, n):
    """Intermediate waypoints along the rhumb line (linear interpolation in Mercator)."""
    # Rhumb line: constant bearing, linear in Mercator projected coords
    pts = []
    bearing_r = to_rad(rhumb_bearing(lat1, lon1, lat2, lon2))
    dist_nm   = rhumb_distance_nm(lat1, lon1, lat2, lon2)
    R = 3440.065
    lat1r = to_rad(lat1)
    for i in range(1, n+1):
        f = i / (n+1)
        d = to_rad(dist_nm * f / R)
        lat_r = math.asin(math.sin(lat1r)*math.cos(d) +
                           math.cos(lat1r)*math.sin(d)*math.cos(bearing_r))
        lon_r = to_rad(lon1) + math.atan2(
            math.sin(bearing_r)*math.sin(d)*math.cos(lat1r),
            math.cos(d) - math.sin(lat1r)*math.sin(lat_r)
        )
        pts.append((to_deg(lat_r), to_deg(lon_r)))
    return pts

def fmt_coord(lat, lon):
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{abs(lat):.1f}°{ns} {abs(lon):.1f}°{ew}"

# ── Compute paths ─────────────────────────────────────────────────────────────
rhumb_brg  = rhumb_bearing(*SFO, *HND)
rhumb_nm   = rhumb_distance_nm(*SFO, *HND)
geo_brg    = initial_bearing(*SFO, *HND)
geo_nm     = haversine_nm(*SFO, *HND)
savings_nm  = rhumb_nm - geo_nm
savings_pct = 100.0 * savings_nm / rhumb_nm

rhumb_wpts = rhumb_waypoints(*SFO, *HND, N_WAYPOINTS)
geo_wpts   = geodesic_waypoints(*SFO, *HND, N_WAYPOINTS)

# Peak latitude of great circle (over Alaska)
peak_lat = max(lat for lat, lon in geo_wpts)

# ── Build text representations ────────────────────────────────────────────────
def make_representations(strategy):
    """Build 5 text levels for rhumb or geodesic strategy."""
    if strategy == "rhumb":
        brg, nm = rhumb_brg, rhumb_nm
        wpts = rhumb_wpts
        strat_name = "rhumb line"
        brg_desc = f"constant bearing {brg:.0f}° (due west)"
        wp_strs = [fmt_coord(*p) for p in wpts]
        prose = (
            f"Depart San Francisco on a constant bearing of {brg:.0f} degrees. "
            f"Maintain heading due west throughout the flight. "
            f"Estimated distance {nm:.0f} nautical miles. "
            f"This is a rhumb line: the bearing never changes."
        )
        reasoning = (
            f"The rhumb line from SFO to HND holds a constant bearing of {brg:.0f} degrees. "
            f"On a Mercator map it appears as a straight line heading due west. "
            f"Total distance is approximately {nm:.0f} NM. "
            f"This path treats the Earth as locally flat — it applies no curvature correction. "
            f"The pocket ruler says west is west. No Jacobian, no update. "
            f"Distance penalty: {savings_nm:.0f} NM longer than the great circle."
        )
    else:
        brg, nm = geo_brg, geo_nm
        wpts = geo_wpts
        strat_name = "great circle"
        brg_desc = f"initial bearing {brg:.0f}° (northwest, over Alaska)"
        wp_strs = [fmt_coord(*p) for p in wpts]
        prose = (
            f"Depart San Francisco on an initial bearing of {brg:.0f} degrees northwest. "
            f"The heading rotates continuously as the aircraft follows the great circle. "
            f"The route arcs north to {peak_lat:.0f} degrees latitude before descending to Tokyo. "
            f"Estimated distance {nm:.0f} nautical miles."
        )
        reasoning = (
            f"The great circle from SFO to HND departs on bearing {brg:.0f} degrees, "
            f"curving northwest over the north Pacific, reaching {peak_lat:.0f}°N, "
            f"then descending southeast to Tokyo Haneda. "
            f"Distance {nm:.0f} NM — {savings_nm:.0f} NM shorter than the rhumb line. "
            f"This path requires trusting the instruments over the pocket ruler. "
            f"The bearing is wrong by eye but right by mathematics. "
            f"Each Jacobian update corrects for Earth curvature. "
            f"The geodesic IS the manifold's natural path."
        )

    return {
        "coords":    f"{fmt_coord(*SFO)} to {fmt_coord(*HND)}",
        "bearing":   f"{strat_name}: {brg_desc}, {nm:.0f} NM",
        "waypoints": f"{strat_name} waypoints: " + " → ".join(wp_strs),
        "prose":     prose,
        "reasoning": reasoning,
    }

LEVELS = ["coords", "bearing", "waypoints", "prose", "reasoning"]
STRATEGIES = ["rhumb", "geodesic"]

representations = {s: make_representations(s) for s in STRATEGIES}

# ── Model loading ─────────────────────────────────────────────────────────────
print("=" * 70)
print("Experiment 15 — Rhumb Line vs Geodesic: SFO → HND")
print("=" * 70)
print()
print(f"Physical ground truth:")
print(f"  Rhumb:    {rhumb_nm:,.0f} NM  bearing {rhumb_brg:.1f}° (due west)")
print(f"  Geodesic: {geo_nm:,.0f} NM  bearing {geo_brg:.1f}° (northwest)")
print(f"  Savings:  {savings_nm:,.0f} NM  ({savings_pct:.1f}% shorter on geodesic)")
print(f"  Great circle peak latitude: {peak_lat:.1f}°N")
print()
print(f"Loading {MODEL_ID} …")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map=DEVICE,
    attn_implementation="eager",
    output_hidden_states=True,
)
model.eval()
print("Model ready.")
print()

# ── Embedding function ────────────────────────────────────────────────────────
@torch.no_grad()
def embed(text):
    ids = tokenizer(text, return_tensors="pt").input_ids.to(DEVICE)
    out = model(ids, output_hidden_states=True)
    h   = out.hidden_states[-1][0]        # (seq_len, 2048)
    return h.mean(dim=0).float().cpu().numpy(), ids.shape[1]

# ── Embed all representations ─────────────────────────────────────────────────
print("Embedding all 2 strategies × 5 levels = 10 representations …")
embeddings = {}
token_counts = {}

for strat in STRATEGIES:
    for level in LEVELS:
        text = representations[strat][level]
        emb, ntok = embed(text)
        embeddings[(strat, level)] = emb
        token_counts[(strat, level)] = ntok
        print(f"  {strat:8s}  {level:10s}  {ntok:3d} tok  |  {text[:60]}…" if len(text) > 60
              else f"  {strat:8s}  {level:10s}  {ntok:3d} tok  |  {text}")

print()

# ── Analysis ──────────────────────────────────────────────────────────────────
print("=" * 70)
print("SEPARABILITY ANALYSIS")
print("=" * 70)
print()

l2_by_level = []
for level in LEVELS:
    v_rhumb = embeddings[("rhumb",    level)]
    v_geo   = embeddings[("geodesic", level)]
    l2 = float(np.linalg.norm(v_rhumb - v_geo))
    l2_by_level.append(l2)
    tok_r = token_counts[("rhumb",    level)]
    tok_g = token_counts[("geodesic", level)]
    print(f"  Level '{level}'  ({tok_r}t / {tok_g}t)")
    print(f"    L2(rhumb, geodesic) = {l2:.3f}")
    print()

best_level = LEVELS[int(np.argmax(l2_by_level))]
best_l2    = max(l2_by_level)
print(f"  Best separation:  level '{best_level}',  L2 = {best_l2:.3f}")
print()

# Ratio: reasoning vs coords
ratio = l2_by_level[LEVELS.index("reasoning")] / (l2_by_level[LEVELS.index("coords")] + 1e-9)
print(f"  Reasoning/coords L2 ratio: {ratio:.2f}×")
print()

# ── Plotting ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("#0d1117")
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

ax_map  = fig.add_subplot(gs[0, 0])
ax_sep  = fig.add_subplot(gs[0, 1])
ax_tok  = fig.add_subplot(gs[1, 0])
ax_txt  = fig.add_subplot(gs[1, 1])

for ax in [ax_map, ax_sep, ax_tok, ax_txt]:
    ax.set_facecolor("#161b22")
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

RHUMB_COL = "#ff7b72"   # red
GEO_COL   = "#79c0ff"   # blue
TEXT_COL  = "#c9d1d9"

# ── Panel 1: Path map (equirectangular projection) ────────────────────────────
all_rhumb = [SFO] + rhumb_wpts + [HND]
all_geo   = [SFO] + geo_wpts   + [HND]

rlats = [p[0] for p in all_rhumb]
rlons = [p[1] for p in all_rhumb]
glats = [p[0] for p in all_geo]
glons = [p[1] for p in all_geo]

# Unwrap rhumb longitudes crossing antimeridian
def unwrap_lons(lons):
    out = [lons[0]]
    for i in range(1, len(lons)):
        d = lons[i] - out[-1]
        if d > 180:  d -= 360
        if d < -180: d += 360
        out.append(out[-1] + d)
    return out

rlons_u = unwrap_lons(rlons)
glons_u = unwrap_lons(glons)

ax_map.plot(rlons_u, rlats, '-o', color=RHUMB_COL, linewidth=2,
            markersize=4, label=f"Rhumb  {rhumb_nm:,.0f} NM  {rhumb_brg:.0f}°", zorder=3)
ax_map.plot(glons_u, glats, '-o', color=GEO_COL,   linewidth=2,
            markersize=4, label=f"Geodesic  {geo_nm:,.0f} NM  {geo_brg:.0f}°", zorder=3)

# Mark airports
ax_map.scatter([SFO[1]], [SFO[0]], s=80, color="white", zorder=5)
ax_map.scatter([HND[1]], [HND[0]], s=80, color="white", zorder=5)
ax_map.annotate("SFO", SFO[::-1], textcoords="offset points", xytext=(-25, 5),
                color=TEXT_COL, fontsize=8)
ax_map.annotate("HND", HND[::-1], textcoords="offset points", xytext=(5, 5),
                color=TEXT_COL, fontsize=8)

ax_map.set_title("Navigation Paths: SFO → HND", color=TEXT_COL, fontsize=10, pad=8)
ax_map.set_xlabel("Longitude", color=TEXT_COL, fontsize=8)
ax_map.set_ylabel("Latitude", color=TEXT_COL, fontsize=8)
ax_map.tick_params(colors=TEXT_COL)
ax_map.legend(fontsize=7, facecolor="#21262d", labelcolor=TEXT_COL,
              edgecolor="#30363d", loc="upper left")

# ── Panel 2: L2 separation by level ──────────────────────────────────────────
x = np.arange(len(LEVELS))
bars = ax_sep.bar(x, l2_by_level, color=[GEO_COL]*len(LEVELS), alpha=0.8, edgecolor="#30363d")
# Colour the best bar differently
bars[int(np.argmax(l2_by_level))].set_color("#ffa657")

for i, v in enumerate(l2_by_level):
    ax_sep.text(i, v + 0.3, f"{v:.1f}", ha="center", va="bottom",
                color=TEXT_COL, fontsize=8)

ax_sep.set_xticks(x)
ax_sep.set_xticklabels(LEVELS, rotation=20, ha="right", color=TEXT_COL, fontsize=8)
ax_sep.set_ylabel("L2 distance (rhumb vs geodesic)", color=TEXT_COL, fontsize=8)
ax_sep.set_title("Embedding Separation by Level", color=TEXT_COL, fontsize=10, pad=8)
ax_sep.tick_params(colors=TEXT_COL)

# ── Panel 3: Token count per level ───────────────────────────────────────────
tok_r = [token_counts[("rhumb",    lv)] for lv in LEVELS]
tok_g = [token_counts[("geodesic", lv)] for lv in LEVELS]
w = 0.35
ax_tok.bar(x - w/2, tok_r, w, color=RHUMB_COL, alpha=0.8, label="Rhumb",    edgecolor="#30363d")
ax_tok.bar(x + w/2, tok_g, w, color=GEO_COL,   alpha=0.8, label="Geodesic", edgecolor="#30363d")
ax_tok.set_xticks(x)
ax_tok.set_xticklabels(LEVELS, rotation=20, ha="right", color=TEXT_COL, fontsize=8)
ax_tok.set_ylabel("Token count", color=TEXT_COL, fontsize=8)
ax_tok.set_title("Token Budget per Level", color=TEXT_COL, fontsize=10, pad=8)
ax_tok.tick_params(colors=TEXT_COL)
ax_tok.legend(fontsize=7, facecolor="#21262d", labelcolor=TEXT_COL, edgecolor="#30363d")

# ── Panel 4: Summary text ─────────────────────────────────────────────────────
ax_txt.axis("off")
summary = (
    f"SFO → HND  Navigation Geometry\n"
    f"{'─'*38}\n"
    f"Rhumb:     {rhumb_nm:>7,.0f} NM   {rhumb_brg:.1f}°  (due west)\n"
    f"Geodesic:  {geo_nm:>7,.0f} NM   {geo_brg:.1f}°  (northwest)\n"
    f"Savings:   {savings_nm:>7,.0f} NM   ({savings_pct:.1f}% shorter)\n"
    f"Peak lat:  {peak_lat:.1f}°N  (over north Pacific)\n"
    f"\n"
    f"Embedding Separation\n"
    f"{'─'*38}\n"
)
for lv, l2 in zip(LEVELS, l2_by_level):
    bar = "█" * int(l2 / 2)
    marker = " ←" if lv == best_level else ""
    summary += f"  {lv:<10}  L2={l2:5.1f}  {bar}{marker}\n"

summary += (
    f"\n"
    f"Reasoning/coords ratio: {ratio:.2f}×\n"
    f"\n"
    f"Thesis: the manifold encodes navigation\n"
    f"strategy, not just destination.\n"
    f"Rhumb = e^I (no curvature update).\n"
    f"Geodesic = Jacobian path.\n"
    f"The instrument panel is right."
)

ax_txt.text(0.05, 0.95, summary, transform=ax_txt.transAxes,
            color=TEXT_COL, fontsize=7.5, fontfamily="monospace",
            verticalalignment="top", linespacing=1.5)

fig.suptitle(
    "Experiment 15 — Rhumb vs Geodesic: SFO→HND\n"
    "Does the transformer manifold distinguish flat from curved navigation?",
    color=TEXT_COL, fontsize=11, y=0.98
)

out_path = ASSETS_DIR / "15_rhumb_vs_geodesic.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Plot saved → {out_path}")
print()

# ── Interpretation ────────────────────────────────────────────────────────────
print("=" * 70)
print("INTERPRETATION")
print("=" * 70)
print()
print(f"  The rhumb line says: west is west.  Bearing {rhumb_brg:.0f}°, {rhumb_nm:,.0f} NM.")
print(f"  The geodesic says:   trust the panel.  Bearing {geo_brg:.0f}°, {geo_nm:,.0f} NM.")
print(f"  The panel is right by {savings_nm:.0f} NM.")
print()
print(f"  In embedding space:")
for lv, l2 in zip(LEVELS, l2_by_level):
    bar = "█" * int(l2 / 2)
    print(f"    {lv:<10}  L2 = {l2:6.2f}  {bar}")
print()
print(f"  Best level: '{best_level}'  L2 = {best_l2:.2f}")
print()
if l2_by_level[0] > 5.0:
    print("  ✓ Even raw coordinates separate rhumb from geodesic.")
    print("    The manifold knows a bearing of 263° is not 316°.")
else:
    print("  — Raw coordinates show weak separation.")
    print("    The difference is in the framing, not the numbers alone.")
print()
print(f"  Ratio reasoning/coords = {ratio:.2f}×")
print(f"  Explicit reasoning {'amplifies' if ratio > 1 else 'does not amplify'} separation.")
print()
print("  Thesis connection:")
print("    e^I (identity path) = rhumb: uniform scaling, no differential update.")
print("    Jacobian path = geodesic: local curvature correction at each step.")
print("    The transformer inhabits the manifold shaped by all prior navigation text.")
print("    It has seen every flight plan, every great-circle formula.")
print("    The question is not whether it knows — it does.")
print("    The question is: at what token count does that knowledge become legible?")
print("=" * 70)
