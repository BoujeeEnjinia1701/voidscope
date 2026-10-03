"""VoidScope sizing calculations, VDS-CAL-001 v0.1 (TRL 3, constructable design VDS-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md (tags in brackets, for example [B3])
and writes docs/04-calcs/results.csv. Geometry comes from PARAMS, derived() and the solids of
cad/src/model.py, so the figures match the STEP files and drawing VDS-DWG-001. It also reads
bom/bom.csv and budget_usd in project.yaml. First-principles paper estimates; nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, derived, build_components  # noqa: E402

G = 9.81
OUT = []


def fmt(v):
    a = abs(v)
    return f"{v:,.0f}" if a >= 100 else (f"{v:.1f}" if a >= 10 else (f"{v:.2f}" if a >= 0.1 else f"{v:.3g}"))


def out(tag, text, value=None, unit=""):
    OUT.append((tag, text, value, unit))
    v = "" if value is None else (fmt(value) if isinstance(value, float) else f"{value}")
    print(f"[{tag}] {text}: {v} {unit}".rstrip())


D = derived(P)
C = build_components(P)

# ------------------------------------------------------------------ A. envelope and reach (R1, R2, R11)
out("A1", "Largest diameter anywhere on the probe (head 48, grip 47, buttons)", D["max_od"], "mm")
out("A2", "Radial clearance in a 51 mm core hole at the head", (51.0 - D["max_od"]) / 2, "mm")
out("A3", "Assembled probe length, tail cap to tip", D["length"], "mm")
out("A4", "Working length, tip to the front of the grip", D["working_length"], "mm")
out("A5", "Head length, collar back face to tip", D["head_len"], "mm")
od, wall, Ls = P["rod"]
out("A6", "Rigid rod: smallest bend radius it can follow", "none (straight only)")

# ------------------------------------------------------------------ B. rod structure and handling
E = 69000.0           # MPa, 6061-T6
SY = 240.0            # MPa, 6061-T6 yield (minimum)
ri = od / 2 - wall
I = math.pi / 64 * (od ** 4 - (od - 2 * wall) ** 4)
Z = I / (od / 2)
A_tube = math.pi / 4 * (od ** 2 - (od - 2 * wall) ** 2)
RHO = 2.7e-6          # kg/mm3
vol = {k: c.shape.volume for k, c in C.items()}
m_rods = sum(vol[f"rod{k}"] for k in range(1, 5)) * RHO
m_coup = sum(vol[f"coupler{k}"] + vol[f"pins{k}"] for k in range(1, 5)) * RHO + 4 * 0.006
m_head_al = (vol["collar"] + vol["nose"]) * RHO
m_cam, m_spk, m_bite = 0.18, 0.012, 0.010
m_tail = (vol["tailcap"]) * RHO + 0.03 + 0.02
m_grip = 0.15
L_cable_in, L_guide_in = D["length"] / 1000, D["length"] / 1000
m_lines_per_m = 0.045 + (math.pi / 4 * (8 ** 2 - 6 ** 2) * 2.2e-6 * 1000) + (math.pi / 4 * (4 ** 2 - 2.5 ** 2) * 1.2e-6 * 1000) \
    + math.pi / 4 * 2.5 ** 2 * 1e-6 * 1000
m_head = m_head_al + m_cam + m_spk + m_bite
m_probe = m_rods + m_coup + m_head + m_tail + m_grip + m_lines_per_m * L_cable_in
w = (m_rods + m_coup) / (D["length"] / 1000) + m_lines_per_m      # kg/m along the rod
out("B1", "Rod tube second moment of area", I, "mm4")
out("B2", "Rod tube section modulus", Z, "mm3")
out("B3", "Rod line mass (tube, couplers, lines, water)", w, "kg/m")
out("B4", "Head mass (collar, nose, camera, speaker, bite valve)", m_head, "kg")
out("B5", "Probe mass, assembled, lines filled", m_probe, "kg")
wN = w * G / 1000      # N/mm
Wh = m_head * G
for a in (1000.0, 2000.0):
    d = wN * a ** 4 / (8 * E * I) + Wh * a ** 3 / (3 * E * I)
    out(f"B6{'a' if a == 1000 else 'b'}", f"Tip droop with {a / 1000:.0f} m unsupported beyond the hole", d, "mm")
# hand force with the hole lip as fulcrum, grip centre as the hand
xg = P["grip"][2] + P["grip"][1] / 2
Ltot = D["length"]
hand = {}
for a in (1000.0, 2000.0, 3000.0):
    xf = Ltot - a
    m_front = wN * a ** 2 / 2 + Wh * a
    m_back = wN * xf ** 2 / 2
    F = (m_front - m_back) / (xf - xg)
    hand[a] = (F, m_front / 1000)
    out(f"B7{int(a / 1000)}", f"Hand force at the grip with {a / 1000:.0f} m in the void and the tip unsupported (+ pushes down)", F, "N")
Mmax = max(v[1] for v in hand.values()) * 1000          # N mm at the lip, 3 m case
sig = Mmax / Z
out("B8", "Bending moment at the hole lip, 3 m in the void, tip unsupported", Mmax / 1000, "N m")
out("B9", "Bending stress in the plain tube at that moment", sig, "MPa")
out("B10", "Stress at a button hole (stress concentration 3)", 3 * sig, "MPa")
out("B11", "Safety factor on yield at a button hole", SY / (3 * sig))
F_push = 200.0
Pcr = math.pi ** 2 * E * I / Ltot ** 2
out("B12", "Euler buckling load of the whole rod, pinned at both ends", Pcr, "N")
out("B13", "Buckling factor at a 200 N two-handed push", Pcr / F_push)
F_pull = 300.0
bear = F_pull / (P["button"][0] * wall)
tear = F_pull / (2 * P["button"][1] * wall)
pin_sh = F_pull / (2 * math.pi / 4 * P["pin"][0] ** 2)
out("B14", "Bearing stress at a button hole at a 300 N pull to free a stuck probe", bear, "MPa")
out("B15", "Shear-out stress behind the button hole at 300 N", tear, "MPa")
out("B16", "Shear stress in the two coupler pins at 300 N (epoxy ignored)", pin_sh, "MPa")

# ------------------------------------------------------------------ C. vision (R3)
px_w, hfov = 1920, 90.0
fov_w = 2 * 1000 * math.tan(math.radians(hfov / 2))
px_letter = px_w / fov_w * 20
out("C1", "Width seen at 1 m with a 90 degree horizontal view", fov_w, "mm")
out("C2", "Pixels across the height of a 20 mm letter at 1 m (1080p)", px_letter, "px")
out("C3", "Pixels needed to read a letter (assumed)", 10)
lum, beam = 60.0, 120.0
omega = 2 * math.pi * (1 - math.cos(math.radians(beam / 2)))
lux = lum / omega
out("C4", "Illuminance on axis at 1 m from the camera LEDs (60 lm in a 120 degree beam)", lux, "lx")
out("C5", "Ratio to the camera's 0.01 lx minimum illumination", lux / 0.01)
out("C6", "Light left after 2 m of dusty air at an assumed extinction of 0.5 per m", lux * math.exp(-0.5 * 2), "lx")

# ------------------------------------------------------------------ D. water (R5, R10)
MU = {5: 1.519e-3, 20: 1.002e-3, 40: 0.653e-3}       # Pa s
d_cap, L_cap = 0.5e-3, 0.600
d_t, L_t = 2.5e-3, 8.0
RHOW = 1000.0


def q_ml_min(h, T):
    R = 128 * MU[T] / math.pi * (L_cap / d_cap ** 4 + L_t / d_t ** 4)
    return RHOW * G * h / R * 6e7


for h in (0.5, 1.0, 2.0):
    for T in (5, 20, 40):
        out(f"D1-{h:g}-{T}", f"Drip ceiling at {h:g} m water height above the tip, {T} C, clamp fully open", q_ml_min(h, T), "mL/min")
qmax = q_ml_min(2.0, 40)
out("D2", "Highest possible flow: 2 m height (1 m allowed plus 1 m error) at 40 C", qmax, "mL/min")
out("D3", "Same, at the 1 m height the procedure allows, 20 C", q_ml_min(1.0, 20), "mL/min")
out("D4", "Water per hour at 1 m, 20 C, clamp fully open", q_ml_min(1.0, 20) * 60, "mL/h")
vprime = math.pi / 4 * (d_t * 1000) ** 2 * L_t * 1000 / 1000
out("D5", "Water in the line when primed (4 x 2.5 mm tube, 8 m)", vprime, "mL")
v_open = math.pi * d_t ** 4 * RHOW * G * 1.0 / (128 * MU[20] * L_t) * 6e7
out("D6", "Flow at 1 m without the capillary (why it is fitted)", v_open, "mL/min")
p_max = RHOW * G * 2.0 / 1000
out("D7", "Water pressure at the bite valve at 2 m height (no flow)", p_max, "kPa")
t_change = 1.0 + 2.0 + 1.0
out("D8", "Water set change: pull old tube 1 min, push new tube 2 min, prime 1 min", t_change, "min")

# ------------------------------------------------------------------ E. air (R6)
RHOA, MUA = 1.2, 1.8e-5


def dp_pipe(Q, d, L, k_minor=0.0):
    A = math.pi / 4 * d ** 2
    v = Q / A
    Re = RHOA * v * d / MUA
    f = 64 / Re if Re < 2300 else 0.316 / Re ** 0.25
    return f * L / d * RHOA * v ** 2 / 2 + k_minor * RHOA * v ** 2 / 2, v, Re


def system(Q_lpm):
    Q = Q_lpm / 60000
    hose = dp_pipe(Q, 0.012, 2.5, 1.0)[0]
    barbs = 2 * dp_pipe(Q, 0.009, 0.03, 1.5)[0]
    a_bore = math.pi / 4 * (D["coupler_id"] / 1000) ** 2 - math.pi / 4 * (0.006 ** 2 + 0.008 ** 2)
    d_h = 4 * a_bore / (math.pi * (D["coupler_id"] / 1000) + math.pi * 0.014)
    rod = dp_pipe(Q, d_h, D["length"] / 1000, 4 * 0.5)[0]
    n_out = len(P["outlets"][2])
    a_out = n_out * math.pi / 4 * (P["outlets"][0] / 1000) ** 2
    v_out = Q / a_out
    outlets = 1.5 * RHOA * v_out ** 2 / 2
    filt = 2.5 * Q_lpm           # Pa, assumed clean F7 cartridge, 50 Pa at 20 L/min
    meter = 200.0                # Pa, upper bound accepted on the flow meter (variable area: about constant)
    return dict(hose=hose, barbs=barbs, rod=rod, outlets=outlets, filter=filt, meter=meter, v_out=v_out,
                total=hose + barbs + rod + outlets + filt + meter)


s20 = system(20.0)
for k in ("filter", "meter", "hose", "barbs", "rod", "outlets", "total"):
    out(f"E1-{k}", f"Pressure drop at 20 L/min: {k}", s20[k], "Pa")
out("E2", "Air speed leaving the six 5 mm outlets at 20 L/min", s20["v_out"], "m/s")
P0, Q0 = 900.0, 300.0      # assumed blower curve at full speed: shut-off 0.9 kPa, free flow 300 L/min


def blower(Q, s):
    return P0 * s ** 2 * (1 - (Q / (Q0 * s)) ** 2)


def op_point(s):
    lo, hi = 0.0, Q0 * s
    for _ in range(60):
        mid = (lo + hi) / 2
        if blower(mid, s) > system(mid)["total"]:
            lo = mid
        else:
            hi = mid
    return lo


q_full = op_point(1.0)
lo, hi = 0.2, 1.0
for _ in range(60):
    mid = (lo + hi) / 2
    if op_point(mid) < 20.0:
        lo = mid
    else:
        hi = mid
s_20 = hi
out("E3", "Air flow at full blower speed into an open void", q_full, "L/min")
out("E4", "Blower speed setting for 20 L/min", s_20 * 100, "%")
out("E5", "Highest pressure at the tip with every outlet blocked (blower shut-off)", P0 / 1000, "kPa")
gap = D["fit_coupler"] / 1000
leak = math.pi * 0.0349 * gap ** 3 * 50 / (12 * MUA * 0.030) * 60000
out("E6", "Leak past one coupler at 50 Pa in the rod (0.11 mm gap, 30 mm long)", leak, "L/min")
p_blow_full, p_blow_ctrl = 4.0, 0.3
p_blow_20 = p_blow_full * s_20 ** 3 + p_blow_ctrl
out("E7", "Blower electrical power at the 20 L/min setting", p_blow_20, "W")

# ------------------------------------------------------------------ F. power (R7)
loads = {"camera and LEDs": 3.0, "monitor and recorder": 7.0}
eff = 0.90
p_video = sum(loads.values()) / eff
p_all = p_video + p_blow_20 + 0.4
E_pack = 12.8 * 6.0
usable, cold = 0.90, 0.70
out("F1", "Video and light load at the battery (camera 3 W, monitor 7 W, converter 90 %)", p_video, "W")
out("F2", "With air at 20 L/min and push-to-talk on standby", p_all, "W")
out("F3", "Pack energy, 12.8 V 6 Ah LiFePO4", E_pack, "Wh")
for T, f in (("20", 1.0), ("-10", cold)):
    out(f"F4-{T}", f"Video and light run time on one pack at {T} C", E_pack * usable * f / p_video, "h")
    out(f"F5-{T}", f"Run time with air and audio on one pack at {T} C", E_pack * usable * f / p_all, "h")
out("F6", "Run time with air and audio on both packs at -10 C (one swap)", 2 * E_pack * usable * cold / p_all, "h")
out("F7", "Peak current at full blower and full LEDs", (p_video + p_blow_full + 2.0) / 12.0, "A")

# ------------------------------------------------------------------ G. robustness (R4)
out("G1", "Energy of a 1 m drop of the head and section 1 together", (m_head + w * Ls / 1000) * G * 1.0, "J")
out("G2", "Minimum wall in the nose (camera bore to outside, and to the pocket)",
    min(24 - abs(P["nose"][3]) - P["nose"][2] / 2, P["pocket"][1] - (P["nose"][3] + P["nose"][2] / 2)), "mm")

# ------------------------------------------------------------------ H. deployment (R9)
steps = [("open both cases, lift out the rod bundle and head", 0.4), ("join the head and four sections (snap buttons)", 0.7),
         ("plug the camera cable, fit the air hose, hang the water bottle", 0.6), ("switch on, check the picture and voice", 0.4)]
for k, (s_, t) in enumerate(steps):
    out(f"H{k + 1}", s_, t, "min")
out("H5", "Estimated time to start searching, two people", sum(t for _, t in steps), "min")

# ------------------------------------------------------------------ I. mass and cost (R8)
m_su = 2.6 + 2 * 0.0 + 0.85 + 0.45 + 0.20 + 0.15 + 0.25 + 0.6 + (vol["eplate"] + vol["dbracket"] + vol["fm_bracket"]) * RHO
out("I1", "Surface unit mass with one pack fitted (case 2.6 kg, pack 0.85 kg, monitor 0.6 kg, others estimated)", m_su, "kg")
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
out("I2", "Estimated cost of the constructable design from bom/bom.csv", cost, "USD")
out("I3", "Value-engineering target (budget_usd)", budget, "USD")
out("I4", "Under (+) or over (-) the target", budget - cost, "USD")
lathe = next(float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("29 "))
out("I5", "Cost without outside lathe time (builder has a lathe)", cost - lathe, "USD")

with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    wtr = csv.writer(f)
    wtr.writerow(["tag", "quantity", "value", "unit"])
    for tag, text, value, unit in OUT:
        wtr.writerow([tag, text, fmt(value).replace(",", "") if isinstance(value, float) else value, unit])
