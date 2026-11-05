"""VoidScope parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check, STEP per part and per assembly (cad/step/)
    python cad/src/model.py               part list with masses, and STL of the chosen design (cad/stl/)
    python cad/src/model.py --check       option A's 180 pairwise constructability checks (vds_geom.py)

Axes: the probe lies on the X axis at the deployed height z_axis (held at waist height), tip toward +X; the
operator stands behind the back of the grip at x < 0. Z is up with the ground at z = 0. The surface unit
stands on the ground on the -Y side with its lid open toward the operator; the reservoir stand is beside it.

Options (VDS-OPT-001; option A is the design of record, VDS-DDR-001 to 004; B and C were added on 2026-10-24,
VDS-DDR-005, and are proposals awaiting Amish):
    A  rigid sectioned rod with a steerable camera tip: four 38.1 mm aluminium sections joined by snap-button
       couplers, the bore is the air duct, a guide tube inside carries the water tube to a bite valve on the nose
    B  reel-fed flexible push cable: a 10 mm glass-fibre push rod runs off a hand reel, the air hose, water tube
       and camera cable are clipped to it, a small turned head carries camera, speaker, bite valve and air outlets
    C  tripod and winch lowered sonde: a three-leg aluminium tripod over a drilled hole, a hand winch pays a
       stainless wire rope down with the sonde, the lines hang on the rope; for vertical holes through a slab

Every part is a cad_parts.part() dict: made, bought, fastener or context. BOM line numbers are given for option A
only (the chosen design carried to the drawing, priced BOM and build plan). Option geometry for A comes from
vds_geom.py (its builders are unchanged, so every dimension is the one in VDS-CAL-001); the drill-and-fasten
work, the individual fasteners, the materials and the edge breaks are added here; B and C are in vds_options.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import cad_parts as cp  # noqa: E402
from cad_parts import part, at, break_edges  # noqa: E402

TITLE = "VoidScope"

# Top-level parameters (mm). Edit these, not the geometry. Option A first (the calculation note, drawings and build
# plan read these), then the dimensions of options B and C.
PARAMS = {
    "z_axis": 950.0,                 # probe axis height in the deployed layout (held at waist height)
    # 5 rod sections: OD, wall, length; number of sections
    "rod": (38.1, 1.47, 1050.0), "n_sec": 4,
    # 6 couplers: OD, wall, length, depth bonded into the section's front end
    "coupler": (34.93, 2.11, 120.0, 60.0),
    # 6 snap button (bought V-spring button): button dia, distance from the receiving end, proud of the tube
    "button": (8.0, 30.0, 1.5), "button_hole": 8.5,
    #   V-spring envelope: width (Z), length (X) behind the button
    "spring": (8.0, 24.0),
    # 6 cross pins locking each coupler (and the tail cap): dia, distance from the section end
    "pin": (4.0, 30.0), "tc_pin_x": 20.0,
    # 7 tail cap: flange OD and length, plug OD and length, plug bore, end wall thickness
    "tailcap": (44.0, 25.0, 35.0, 40.0, 30.0, 8.0),
    #   side air barb: thread dia (1/4 BSP), hex across flats, barb OD (12 mm hose), barb length, x from the back face
    "barb": (13.2, 17.0, 12.0, 22.0, 12.5),
    #   grommets in the end wall: (z of centre, hole dia) for the cable and the guide
    "grommets": {"cable": (-10.0, 10.0), "guide": (10.0, 12.0)},
    # 8 grip: OD, length, start x
    "grip": (47.0, 300.0, 35.0),
    # 9, 10, 11 lines inside the rod: (z of centre, OD, ID); stub length behind the tail cap
    "cable": (-10.0, 6.0), "guide": (10.0, 8.0, 6.0), "wtube": (4.0, 2.5), "stub": 150.0,
    # 3 collar: OD, body length, socket depth, plenum bore; spigot OD and length; spigot bore dia
    #   and its z offset (on the camera axis); button spotface dia and depth below the OD
    "collar": (48.0, 98.0, 60.0, 30.0), "spigot": (40.0, 12.0), "spigot_bore": (14.0, -6.5),
    "spotface": (14.0, 3.7),
    #   air outlets: hole dia, x from the collar back face, angles (deg from +Y toward +Z); the two lower
    #   side outlets sit at 240 and 300 deg so the steering housings (215 and 325 deg) pass them (VDS-DDR-003)
    "outlets": (5.0, 79.0, (0.0, 45.0, 135.0, 240.0, 270.0, 300.0)),
    # 4 speaker: dia, thickness, cover thickness; pocket dia; x of centre from the collar back face; floor |y|
    "speaker": (20.0, 4.0, 0.5), "spk_pocket": 20.5, "spk_x": 79.0, "spk_floor": 16.8,
    #   water exit: hole dia, x where its axis crosses z = 12 (from the collar back face), slope 45 deg
    "wexit": (4.5, 72.0), "groove": (4.5, 20.0),     # groove width and floor height (z) on top
    # 2 nose: length, counterbore dia (on the spigot), bore dia (through, on the camera axis), camera axis z
    #   (the camera now sits in the steerable tip; the old front lip is gone, VDS-DDR-003)
    "nose": (75.0, 40.2, 29.3, -6.5),
    # 30 to 34 steerable camera tip (VDS-DDR-003, Amish 2026-10-03, decision 3A), all on the camera axis:
    #   link OD, bore, body length, gap between bodies (the gap closes at 18 deg a joint); number of joints
    "link": (33.0, 23.0, 10.0, 5.25), "n_joint": 5,
    #   hinge lugs at top and bottom: width, split radius (outer lugs above it, inner lugs below), radial and
    #   end clearance; hinge pin dia
    "lug": (8.0, 14.0, 0.1, 0.4), "tpin": 2.0,
    #   steering wires in the links: distance from the camera axis (on +/-Y), hole dia, wire dia
    "swire": (14.0, 1.2, 0.6),
    #   31 base link: spigot OD (in the nose bore) and length, flange length, bore; M3 grub screws x back from the nose front
    "base": (29.25, 14.0, 8.0, 12.0), "base_screw": (3.0, 7.0),
    #   32 tip housing: back wall length (23 mm bore), camera bore depth, window recess ahead of the camera;
    #   anchor cross-hole dia and x from the back face; M3 grub screws: x from the camera's back, angles
    "tiph": (8.0, 58.0, 3.0), "anchor": (3.0, 4.0), "grub": (3.0, 20.0, (60.0, 120.0)),
    #   sheath over the bending section: wall
    "sheath": 0.6,
    #   33 steering housings in the rod: OD, |y| and z of centre (at 215 and 325 deg); stop counterbore dia
    #   and depth in the collar front wall; hole dia in section 4 and the control body
    "housing": (3.0, 10.5, -7.5), "hstop": (3.2, 2.0), "hhole": (4.0, 3.2),
    #   34 steering control on section 4 ahead of the grip: x of the drum centre; clamp collar outer radius and
    #   length; pad height above the axis; cheek inner |y|, thickness, height above the pad; drum radius (groove
    #   root), half width and centre height above the axis; shaft dia; lever length, width, thickness
    "ctrl": (375.0, 25.0, 64.0, 30.0), "cheek": (14.0, 3.0, 40.0), "drum": (18.0, 13.5, 50.0), "shaft": 6.0,
    "lever": (50.0, 12.0, 3.0),
    #   bite valve pocket: width, floor z, length back from the nose front
    "pocket": (11.5, 12.0, 50.0),
    #   M4 screws nose to spigot: x from the nose back face, angles
    "nose_screws": (6.0, (30.0, 150.0, 270.0)),
    # 1 camera head (bought, IP68): dia, length; rubber spacer ring length
    "camera": (29.0, 55.0),
    # 11 bite valve: OD, length
    "bite": (11.0, 40.0),
    # 14 surface unit case (bought): outside L (X) x W (Y), base height, lid height, wall; position of
    #   the base corner nearest the origin; lid opening angle
    "case": (410.0, 330.0, 125.0, 50.0, 3.0), "case_at": (250.0, -1000.0), "lid_open": 100.0,
    # 15 equipment plate: L x W x t, spacer height, inset from the case's inner walls (x, y)
    "eplate": (330.0, 300.0, 3.0), "espacer": 6.0, "eplate_in": (8.0, 9.0),
    # 17 battery (fitted pack): L x W x H, x, y of its corner on the plate (from the plate corner)
    "battery": (151.0, 65.0, 94.0), "bat_at": (12.0, 12.0),
    # 18 blower: L x W x H lying flat on standoffs (height), corner on the plate
    "blower": (97.0, 94.0, 33.0), "blower_off": 10.0, "blower_at": (12.0, 110.0),
    # 20 flow meter (panel rotameter, vertical): body W (X) x D (Y) x H; bracket angle leg x t; corner on the plate
    "flowmeter": (32.0, 30.0, 100.0), "fm_angle": (40.0, 3.0), "fm_at": (280.0, 230.0),
    # 21 control modules tray: L x W x H; corner on the plate
    "modules": (110.0, 70.0, 35.0), "mod_at": (175.0, 12.0),
    # 23 wall fittings on the +Y wall (toward the probe): (x from the case's -X end, z) for the camera
    #   socket, the air outlet and the headset socket
    "fittings": {"camera": (120.0, 70.0), "air": (300.0, 70.0), "headset": (200.0, 70.0)},
    # 19 intake filter on the -Y wall: dia, length, x from the -X end, z
    "filter": (60.0, 70.0, 150.0, 65.0),
    # 16 display: 7 in monitor W x H x D; bracket plate t, stand-off from the lid floor, foot width
    "monitor": (185.0, 120.0, 28.0), "dbracket": (2.0, 15.0, 20.0),
    # 13 reservoir stand: position, hub height, pole top, leg spread radius, pole dia; 12 bottle dia,
    #   height, bottom height above the ground
    "stand": (1100.0, -830.0, 500.0, 1700.0, 420.0, 25.0), "bottle": (90.0, 210.0, 1350.0),
    # ---- fixings added at kit 1.9 (option A, VDS-DDR-005): M5 hex bolt sets and tapped screws, hole and pitch
    "m5_hole": 5.5, "vesa": 75.0,
    # ---- option B, reel-fed flexible push cable: push rod OD and deployed length from the reel's feed guide;
    #      rod clip pitch; head body OD and length; reel hub OD, flange OD, flange gap, hub length;
    #      frame base and height; the reel stands at x = -rb_x (behind the operator's hand) on the ground
    "b_rod": (10.0, 5200.0), "b_clip_pitch": 650.0, "b_head": (40.0, 150.0),
    "b_reel": (640.0, 800.0, 60.0), "b_frame": (420.0, 560.0), "b_z_axis": 950.0, "b_reel_at": (-1500.0, 0.0),
    "b_hose": (12.0, 10.0),
    # ---- option C, tripod and winch lowered sonde: leg tube OD and wall, leg length, spread radius at the feet,
    #      head height; winch drum OD and width; rope dia; sonde OD and length; hole centre at the origin (x, y)
    "c_leg": (32.0, 2.0, 1800.0), "c_spread": 800.0, "c_head_z": 1560.0, "c_winch": (120.0, 80.0),
    "c_rope": 4.0, "c_sonde": (44.0, 360.0), "c_depth": 4000.0, "c_hole": 51.0,
}

OPTIONS = {"A": "Rigid sectioned rod with steerable tip", "B": "Reel-fed flexible push cable", "C": "Tripod and winch lowered sonde"}
PRINCIPLES = {
    "A": "A 4.5 m rigid aluminium rod pushed straight into a 51 mm hole; its bore is the air duct, a guide tube inside "
         "carries the water, and a thumb-steered pinned-link tip bends the camera 90 degrees each way.",
    "B": "A 10 mm glass-fibre push rod runs off a hand reel and follows a bent void; air hose, water tube and camera "
         "cable are clipped to it and a small turned head carries camera, speaker, bite valve and air outlets.",
    "C": "A three-leg tripod over a drilled hole pays a stainless wire rope off a hand winch; the sonde with camera, "
         "speaker, bite valve and air outlets hangs on it, with the lines clipped to the rope, in a vertical hole.",
}
CHOSEN = "A"   # the design of record; B and C are alternatives. concept_chosen in project.yaml stays "A (proposed)"
OPTION_VIEWS = {
    "A": {"el": 20, "az": -35, "scale": "person", "ground_z": 0},
    "B": {"el": 20, "az": -35, "scale": "person", "ground_z": 0},
    "C": {"el": 20, "az": -35, "scale": "person", "ground_z": 0},
}
# Pairs of part-name fragments allowed to touch or overlap (none needed: every fit is modelled with its clearance)
ALLOWED_CONTACTS: list = []

import vds_geom as G  # noqa: E402  (needs PARAMS from this module)
from vds_geom import derived, build_components, bent_tip, BOM, PROBE_KEYS, probe_keys  # noqa: E402,F401
from vds_geom import HEAD_KEYS, TIP_KEYS, CTRL_KEYS, SURFACE_KEYS, assembly, build_parts  # noqa: E402,F401

# ---------------------------------------------------------------------------------------------------------
# Option A: legacy key -> (name, material, kind, split into single solids?)
# ---------------------------------------------------------------------------------------------------------
_SPEC = {
    "rod": ("Rod section {k}", "aluminium", "made", False),
    "coupler": ("Coupler {k}", "aluminium", "made", False),
    "button": ("Snap button {k}", "stainless", "bought", False),
    "spring": ("Snap button V-spring {k}", "stainless", "bought", False),
    "pins": ("Coupler cross pin {k}", "stainless", "fastener", True),
    "tailcap": ("Tail cap", "aluminium", "made", False),
    "barb": ("Air inlet barb, 1/4 BSP to 12 mm", "brass", "bought", False),
    "tc_grommets": ("Tail cap grommet", "epdm", "bought", True),
    "tc_pins": ("Tail cap cross pin", "stainless", "fastener", True),
    "grip": ("Grip", "epdm", "bought", False),
    "cable": ("Camera and speaker cable", "rubber_belt", "bought", False),
    "guide": ("Water guide tube, PTFE", "hdpe_natural", "bought", False),
    "wtube": ("Water tube, 4 x 2.5 mm", "polycarbonate", "bought", False),
    "bite": ("Bite valve", "hdpe_natural", "bought", False),
    "collar": ("Collar", "aluminium", "made", False),
    "nose": ("Nose", "aluminium", "made", False),
    "nose_screws": ("Nose screw M4", "stainless", "fastener", True),
    "camera": ("Camera head, IP68, 29 mm", "matte_black", "bought", False),
    "spg_grommet": ("Spigot grommet", "epdm", "bought", False),
    "speaker": ("Speaker, 20 mm IP67", "matte_black", "bought", False),
    "spk_cover": ("Speaker cover disc", "stainless", "made", False),
    "base": ("Base link", "aluminium", "made", False),
    "base_screws": ("Base link grub screw M3", "stainless", "fastener", True),
    "link": ("Bending link {k}", "hdpe_natural", "made", False),
    "tpins": ("Hinge pin 2 mm", "stainless", "fastener", True),
    "sheath": ("Bending section sheath", "epdm", "bought", False),
    "tiph": ("Tip housing", "aluminium", "made", False),
    "grubs": ("Camera grub screw M3", "stainless", "fastener", True),
    "swires": ("Steering wire {k}", "stainless", "bought", True),
    "housings": ("Steering housing {k}", "mild_steel", "bought", True),
    "ctrl_body": ("Steering control body", "hdpe_natural", "made", False),
    "drum": ("Steering drum", "aluminium", "made", False),
    "shaft": ("Drum shaft", "stainless", "bought", False),
    "lever": ("Steering lever", "hdpe_natural", "made", False),
    "knob": ("Friction lock knob", "matte_black", "bought", False),
    "ctrl_screw": ("Clamp screw", "stainless", "fastener", False),
    "case": ("Surface unit case, drilled", "matte_black", "bought", False),
    "lid": ("Surface unit case lid", "matte_black", "bought", False),
    "eplate": ("Equipment plate", "aluminium", "made", False),
    "espacers": ("Plate spacer {k}", "hdpe_natural", "fastener", True),
    "battery": ("Battery pack, LiFePO4", "matte_black", "bought", False),
    "blower": ("Blower", "matte_black", "bought", False),
    "blower_legs": ("Blower standoff {k}", "aluminium", "fastener", True),
    "modules": ("Control modules tray", "hdpe_natural", "bought", False),
    "flowmeter": ("Air flow meter", "polycarbonate", "bought", False),
    "fm_bracket": ("Flow meter bracket", "aluminium", "made", False),
    "fittings": ("Wall fitting {k}", "brass", "bought", True),
    "filter": ("Intake filter", "hdpe_natural", "bought", False),
    "monitor": ("Monitor with recorder", "matte_black", "bought", False),
    "dbracket": ("Monitor bracket", "aluminium", "made", False),
    "stand": ("Reservoir stand", "matte_black", "bought", False),
    "bottle": ("Water reservoir bottle", "pe_tank_white", "bought", False),
}
_FITTING_NAMES = ["camera socket GX16", "air bulkhead fitting", "headset socket"]
_EXPLODE = {
    "camera": (260, 0, 120), "nose": (220, 0, 60), "collar": (120, 0, 60), "speaker": (120, -160, 60),
    "rods": (0, 0, 220), "couplers": (0, 0, 120), "tailcap": (-260, 0, 60), "grip": (0, 0, 320),
    "cable": (0, 0, -120), "guide": (0, 0, -200), "waterset": (360, 0, 200), "bottle": (200, 0, 300),
    "stand": (300, 0, 0), "case": (0, 0, 0), "eplate": (0, 0, 220), "display": (0, 0, 520), "battery": (0, 0, 380),
    "blower": (0, 0, 420), "filter": (0, -200, 0), "flowmeter": (160, 0, 400), "modules": (0, 0, 460),
    "fittings": (0, 180, 0), "links": (360, 0, 60), "base": (300, 0, 60), "tiph": (420, 0, 60),
    "steer": (0, 0, -280), "ctrl": (0, 0, 200),
}


def _spec(key):
    import re
    m = re.fullmatch(r"(rod|coupler|button|spring|pins|link)(\d)", key)
    if m:
        return _SPEC[m.group(1)], m.group(2)
    return _SPEC[key], None


def _finish(shape, kind):
    """Break the edges of a bare box or cylinder, as a real cut, moulded or turned part has (made and bought parts)."""
    if not shape.is_valid:                       # the lugged links and the base link leave sliver faces; repair them
        try:
            fixed = shape.fix()
            if fixed.is_valid and abs(fixed.volume - shape.volume) < 0.01 * shape.volume:
                shape = fixed
        except Exception:
            pass
    if kind not in ("made", "bought"):
        return shape
    from cad_check import is_bare
    if not is_bare(shape):
        return shape
    try:
        bb = shape.bounding_box()
        r = min(1.5, 0.12 * min(bb.size.X, bb.size.Y, bb.size.Z))
        return break_edges(shape, max(r, 0.2))
    except Exception:
        return shape


def _drill(shape, pts, d, z0, z1):
    """Vertical holes of dia d at the (x, y) points, from z0 to z1."""
    from build123d import Cylinder, Pos
    for x, y in pts:
        shape = shape - Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, abs(z1 - z0))
    return shape


def _plate_parts(p, D, C):
    """Drilled plate, spacers, case floor and the screws that fasten the equipment (option A, VDS-DDR-005)."""
    from build123d import Cone, Cylinder, Pos
    hd = p["m5_hole"]
    L, W, t = p["eplate"]
    ct = p["case"][4]
    plate_sh, _, (px, py, pz) = G._eplate(p, D)
    x0, y0 = px, py
    z0 = ct + p["espacer"]
    # corner screws: countersunk from under the case floor, spacer, plate, washer and nyloc nut on top of the plate
    corners = [(x0 + x, y0 + y) for x in (15, L - 15) for y in (15, W - 15)]
    corners[0] = (x0 + 15, y0 + 93)            # the battery sits on the first corner, so its spacer and screw move clear
    # equipment bolts from under the plate (head in the 6 mm gap): blower standoffs, control tray, flow meter bracket
    bl = p["blower"]; bax, bay = p["blower_at"]; bo = p["blower_off"]
    blower_pts = [(px + bax + dx, py + bay + dy) for dx in (8, bl[0] - 8) for dy in (8, bl[1] - 8)]
    mL, mW, mH = p["modules"]; max_, may = p["mod_at"]
    mod_pts = [(px + max_ + dx, py + may + dy) for dx in (10, mL - 10) for dy in (10, mW - 10)]
    leg, ft = p["fm_angle"]; fax, fay = p["fm_at"]; fm = p["flowmeter"]
    fm_pts = [(px + fax + leg / 2, py + fay + dy) for dy in (6, fm[1] - 6)]
    plate = _drill(plate_sh, corners + blower_pts + mod_pts + fm_pts, hd, z0 - 1, z0 + t + 1)
    base = C["case"].shape
    base = _drill(base, corners, hd, -1, ct + 1)
    for (x, y) in corners:                     # countersink for the flat-head screw, flush with the outside
        base = base - Pos(x, y, 1.4) * Cone(5.0, 2.5, 2.8)
    return plate, base, dict(corners=corners, blower=blower_pts, mod=mod_pts, fm=fm_pts, z0=z0, ct=ct, pz=pz, px=px, py=py)


def option_a(p=PARAMS):
    """Option A at D3: the vds_geom solids with materials, single-solid fasteners, drilled holes and their bolts."""
    from build123d import Cone, Cylinder, Pos, Rot
    D = derived(p)
    C = build_components(p)
    C["wtube"].shape = C["wtube"].shape - C["bite"].shape
    out, seen = [], {}
    pl_info = None

    def emit(key, shape, name, material, kind, bom, group, k=None):
        shape = _finish(shape, kind)
        out.append(part(name, shape, material, kind=kind, bom=bom, group=group,
                        explode=_EXPLODE.get(group, (0, 0, 0)), note=key))

    # --- drilled equipment plate and case floor (replace the legacy solids)
    plate, base, info = _plate_parts(p, D, C)
    overrides = {"eplate": plate, "case": base}
    # --- equipment fixings need the holes in the other parts too
    hd, mh = p["m5_hole"], 5.5
    pz = info["pz"]
    bl = p["blower"]; bo = p["blower_off"]
    legs = C["blower_legs"].shape.solids()
    blower_sh = C["blower"].shape
    blower_sh = _blind(blower_sh, info["blower"], 5.0, pz + bo, pz + bo + 8)
    legs = [_drill1(s, 5.5) for s in legs]
    modules_sh = _blind(C["modules"].shape, info["mod"], 5.0, pz, pz + 8)
    fmb = C["fm_bracket"].shape
    fmb = _drill(fmb, info["fm"], hd, pz - 1, pz + p["fm_angle"][1] + 1)
    spacers = []
    for s in C["espacers"].shape.solids():
        c = s.bounding_box().center()
        tgt = min(info["corners"], key=lambda q: (q[0] - c.X) ** 2 + (q[1] - c.Y) ** 2)
        if abs(c.X - tgt[0]) > 1 or abs(c.Y - tgt[1]) > 1:       # the moved corner
            s = Pos(tgt[0] - c.X, tgt[1] - c.Y, 0) * s
        spacers.append(_drill1(s, 5.5))
    overrides.update(modules=modules_sh, blower=blower_sh, fm_bracket=fmb)
    mo, mon_parts = _monitor_work(p, D, C)
    overrides.update(mo)

    for key, c in C.items():
        (name, material, kind, split), kk = _spec(key)
        group = c.group
        shape = overrides.get(key, c.shape)
        bom = c.bom
        if key == "espacers":
            for i, s in enumerate(spacers, 1):
                emit(key, s, name.format(k=i), material, kind, bom, group)
            continue
        if key == "blower_legs":
            for i, s in enumerate(legs, 1):
                emit(key, s, name.format(k=i), material, kind, bom, group)
            continue
        if split:
            sols = shape.solids()
            for i, s in enumerate(sols, 1):
                nm = name
                if "{k}" in nm:
                    nm = nm.format(k=i)
                elif key == "fittings":
                    pass
                elif len(sols) > 1:
                    nm = f"{nm} {kk + '.' if kk else ''}{i}"
                if key == "fittings":
                    nm = f"Wall fitting: {_FITTING_NAMES[i - 1] if i <= 3 else i}"
                emit(key, s, nm, material, kind, bom, group)
            continue
        nm = name.format(k=kk) if "{k}" in name else name
        if key == "ctrl_screw":
            nm = name
        emit(key, shape, nm, material, kind, bom, group)

    out += _plate_fasteners(p, D, info)
    out += mon_parts
    return out


def _blind(shape, pts, d, z0, z1):
    from build123d import Cylinder, Pos
    for x, y in pts:
        shape = shape - Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)
    return shape


def _drill1(solid, d):
    """Axial hole through a vertical post (a standoff or spacer) about its own axis."""
    from build123d import Cylinder, Pos
    bb = solid.bounding_box()
    c = bb.center()
    return solid - Pos(c.X, c.Y, c.Z) * Cylinder(d / 2, bb.size.Z + 2)


def _plate_fasteners(p, D, info):
    """Screws, washers and nuts for the equipment plate, blower, control tray and flow meter bracket (M5)."""
    from build123d import Cone, Cylinder, Pos, Rot
    out = []
    ct, z0, pz = info["ct"], info["z0"], info["pz"]
    plate_t = p["eplate"][2]
    # corner screws: M5 flat-head from under the case floor; washer and nyloc nut on top of the plate
    for i, (x, y) in enumerate(info["corners"], 1):
        L = ct + p["espacer"] + plate_t + 1.0 + 4.7 + 2.0     # floor, spacer, plate, washer, nut, thread beyond
        head = Pos(x, y, 1.4) * Cone(5.0, 2.5, 2.8)           # 90 degree countersunk head, flush with the floor
        shank = Pos(x, y, 2.8 + (L - 2.8) / 2 - 0.0) * Cylinder(2.5, L - 2.8)
        out.append(part(f"M5 flat-head screw {i} (ISO 10642)", head + shank, "stainless", kind="fastener", bom=15, group="eplate"))
        out.append(part(f"M5 washer {i} (ISO 7089)", at(cp.washer(5), (x, y, z0 + plate_t)), "stainless", kind="fastener", bom=15, group="eplate"))
        nut = cp.hex_nut(5)
        ring = Pos(0, 0, 4.7 + 1.5) * (Cylinder(4.5, 3.0) - Cylinder(2.5, 3.2))
        out.append(part(f"M5 nyloc nut {i} (ISO 10511)", at(nut + ring, (x, y, z0 + plate_t + 1.0)), "stainless", kind="fastener", bom=15, group="eplate"))
    # equipment bolts: head and washer under the plate in the 6 mm gap, shank up through plate and post
    def under(pts, grip_up, label, bom, group, depth_in):
        for i, (x, y) in enumerate(pts, 1):
            L = grip_up + depth_in
            head = at(cp._hex(8, 3.5), (x, y, z0 - 1.0 - 3.5))     # head under washer, below the plate
            shank = Pos(x, y, z0 - 1.0 + L / 2) * Cylinder(2.5, L)
            sh = head + shank
            out.append(part(f"M5 hex screw {label} {i} (ISO 4017)", sh, "stainless", kind="fastener", bom=bom, group=group))
            out.append(part(f"M5 washer {label} {i} (ISO 7089)", at(cp.washer(5), (x, y, z0 - 1.0)), "stainless", kind="fastener", bom=bom, group=group))
    under(info["blower"], plate_t + p["blower_off"], "blower", 18, "blower", 6.0)
    under(info["mod"], plate_t, "tray", 21, "modules", 6.0)
    # flow meter bracket: bolt up through plate and the angle leg, washer and nut on top of the leg
    leg_t = p["fm_angle"][1]
    for i, (x, y) in enumerate(info["fm"], 1):
        L = plate_t + leg_t + 1.0 + 4.7 + 2.0 + 1.0
        head = at(cp._hex(8, 3.5), (x, y, z0 - 1.0 - 3.5))
        shank = Pos(x, y, z0 - 1.0 + L / 2) * Cylinder(2.5, L)
        out.append(part(f"M5 hex screw flow meter {i} (ISO 4017)", head + shank, "stainless", kind="fastener", bom=20, group="flowmeter"))
        out.append(part(f"M5 washer flow meter lower {i} (ISO 7089)", at(cp.washer(5), (x, y, z0 - 1.0)), "stainless", kind="fastener", bom=20, group="flowmeter"))
        out.append(part(f"M5 washer flow meter upper {i} (ISO 7089)", at(cp.washer(5), (x, y, z0 + plate_t + leg_t)), "stainless", kind="fastener", bom=20, group="flowmeter"))
        out.append(part(f"M5 hex nut flow meter {i} (ISO 4032)", at(cp.hex_nut(5), (x, y, z0 + plate_t + leg_t + 1.0)), "stainless", kind="fastener", bom=20, group="flowmeter"))
    return out


def _monitor_work(p, D, C):
    """VESA 75 screws from the bracket plate into the monitor, and M4 self-tapping screws from the bracket feet
    into the lid floor; returns (overrides, screw parts). Built with the lid closed, then posed with it."""
    from build123d import Cylinder, Pos
    L, W, hb, hl, t = p["case"]
    x0, y0 = p["case_at"]
    mw, mh, md = p["monitor"]
    bt, so, foot = p["dbracket"]
    zf = hb + hl - t
    cx, cy = x0 + L / 2, y0 + W / 2
    v = p["vesa"] / 2
    pts = [(cx + a, cy + b) for a in (-v, v) for b in (-v, v)]
    ztop = zf - so                       # top of the bracket plate
    zmon = zf - so - bt                  # monitor back face
    mon, br = C["monitor"].shape, C["dbracket"].shape
    pose = G._lid_pose
    parts = []
    for i, (x, y) in enumerate(pts, 1):
        br = br - pose(Pos(x, y, (ztop + zmon) / 2) * Cylinder(2.2, bt + 1), p)
        mon = mon - pose(Pos(x, y, zmon - 3.0) * Cylinder(2.0, 6.0), p)
        head = Pos(x, y, ztop + 1.4) * Cylinder(3.5, 2.8)
        shank = Pos(x, y, (ztop + zmon - 6.0) / 2) * Cylinder(2.0, ztop - zmon + 6.0)
        parts.append(part(f"M4 pan head screw monitor {i}", pose(head + shank, p), "stainless", kind="fastener", bom=16, group="display"))
    # bracket feet: the flange of each foot lies on the lid floor; screw through it into the lid
    fx = [cx - mh / 2 - 10 - foot / 2 + bt / 2, cx + mh / 2 + 10 + foot / 2 - bt / 2]
    lid = C["lid"].shape
    fpts = [(x, cy + s * (mw / 2 - 25)) for x in fx for s in (-1, 1)]
    for i, (x, y) in enumerate(fpts, 1):
        br = br - pose(Pos(x, y, zf - bt / 2) * Cylinder(2.2, bt + 1), p)
        lid = lid - pose(Pos(x, y, zf + 1.25) * Cylinder(2.0, 2.5), p)
        sc = Pos(x, y, zf - bt - 1.4) * Cylinder(3.5, 2.8) + Pos(x, y, (zf - bt + zf + 2.5) / 2) * Cylinder(2.0, bt + 2.5)
        parts.append(part(f"M4 self-tapping screw bracket {i}", pose(sc, p), "stainless", kind="fastener", bom=16, group="display"))
    return {"monitor": mon, "dbracket": br, "lid": lid}, parts


# ---------------------------------------------------------------------------------------------------------
from vds_options import option_b, option_c  # noqa: E402

_SURFACE_GROUPS = {"case", "eplate", "display", "battery", "blower", "filter", "flowmeter", "modules", "fittings",
                   "stand", "bottle"}
_CACHE: dict = {}


def legacy_components(option="A") -> dict:
    """Option A's parts keyed like the earlier component dictionary (rod1, tpins, nose ...), each key's solids fused,
    for the calculation note, the build plan pictures and the concept media, which look parts up by key. The geometry
    is the kit 1.9 model's (drilled plate, split fasteners and all); only the packaging is the old one."""
    from vds_geom import Comp
    option = option if isinstance(option, str) else "A"      # callers pass PARAMS; the dictionary describes option A
    groups: dict = {}
    for i, q in enumerate(components(option)):
        key = q.get("note") or f"x_{q['group']}_{i}"
        groups.setdefault(key, []).append(q)
    out = {}
    for key, qs in groups.items():
        sh = qs[0]["shape"]
        for q in qs[1:]:
            sh = sh + q["shape"]
        kind = "fixing" if qs[0]["kind"] == "fastener" else qs[0]["kind"]
        out[key] = Comp(qs[0]["name"], sh, qs[0]["bom"], kind, qs[0]["group"])
    return out


