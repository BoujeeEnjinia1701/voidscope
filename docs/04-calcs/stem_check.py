"""VoidScope STEM check calculations (VDS-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. Each row is a first-order screen computed here from the stated laws and
inputs, then set beside the figure in the calculation note (VDS-CAL-001, docs/04-calcs/sizing.py, read from
docs/04-calcs/results.csv so this script runs in seconds). Option A is the design of record; B and C are the
concept options of VDS-OPT-001.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX, FAILS, SIGMA  # noqa: E402,F401

RES = {r["tag"]: r["value"] for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open())}


def cal(tag):
    return float(RES[tag])


c = Check(ROOT / "docs/04-calcs/stem_results.csv")

# ---------------------------------------------------------------------------------------------- inputs
E_AL, SY_AL = 69000.0, 240.0          # MPa, 6061-T6 (handbook)
OD, T_W = 38.1, 1.47                  # mm rod tube
I_ROD = math.pi / 64 * (OD ** 4 - (OD - 2 * T_W) ** 4)           # mm4
Z_ROD = I_ROD / (OD / 2)
L_PROBE = cal("A3")                   # mm
W_ROD = cal("B3") * G / 1000.0        # N per mm of rod
F_HEAD = cal("B4") * G                # N

# ------------------------------------------------------------------------------ Physics: structure
pcr = math.pi ** 2 * E_AL * I_ROD / L_PROBE ** 2
c.cited("S1", "The whole rod survives a hard two-handed push of 200 N without buckling (twice the push as margin)", "Physics",
        "Strength of materials", f"Euler column buckling, P = pi^2 E I / L^2, pinned at both ends, 6061-T6 38.1 x 1.47 mm tube, 4.54 m: {pcr:.0f} N against 400 N needed. This is the ideal upper bound for a uniform tube; the slack at four couplers (0.11 mm a side) and the rod's own sag lower it (independent review)",
        f"{pcr:.0f} N ideal against 400 N needed; couplers fitted to test at TRL 4", PLAUSIBLE, closed_by=f"VDS-CAL-001 B12 ({cal('B12'):.0f} N); PR-017")
L2 = 2000.0
droop_c = W_ROD * L2 ** 4 / (8 * E_AL * I_ROD) + F_HEAD * L2 ** 3 / (3 * E_AL * I_ROD)
Lb = L_PROBE - L2 - 335.0 - 15.0                    # lip to grip centre
droop = droop_c + (W_ROD * L2 ** 2 / 2 + F_HEAD * L2) * Lb / (3 * E_AL * I_ROD) * L2
c.cited("S2", "With 2 m of probe unsupported beyond the hole the tip droops by a few per cent of that length, so the tip is rested on debris beyond about 2 m", "Physics", "Strength of materials",
        f"Cantilever d = w L^4 / 8EI + P L^3 / 3EI = {droop_c:.1f} mm, plus the turn of the back span about the hole lip (pivot, grip held): {droop:.0f} mm in all. The first version took the lip as a clamp (16.8 mm) and the independent review corrected it",
        f"{droop:.0f} mm at 2 m, about 2 per cent of the length; the camera looks about 1 degree low, which the steering takes up", PLAUSIBLE,
        closed_by=f"VDS-CAL-001 B6b ({cal('B6b'):.0f} mm); build plan section 5")
L3 = 3000.0
m_lip = W_ROD * L3 ** 2 / 2 + F_HEAD * L3
s_btn = 3 * m_lip / Z_ROD
c.claim("S3", "At a snap-button hole the rod keeps a safety factor of at least 2 on yield with 3 m unsupported in a void", "Physics",
        "Strength of materials", "Bending stress M / Z with a stress concentration of 3 at an 8.5 mm hole; 6061-T6 yield 240 MPa",
        round(s_btn, 0), SY_AL / 2, "MPa", closed_by=f"VDS-CAL-001 B11 (factor {cal('B11'):.2f})")
c.claim("S4", "The two coupler pins carry a 300 N pull to free a stuck probe", "Engineering and technology", "Strength of materials",
        "Double shear of two 4 mm aluminium pins, tau = F / (2 n A); shear strength taken as 0.58 of 240 MPa",
        round(300 / (2 * 2 * math.pi * 2.0 ** 2), 1), 0.58 * SY_AL, "MPa", closed_by=f"VDS-CAL-001 B16 ({cal('B16'):.1f} MPa)")
nj_t = 83.3
c.claim("S5", "A steering wire keeps a factor of 3 on its assumed breaking load under a 30 N thumb push against the stop", "Physics",
        "Strength of materials", "Lever and drum: wire tension T = F x lever / drum radius = 30 N x 50 mm / 18 mm radius (36 mm drum) = 83 N; 0.6 mm 7x7 stainless rope breaking load 250 N assumed (to confirm from the supplier)",
        round(30 * 50.0 / 18.0, 1), 250.0 / 3, "N", margin=0.1, closed_by="VDS-CAL-001 J15, J16 (factor 3.0)")
c.claim("S6", "The printed PA12 hinge lugs bear the wire tension without yielding", "Engineering and technology", "Strength of materials",
        "Bearing stress F / (n d t) on two 2 mm pins in 2.4 mm lugs at 83 N; PA12 yield about 45 MPa (datasheet value, to confirm)",
        round(83.3 / (2 * 2.0 * 2.4), 1), 45.0 / 1.5, "MPa", closed_by=f"VDS-CAL-001 J18 ({cal('J18'):.1f} MPa)")

# ------------------------------------------------------------------------------ Physics: water
RHO, G_ = 992.0, G                     # kg/m3 at 40 C
mu40, d_c, L_c = 0.653e-3, 0.5e-3 * 1.05, 0.750      # bore 5 per cent oversize, capillary 750 mm (VDS-DDR-006 F3)
dp = RHO * G_ * 2.0
q_ml = math.pi * (d_c / 2) ** 4 * dp / (8 * mu40 * L_c) * 6e7
c.claim("S7", "The gravity drip never exceeds 5 mL/min, even with the bottle 2 m up (1 m allowed plus 1 m error) and water at 40 C", "Physics",
        "Fluid mechanics", "Hagen-Poiseuille flow in a 0.5 mm bore (5 per cent oversize as worst case), 750 mm long capillary (600 mm failed the margin, fix F3), Q = pi r^4 dP / 8 mu L (8 m of 2.5 mm tube in series lowers it further)",
        round(q_ml, 2), 5.0, "mL/min", margin=0.1, closed_by=f"VDS-CAL-001 D2 ({cal('D2'):.2f} mL/min)")
v = q_ml / 6e7 / (math.pi * (d_c / 2) ** 2)
re = RHO * v * d_c / mu40
c.claim("S8", "The capillary flow is laminar, so the Poiseuille law applies", "Physics", "Fluid mechanics",
        "Reynolds number Re = rho v d / mu below 2,000 at the highest flow", round(re, 0), 2000.0, "(Re)", closed_by="VDS-CAL-001 D1")
ml_h = cal("D4")
c.claim("S9", "At the 1 m, 20 C setting the drip supplies at least half of the 2.5 L a day that Sphere gives as the survival need for drinking", "Biology",
        "Human physiology", "Sphere Handbook, water supply standard 1: survival needs 2.5 to 3 litres per day (drinking and food); 88 mL/h is 2.1 L/day. The drip is a bridge until extrication, not full hydration",
        round(ml_h * 24 / 1000, 2), 1.25, "L/day", rule="above", closed_by="VDS-CAL-001 D4")

# ------------------------------------------------------------------------------ Physics: air
c.claim("S10", "The air path loses less than the blower can overcome at 20 L/min", "Physics", "Fluid mechanics",
        "Sum of Darcy-Weisbach pipe losses and minor losses over the filter, meter, 2.5 m hose, barbs, rod bore and outlets; blower shut-off 0.9 kPa",
        round(cal("E1-total") / 1000, 3), 0.9, "kPa", closed_by="VDS-CAL-001 E1")
c.claim("S11", "With every outlet blocked the pressure at the tip stays below 1 kPa above ambient", "Physics", "Fluid mechanics",
        "Blower shut-off pressure is the only stop (a centrifugal blower cannot exceed its shut-off head), and it rises with the square of speed, so the blower runs from the converter's regulated output with a fixed speed cap and not straight from the pack (12.8 to 14.4 V would lift 0.9 kPa to about 1.1 to 1.3 kPa); 0.9 kPa is a datasheet figure to confirm when bought (fix F5, independent review)",
        cal("E5"), 1.0, "kPa", margin=0.1, closed_by="VDS-CAL-001 E5")

# ------------------------------------------------------------------------------ Physics: optics and light
px = 1920 / (2 * 1000 * math.tan(math.radians(45))) * 20
c.cited("S12", "A 20 mm letter 1 m from the camera spans enough pixels to read", "Physics", "Optics",
        f"Pinhole geometry: 1920 pixels across a 90 degree view give 0.96 px/mm at 1 m, {px:.1f} px per 20 mm letter against 10 needed. This counts sensor pixels only; lens blur, compression and an analogue link can cost 30 to 50 per cent, which still leaves about 10 px (independent review)",
        f"{px:.1f} px at the sensor, about 10 px after losses", PLAUSIBLE, closed_by=f"VDS-CAL-001 C2 ({cal('C2'):.1f} px); chart test at TRL 4")
c.cited("S13", "In moderate dust (extinction 0.5 per m, visibility about 8 m) the light after 2 m is far above the camera's minimum illumination; in dust so dense that visibility is 1 m nothing is seen, as with any camera", "Physics", "Optics",
        f"Inverse-square illuminance from 60 lm in a 120 degree beam, Beer-Lambert extinction over the 2 m round trip: {cal('C6'):.1f} lx at 0.5 per m, {cal('C7'):.4f} lx at 4 per m against a 0.01 lx minimum. The first version called 0.5 per m heavy dust (independent review)",
        f"{cal('C6'):.1f} lx at 0.5 per m; {cal('C7'):.4f} lx at 4 per m", PLAUSIBLE, closed_by="VDS-CAL-001 C6, C7; dust box at TRL 4")

# ------------------------------------------------------------------------------ Physics: heat
# Tip housing: 33 mm x 71 mm aluminium cylinder in still air, camera and LEDs dissipating in a sealed head.
D_T, L_T = 0.033, 0.071
A_T = math.pi * D_T * L_T + math.pi * D_T ** 2 / 4


def tip_temp(q_w, t_amb_c, eps):
    """Surface temperature of the tip housing: Churchill-Chu natural convection on a horizontal cylinder plus radiation."""
    k, nu, al, pr = 0.0285, 1.85e-5, 2.6e-5, 0.71
    ta = t_amb_c + 273.15
    for i in range(1, 3000):
        dt = i * 0.1
        ts = ta + dt
        ra = G * (1 / (ta + dt / 2)) * dt * D_T ** 3 / (nu * al)
        nu_ = (0.6 + 0.387 * ra ** (1 / 6) / (1 + (0.559 / pr) ** (9 / 16)) ** (8 / 27)) ** 2
        h = nu_ * k / D_T + eps * SIGMA * (ts ** 4 - ta ** 4) / dt
        if h * A_T * dt >= q_w:
            return t_amb_c + dt
    return float("nan")


T_TOUCH = 48.0   # deg C, uncoated metal touched for 600 s: a trapped survivor cannot pull away (BS EN 13202 table as reproduced in IEEE PSTC, see Sources)
# Record of the failed first version (kept in VDS-STM-001, Fix history): 3 W, bead-blasted, 85 C against 55 C at 45 C ambient, and the 10 s limit was the wrong criterion.
Q_FIX, EPS_FIX = 0.8, 0.85
t_fix = tip_temp(Q_FIX, 35.0, EPS_FIX)
t_fix45 = tip_temp(Q_FIX, 45.0, EPS_FIX)
c.claim("S14", "After the fix (housing black anodised, emissivity 0.85; LEDs dimmed so the head dissipates 0.8 W by default) the tip housing stays at or below 48 C, the 10 minute touch limit for bare metal, at 35 C ambient", "Physics", "Thermodynamics and heat transfer",
        f"Same convection and radiation model; at 45 C ambient it reaches {t_fix45:.0f} C, so above 35 C ambient the tip is kept off the survivor (steered aside, as for giving water) and the LEDs are kept at the lowest useful setting; camera power at the dimmed setting is a datasheet figure to confirm when bought",
        round(t_fix, 1), T_TOUCH, "C", margin=0.1, closed_by="VDS-DDR-006 F1; VDS-CAL-001 K1 to K5")
cap_wh = 12.8 * 6.0
run_cold = cap_wh * 0.9 * 0.7 / cal("F1")
c.claim("S15", "One pack runs video and light for at least 4 h at -10 C", "Physics", "Thermodynamics and heat transfer",
        "Energy balance: 76.8 Wh x 0.9 usable x 0.70 of capacity at -10 C (assumed) over an 11.1 W load (camera at full power 3 W, monitor 7 W, converter 90 %; the dimmed camera, about 0.8 W, makes the run longer)",
        round(run_cold, 2), 4.0, "h", rule="above", margin=0.1, closed_by=f"VDS-CAL-001 F4--10 ({cal('F4--10'):.2f} h)")

# ------------------------------------------------------------------------------ Chemistry
c.cited("S16", "Aluminium tube with stainless pins, wire and screws and a brass air barb survives a wet shift in a collapsed building",
        "Chemistry", "Electrochemistry and batteries",
        "Galvanic series: 6061 aluminium is anodic to stainless steel and brass, so a wet crevice corrodes the aluminium; anodising insulates, the wet time is one shift and the kit is rinsed and dried after use",
        "No rate can be stated at first order; the pins and screws sit in anodised or nylon-tipped holes", PLAUSIBLE, closed_by="")
c.cited("S17", "A LiFePO4 pack delivers its rated energy at -10 C and is charged only above 0 C", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 cells discharge at low temperature with reduced capacity (70 % assumed) and must not be charged below freezing; the exact limits are on the pack datasheet, to confirm when bought",
        "Charging indoors away from the kit is already a stop (build plan S2, S8)", PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------------------ Biology and safety science
c.cited("S18", "A bite valve passes water only when bitten, with 19.6 kPa of water head behind it", "Biology", "Human physiology",
        "Water pressure rho g h = 19.6 kPa at 2 m; a silicone slit bite valve stays closed until bitten at a cracking pressure that must exceed it (supplier figure, not yet known)",
        "Cracking pressure and the survivor's ability to bite and sip are to confirm at TRL 4 with the medical lead", PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------------------ Mathematics
c.order_of_magnitude("S19", "The assembled probe is 4.54 m long", "Mathematics", "Units and dimensional analysis", claimed=cal("A3"), estimate=4 * 1050 + 313 + 30,
                     unit="mm", law="Four 1,050 mm sections plus a 313 mm head plus the tail cap", closed_by="VDS-CAL-001 A3")
c.balance("S20", "The setup time of 2.2 min is the sum of its steps", "Mathematics", "Units and dimensional analysis",
          {"steps": 2.2}, {"H1": cal("H1"), "H2": cal("H2"), "H3": cal("H3"), "H4": cal("H4"), "H5": cal("H5")}, "min",
          law="Sum of the timed steps (estimates, to time in drills)", closed_by="VDS-CAL-001 H6")
c.claim("S21", "The head fits a standard 51 mm core hole", "Engineering and technology", "Standards practice",
        "Geometry: largest diameter on the probe 48 mm against a 51 mm core hole, 1.5 mm a side",
        cal("A1"), 51.0, "mm", margin=0.05, closed_by="VDS-CAL-001 A1, A2")
c.claim("S22", "The kit costs less than the value-engineering target", "Engineering and technology", "Standards practice",
        "Sum of bom/bom.csv against budget_usd 2,000 (a control target, not a limit)", cal("I2"), cal("I3"), "USD", margin=0.1,
        closed_by="VDS-CAL-001 I2")

# ------------------------------------------------------------------------------ Option B: reel-fed glass-fibre push rod
E_GRP, D_B = 40000.0, 10.0           # MPa (typical pultruded E-glass rod, to confirm), mm
I_B = math.pi / 64 * D_B ** 4
w_b = 1900.0 * (math.pi / 4 * (D_B / 1000) ** 2) * G / 1000.0   # N per mm
F_B = 0.5 * G
droop_b = w_b * 1000 ** 4 / (8 * E_GRP * I_B) + F_B * 1000 ** 3 / (3 * E_GRP * I_B)
c.cited("SB1", "Option B (after the fix): the 10 mm glass-fibre rod reaches 4 m only where the void floor or debris carries it; free reach in air is capped at 1 m", "Physics",
        "Strength of materials",
        f"Cantilever droop at only 1 m is {droop_b:.0f} mm (E 40 GPa assumed, I = {I_B:.0f} mm4), growing with L^3: a flexible rod cannot hold a head in free air beyond about 1 m. Fix: B is claimed only where the void floor or debris carries the rod, free reach capped at 1 m",
        "Floor-supported reach plausible, to test; the first claim (4 m in free air) failed and was restated", PLAUSIBLE, closed_by="VDS-OPT-001; VDS-DDR-006 F2")
eps_b = D_B / (2 * 320.0 + D_B)
c.cited("SB2", "Option B: winding the rod on a 640 mm hub keeps the bending strain at about 1.5 per cent", "Physics", "Strength of materials",
        f"Elastic strain of a rod bent on a drum, e = d / (2R + d) = {eps_b * 100:.2f} per cent, about 600 MPa at 40 GPa; that is a large share of the strength of pultruded glass-fibre rod and glass composites creep under sustained load, so a larger hub or the supplier's allowable strain is needed (independent review)",
        f"{eps_b * 100:.2f} per cent against an unknown allowable", PLAUSIBLE, closed_by="VDS-OPT-001")
# ------------------------------------------------------------------------------ Option C: tripod and winch
I_LEG = math.pi / 64 * (32.0 ** 4 - 28.0 ** 4)
pcr_leg = math.pi ** 2 * E_AL * I_LEG / 1800.0 ** 2
c.claim("SC1", "Option C: each tripod leg carries the 150 N hanging load with a factor of 10 against buckling", "Physics", "Strength of materials",
        "Euler buckling of a 32 x 2 mm aluminium tube, 1.8 m, pinned ends; load shared by three legs and taken as 150 N per leg (conservative)",
        1500.0, round(pcr_leg, 0), "N", closed_by="VDS-OPT-001")
c.cited("SC2", "Option C: the sonde hangs vertical and steady on its rope and the lines hang clear in a vertical hole", "Physics", "Mechanics and statics",
        "A body hanging from an eye above its centre of mass hangs upright; it spins freely on the rope, so the picture rotates and the bite valve swings; steering is none",
        "Works only down a vertical hole; side entry is not possible", PLAUSIBLE, closed_by="")

if __name__ == "__main__":
    print(f"After the fix: tip housing {t_fix:.1f} C at 35 C ambient and {t_fix45:.1f} C at 45 C (0.8 W, black anodised)")
    for q in (3.0, 1.5, 1.0, 0.8):
        print(f"  {q} W, eps 0.85: " + ", ".join(f"{t} C ambient -> {tip_temp(q, t, 0.85):.1f}" for t in (20, 35, 45)))
    print(f"Buckling {pcr:.0f} N, droop {droop:.1f} mm, button stress {s_btn:.0f} MPa, drip {q_ml:.2f} mL/min, Re {re:.0f}, "
          f"cold run {run_cold:.2f} h, B droop at 1 m {droop_b:.0f} mm, C leg {pcr_leg:.0f} N")
    c.write()
