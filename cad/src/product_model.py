"""VoidScope product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the four anodised rod sections with painted depth
bands under clear heat-shrink, the teal couplers and red snap buttons at the joints, the turned
head (collar with six air outlets and the speaker grille, nose with the camera window and LEDs,
the blue bite valve parked on top with its water tube in the groove), the steerable camera tip
(VDS-DDR-003: black silicone sheath over the bending section, aluminium tip housing with the camera
window and LEDs), shown bent 45 deg in the hero and detail views and straight in the exploded view,
the steering control with its red lever on section 4, the tail cap with its brass air barb and the black grip; the air hose, camera cable and water tube running to the surface unit;
the orange IP67 case with its lid open, the 7 in monitor showing a picture, the equipment plate
with battery, blower, flow meter and control modules, the wall fittings and intake filter; the
water bottle on its light stand. Context: a broken concrete wall with a 51 mm core hole that the
probe passes through, rubble at its foot, and a 1.75 m mannequin standing where the operator
stands. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_components() in
model.py, with the same axes (probe along +X at the deployed height, Z up, ground at z = 0).
The rod, couplers, buttons, head, tail cap, grip, case, plate and every part in the case are the
model.py solids themselves. Departures from model.py (depth bands, monitor picture, LED dots,
speaker grille holes, hoses and cables drawn to the surface unit, the rubble context) are listed
in docs/REVIEW.md and were accepted under Amish's 2026-10-03 pre-approval.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import Box, Pos, Rot, Sphere  # noqa: E402
from model import PARAMS, build_components, derived, bent_tip, xcyl, xtube, rod_between  # noqa: E402

TIP_BEND = -45.0        # deg; the hero and detail views show the tip steered 45 deg toward -Y (toward the viewer)

TITLE = "VoidScope: rubble void search probe with water and air lines"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["probe", "head", "tipbent", "surface", "lines", "context"], "explode": False, "el": 22, "az": -35,
     "note": "Product render from the front right and above (about 22 deg elevation): the probe pushed through a 51 mm "
             "core hole in a broken wall, head in the void beyond with its camera tip steered 45 deg, steering lever on "
             "the rod ahead of the grip, surface unit with its lid open and water bottle on its stand beside the "
             "operator (1.75 m mannequin)"},
    {"name": "exploded", "groups": ["probe", "head", "tipstraight", "surface"], "explode": True, "el": 28, "az": -50,
     "note": "Exploded view from the front right and above (about 28 deg elevation): rod sections, couplers and snap "
             "buttons pulled apart along the probe; collar, speaker, nose, base link, bending links, tip housing and "
             "camera ahead of section 1; steering control lifted off section 4; tail cap and grip behind; surface unit "
             "plate, battery, blower, flow meter, modules and monitor lifted out of the case"},
    {"name": "detail", "groups": ["head", "tipbent"], "explode": False, "el": 18, "az": -30,
     "note": "Detail from the front right, slightly above (about 18 deg elevation), close on the head: camera tip "
             "steered 45 deg on its sheathed bending section, camera window and LEDs in the tip housing, bite valve "
             "parked on top of the nose with its water tube in the groove, six air outlets and the speaker grille on "
             "the collar, front of section 1 with its snap button"},
]

C_AL = "#C9CED6"        # clear anodised aluminium
C_HEAD = "#8A9099"      # bead-blasted aluminium
C_TEAL = "#0F766E"
C_RED = "#B91C1C"
C_BAND = "#111827"
C_CASE = "#E8891C"      # orange case
C_LID = "#E8891C"
C_BLK = "#1F2937"
C_CONC = "#A8A29E"
C_CLAY = "#B9B4AC"

LOOK = {  # model key: (display name, colour, material, group)
    "collar": ("Collar, bead-blasted aluminium", C_HEAD, "metal", "head"),
    "nose": ("Nose, bead-blasted aluminium", "#9AA0A8", "metal", "head"),
    "nose_screws": ("Nose screws, stainless", "#D1D5DB", "metal", "head"),
    "spg_grommet": ("Spigot grommet, rubber", C_BLK, "rubber", "head"),
    "speaker": ("Speaker", "#374151", "plastic", "head"),
    "spk_cover": ("Speaker cover, stainless mesh", "#B8BCC2", "metal", "head"),
    "bite": ("Bite valve, blue silicone", "#2563EB", "rubber", "head"),
    "tailcap": ("Tail cap, aluminium", C_HEAD, "metal", "probe"),
    "barb": ("Air barb, brass", "#B08D57", "metal", "probe"),
    "tc_grommets": ("Tail cap grommets, rubber", C_BLK, "rubber", "probe"),
    "tc_pins": ("Tail cap pins, aluminium", C_AL, "metal", "probe"),
    "grip": ("Grip, black rubber", "#151515", "rubber", "probe"),
    "case": ("Case base, orange polypropylene", C_CASE, "plastic", "surface"),
    "lid": ("Case lid, orange polypropylene", C_LID, "plastic", "surface"),
    "eplate": ("Equipment plate, aluminium", "#B5BAC1", "metal", "surface"),
    "espacers": ("Plate spacers, nylon", "#E5E7EB", "plastic", "surface"),
    "battery": ("Battery pack, LiFePO4", "#2B2F36", "plastic", "surface"),
    "blower": ("Blower, black", "#1F2937", "plastic", "surface"),
    "blower_legs": ("Blower standoffs, brass", "#B08D57", "metal", "surface"),
    "modules": ("Control modules tray with switch and knob", "#334155", "plastic", "surface"),
    "flowmeter": ("Flow meter, clear body", "#BFE3F2", "clear", "surface"),
    "fm_bracket": ("Flow meter bracket, aluminium", "#9CA3AF", "metal", "surface"),
    "fittings": ("Wall fittings, black and brass", C_BLK, "plastic", "surface"),
    "filter": ("Intake filter, grey", "#D1D5DB", "plastic", "surface"),
    "monitor": ("Monitor housing, black", "#111111", "plastic", "surface"),
    "dbracket": ("Monitor bracket, aluminium", "#9CA3AF", "metal", "surface"),
    "stand": ("Reservoir light stand, black", "#202225", "painted", "surface"),
    "base": ("Base link, bead-blasted aluminium", "#9AA0A8", "metal", "head"),
    "ctrl_body": ("Steering control body, black nylon", "#1F2937", "plastic", "probe"),
    "drum": ("Steering drum, aluminium", "#B5BAC1", "metal", "probe"),
    "shaft": ("Drum shaft, stainless", "#D1D5DB", "metal", "probe"),
    "lever": ("Steering lever, red", C_RED, "painted", "probe"),
    "knob": ("Friction lock knob, black", "#151515", "plastic", "probe"),
    "ctrl_screw": ("Clamp screw, stainless", "#D1D5DB", "metal", "probe"),
    "bottle": ("Water bottle, translucent polypropylene", "#DCEBF5", "clear", "surface"),
}
TIP_LOOK = {  # steerable tip parts, drawn bent (hero, detail) or straight (exploded)
    "link1": ("Bending link 1", "#2B2F36", "plastic"), "link2": ("Bending link 2", "#2B2F36", "plastic"),
    "link3": ("Bending link 3", "#2B2F36", "plastic"), "link4": ("Bending link 4", "#2B2F36", "plastic"),
    "tpins": ("Hinge pins, stainless", "#D1D5DB", "metal"),
    "sheath": ("Bending section sheath, black silicone", "#151515", "rubber"),
    "tiph": ("Tip housing, bead-blasted aluminium", C_HEAD, "metal"),
    "grubs": ("Camera grub screws, stainless", "#D1D5DB", "metal"),
    "camera": ("Camera head, stainless, window and lens", "#2B2F36", "metal"),
}
EXPLODE = {"camera": (700, 0, 0), "nose": (380, 0, 0), "nose_screws": (380, 0, 60),
           "base": (440, 0, 0), "link1": (500, 0, 0), "link2": (515, 0, 0), "link3": (530, 0, 0), "link4": (545, 0, 0),
           "tpins": (520, 0, 70), "sheath": (520, 0, -90), "tiph": (620, 0, 0), "grubs": (620, 0, 60),
           "ctrl_body": (0, 0, 120), "drum": (0, 0, 220), "shaft": (0, -80, 220), "lever": (0, 80, 220), "knob": (0, -130, 220),
           "ctrl_screw": (0, 0, 60),
           "collar": (160, 0, 0), "spg_grommet": (200, 0, 0), "speaker": (160, -90, 0), "spk_cover": (160, -130, 0),
           "bite": (380, 0, 90), "tailcap": (-200, 0, 0), "barb": (-200, -60, 0), "tc_grommets": (-260, 0, 0),
           "tc_pins": (-200, 0, 50), "grip": (0, 0, 120), "eplate": (0, 0, 180), "espacers": (0, 0, 90),
           "battery": (0, 0, 360), "blower": (0, 0, 360), "blower_legs": (0, 0, 300), "modules": (0, 0, 360),
           "flowmeter": (0, 0, 420), "fm_bracket": (0, 0, 300), "fittings": (0, 150, 0), "filter": (0, -150, 0),
           "monitor": (-160, 0, 0), "dbracket": (-80, 0, 0), "lid": (0, 0, 0), "case": (0, 0, 0)}


def _polyline(points, r):
    out = None
    for a, b_ in zip(points[:-1], points[1:]):
        seg = rod_between(a, b_, r)
        out = seg if out is None else out + seg
    for p in points[1:-1]:
        out = out + Pos(*p) * Sphere(r)
    return out


def _bezier(p0, p1, p2, p3, n=10):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3; b_ = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t ** 2; d = t ** 3
        pts.append(tuple(a * p0[k] + b_ * p1[k] + c * p2[k] + d * p3[k] for k in range(3)))
    return pts


def product_parts(P=PARAMS):
    D = derived(P)
    C = build_components(P)
    zc = P["z_axis"]
    n = P["n_sec"]
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(float(v) for v in explode)})

    # rod sections, couplers, buttons and pins; each section explodes back along the probe
    for k in range(1, n + 1):
        ex = (-(k - 1) * 160.0, 0, 0)
        add(f"Rod section {k}, clear anodised aluminium", C[f"rod{k}"].shape, C_AL, "metal", 5, "probe", ex)
        add(f"Coupler {k}, teal anodised aluminium", C[f"coupler{k}"].shape, C_TEAL, "metal", 6, "probe", (ex[0] + 80, 0, 0))
        add(f"Snap button {k}, red", C[f"button{k}"].shape, C_RED, "painted", 6, "probe", (ex[0] + 80, 0, 0))
        add(f"Coupler pins {k}, aluminium", C[f"pins{k}"].shape, C_AL, "metal", 6, "probe", ex)
    # depth bands every 100 mm from the tip, under clear heat-shrink (appearance only)
    od = P["rod"][0]
    bands = None
    xt = D["x_tip"]
    for i in range(1, 50):
        x = xt - 100.0 * i
        if x < D["grip_end"] + 20 or x > D["x_collar"] - 5:
            continue
        if any(abs(x - s1) < 8 or abs(x - s0) < 40 for s0, s1 in D["sections"]):
            continue
        w = 6.0 if i % 5 == 0 else 2.5
        ring = xtube(x - w / 2, x + w / 2, od / 2 + 0.15, od / 2, 0, zc)
        bands = ring if bands is None else bands + ring
    add("Depth bands, black paint", bands, C_BAND, "painted", 5, "probe")
    # every other modelled part with its look
    for key, (name, col, mat, grp) in LOOK.items():
        add(name, C[key].shape, col, mat, C[key].bom, grp, EXPLODE.get(key, (0, 0, 0)))
    # steerable tip: straight for the exploded view, steered TIP_BEND for the hero and detail views
    bent = bent_tip(P, TIP_BEND, C)
    for key, (name, col, mat) in TIP_LOOK.items():
        add(name, C[key].shape, col, mat, C[key].bom, "tipstraight", EXPLODE.get(key, (0, 0, 0)))
        add(name, bent[key], col, mat, C[key].bom, "tipbent")
    # monitor picture (appearance only): a dark green-grey screen on the monitor's face
    mon = C["monitor"].shape.bounding_box()
    # the lid is open toward -X: the screen face is the monitor's -X face
    scr = Pos(mon.min.X - 0.4, (mon.min.Y + mon.max.Y) / 2, (mon.min.Z + mon.max.Z) / 2) * Box(0.8, mon.size.Y - 16, mon.size.Z - 16)
    add("Monitor screen, glass", scr, "#2F4A3A", "screen", 16, "surface", EXPLODE["monitor"])
    # camera LEDs as small dots on the camera face (appearance only), straight and steered
    camz = zc + P["nose"][3]
    leds = None
    for i in range(12):
        a = 2 * math.pi * i / 12
        dot = Pos(D["cam_x1"] + 0.2, 10.5 * math.cos(a), camz + 10.5 * math.sin(a)) * Sphere(1.0)
        leds = dot if leds is None else leds + dot
    lens = xcyl(D["cam_x1"] - 0.5, D["cam_x1"] + 0.3, 4.5, 0, camz)

    def steer(shape):
        ph = TIP_BEND / P["n_joint"]
        for x in reversed(D["pivots"]):
            shape = Pos(x, 0, camz) * Rot(0, 0, ph) * Pos(-x, 0, -camz) * shape
        return shape
    add("Camera LEDs, white", leds, "#FFF7E0", "clear", 1, "tipstraight", EXPLODE["camera"])
    add("Camera lens, glass", lens, "#0B0F14", "clear", 1, "tipstraight", EXPLODE["camera"])
    add("Camera LEDs, white", steer(leds), "#FFF7E0", "clear", 1, "tipbent")
    add("Camera lens, glass", steer(lens), "#0B0F14", "clear", 1, "tipbent")
    # water tube and cable inside the rod (head end only, visible through the outlets and the groove)
    add("Water tube, blue polyurethane", C["wtube"].shape & Pos(D["x_collar"] + 60, 0, zc) * Box(240, 80, 80), "#3B82F6", "plastic", 11, "head",
        (380, 0, 90))
    # lines from the tail cap to the surface unit (appearance only)
    bx0 = P["barb"][4]
    barb_end = (bx0, -(P["tailcap"][0] / 2 + 8 + P["barb"][3]), zc)
    x0, y0 = P["case_at"]
    L, W = P["case"][:2]
    air_out = (x0 + P["fittings"]["air"][0], y0 + W + 21, P["fittings"]["air"][1])
    cam_sock = (x0 + P["fittings"]["camera"][0], y0 + W + 21, P["fittings"]["camera"][1])
    hose = _polyline(_bezier(barb_end, (bx0, -400, zc - 150), (air_out[0] - 200, air_out[1] + 300, 30), air_out), 9.0)
    add("Air hose, translucent silicone", hose, "#E5E7EB", "rubber", 24, "lines")
    st = (-P["stub"], 0, zc + P["cable"][0])
    cable = _polyline(_bezier(st, (-450, 0, zc - 200), (cam_sock[0] - 300, cam_sock[1] + 250, 25), cam_sock), 3.0)
    add("Camera cable, black", cable, "#111111", "rubber", 9, "lines")
    gs = (-P["stub"], 0, zc + P["guide"][0])
    sx, sy = P["stand"][:2]
    spig = (sx + 70, sy, P["bottle"][2] - 25)
    wline = _polyline(_bezier(gs, (-420, 60, zc + 100), (spig[0] - 300, spig[1] + 200, spig[2] - 400), spig), 2.0)
    add("Water tube to the bottle, blue polyurethane", wline, "#3B82F6", "plastic", 11, "lines")
    # context: broken concrete wall with a 51 mm core hole, rubble, mannequin
    xw = 1800.0
    wall = Pos(xw + 120, 0, 700) * Box(240, 1600, 1400) + Pos(xw + 120, -350, 1450) * Rot(18, 0, 0) * Box(240, 900, 300)
    wall = wall - xcyl(xw - 10, xw + 260, 25.5, 0, zc)
    add("Broken concrete wall with a 51 mm core hole", wall, C_CONC, "plastic", None, "context")
    rub = None
    for (rx, ry, rz, a, s) in ((xw - 150, 500, 90, 20, 260), (xw - 60, -620, 70, -35, 200), (xw + 500, 300, 110, 10, 300),
                               (xw + 700, -400, 80, 40, 220), (xw - 260, 150, 40, 65, 120)):
        blk = Pos(rx, ry, rz) * Rot(0, 0, a) * Rot(12, 8, 0) * Box(s, s * 0.7, s * 0.5)
        rub = blk if rub is None else rub + blk
    add("Concrete rubble", rub, "#9C958E", "plastic", None, "context")
    from context_parts import mannequin
    person = Pos(-520, 380, 0) * Rot(0, 0, 90) * mannequin(1750, "stand")
    add("Person, 1.75 m mannequin (scale)", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:8s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