def surface_unit(parts) -> list:
    """The surface unit, reservoir stand and bottle with all their fasteners (shared by all three options)."""
    return [q for q in parts if q["group"] in _SURFACE_GROUPS]


def components(option: str) -> list:
    """The parts of an option as cad_parts.part() dicts (every option at D3)."""
    if "A" not in _CACHE:
        _CACHE["A"] = option_a(PARAMS)
    if option == "A":
        return list(_CACHE["A"])
    if option == "B":
        return option_b(PARAMS, surface_unit(_CACHE["A"]))
    if option == "C":
        return option_c(PARAMS, surface_unit(_CACHE["A"]))
    raise KeyError(option)


if __name__ == "__main__":
    import copy
    from build123d import Compound, export_stl
    if "--check" in sys.argv:
        sys.exit(1 if G.print_checks(C=build_components()) else 0)
    for opt in OPTIONS:
        ps = components(opt)
        real = [q for q in ps if q["kind"] != "context"]
        print(f"option {opt}: {len(real)} parts, {sum(cp.mass_kg(q) for q in real):.1f} kg")
    a = [q for q in components(CHOSEN) if q["kind"] != "context"]
    for q in a:
        if q["kind"] in ("made", "bought"):
            print(f"  {q['bom']:>3}  {q['name']:<50} {cp.mass_kg(q):6.2f} kg")
    out = HERE.parents[1] / "cad/stl"
    out.mkdir(parents=True, exist_ok=True)
    sets = {
        "voidscope-assembly": a,
        "voidscope-probe": [q for q in a if q["group"] not in _SURFACE_GROUPS],
        "voidscope-head": [q for q in a if q["note"] in HEAD_KEYS or q["note"] == "bite"],
        "voidscope-surface-unit": surface_unit(a),
    }
    for name, ps in sets.items():
        export_stl(Compound([copy.copy(q["shape"]) for q in ps]), str(out / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        print("wrote", name)
