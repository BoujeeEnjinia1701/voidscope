"""VoidScope parametric model (build123d), TRL 3, constructable design (VDS-DDR-002).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    voidscope-assembly.step / .stl      the whole kit as deployed: probe, surface unit, reservoir stand
    voidscope-probe.step / .stl         four rod sections, couplers, tail cap, grip, lines and head
    voidscope-head.step / .stl          collar, nose, camera head, speaker, bite valve and line ends
    voidscope-surface-unit.step / .stl  case, equipment plate and everything mounted in it
and prints the constructability checks (python cad/src/model.py --check prints them only).

Axes: the probe lies on the X axis at the deployed height z_axis, tip toward +X; the back face
of the tail cap is at x = 0. Z is up with the ground at z = 0. The camera's "up" is +Z: the
bite valve pocket is on top of the nose, the snap buttons are on the +Y side and the speaker on
the -Y side. The surface unit stands on the ground on the -Y side with its lid open toward the
operator, who stands behind the tail cap.

Constructable design (2026-10-03, decided under Amish's pre-approval, VDS-DDR-002):
    rod of four 1,050 mm sections of 38.1 x 1.47 mm 6061-T6 tube, joined by internal couplers
    (34.93 x 2.11 mm tube) pinned and bonded into each section's front end, locked by a bought
    V-spring snap button; the rod bore is the air duct; the camera cable and a PTFE guide tube
    carrying the single-use water tube run inside it and stay threaded through the sections
    (tent-pole storage); turned aluminium collar (socket, air plenum, six outlets, speaker
    pocket, water exit) and nose (eccentric camera bore, bite valve pocket); turned tail cap with
    the air inlet barb and two grommets; surface unit in a bought hard case with an equipment
    plate, battery, blower, flow meter, control modules, wall fittings and the monitor in the lid.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (VDS-CAL-001), the drawing VDS-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py), the build plan pictures (cad/src/build_plan_media.py) and the
appearance model (cad/src/product_model.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
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
    #   air outlets: hole dia, x from the collar back face, angles (deg from +Y toward +Z)
    "outlets": (5.0, 79.0, (0.0, 45.0, 135.0, 225.0, 270.0, 315.0)),
    # 4 speaker: dia, thickness, cover thickness; pocket dia; x of centre from the collar back face; floor |y|
    "speaker": (20.0, 4.0, 0.5), "spk_pocket": 20.5, "spk_x": 79.0, "spk_floor": 16.8,
    #   water exit: hole dia, x where its axis crosses z = 12 (from the collar back face), slope 45 deg
    "wexit": (4.5, 72.0), "groove": (4.5, 20.0),     # groove width and floor height (z) on top
    # 2 nose: length, counterbore dia (on the spigot), camera bore dia, camera axis z, lip bore, lip length
    "nose": (75.0, 40.2, 29.3, -6.5, 26.0, 3.0),
    #   bite valve pocket: width, floor z, length back from the nose front
    "pocket": (11.5, 12.0, 50.0),
    #   M4 screws nose to spigot: x from the nose back face, angles
    "nose_screws": (6.0, (30.0, 150.0, 270.0)),
    # 1 camera head (bought, IP68): dia, length; rubber spacer ring length
    "camera": (29.0, 55.0), "cam_ring": 5.0,
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
}

BOM = {  # model key: (BOM line, name)
    "camera": (1, "Camera head, IP68, 29 mm"),
    "nose": (2, "Nose"),
    "collar": (3, "Collar with air outlets"),
    "speaker": (4, "Speaker with cover"),
    "rods": (5, "Rod sections (4)"),
    "couplers": (6, "Couplers with snap buttons and pins (4)"),
    "tailcap": (7, "Tail cap with air barb and grommets"),
    "grip": (8, "Grip"),
    "cable": (9, "Camera and speaker cable"),
    "guide": (10, "Water guide tube"),
    "waterset": (11, "Water set (single use)"),
    "bottle": (12, "Water reservoir bottle"),
    "stand": (13, "Reservoir stand"),
    "case": (14, "Surface unit case"),
    "eplate": (15, "Equipment plate with spacers"),
    "display": (16, "Monitor with recorder and lid bracket"),
    "battery": (17, "Battery pack, LiFePO4"),
    "blower": (18, "Blower"),
    "filter": (19, "Intake filter"),
    "flowmeter": (20, "Air flow meter"),
    "modules": (21, "Control modules"),
    "fittings": (23, "Wall fittings"),
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought" or "fixing"
    group: str | None  # key in BOM (build_parts groups components by it)


# ------------------------------------------------------------------ helpers
def _b3d():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(x0, x1, r, y=0.0, z=0.0):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, x1 - x0)


def xtube(x0, x1, ro, ri, y=0.0, z=0.0):
    return xcyl(x0, x1, ro, y, z) - xcyl(x0 - 1, x1 + 1, ri, y, z)


def zcyl(x, y, z0, z1, r):
    b = _b3d()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def radial(x, ang, r0, r1, rad, zc=0.0):
    """Cylinder of radius rad on a radial axis at angle ang (deg from +Y toward +Z), from r0 to r1."""
    b = _b3d()
    a = math.radians(ang)
    d = b.Vector(0, math.cos(a), math.sin(a))
    c = b.Vector(x, 0, zc) + d * ((r0 + r1) / 2)
    return b.Solid.make_cylinder(rad, r1 - r0, b.Plane(origin=c - d * ((r1 - r0) / 2), z_dir=d))


def rod_between(p0, p1, r):
    """Cylinder of radius r from point p0 to p1."""
    b = _b3d()
    p0, p1 = b.Vector(*p0), b.Vector(*p1)
    d = p1 - p0
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=p0, z_dir=d.normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ derived dimensions
def derived(p=PARAMS):
    """Dimensions the calc note, drawings and build plan quote, computed from PARAMS."""
    od, wall, L = p["rod"]
    n = p["n_sec"]
    fl = p["tailcap"][1]
    sec = [(fl + i * L, fl + (i + 1) * L) for i in range(n)]       # back to front: section 4, 3, 2, 1
    x_collar = sec[-1][1]
    cl = p["collar"][1]
    x_nose = x_collar + cl
    nose_len = p["nose"][0]
    x_tip = x_nose + nose_len
    gstart = p["grip"][2]
    gend = gstart + p["grip"][1]
    cod, cw, clen, cbond = p["coupler"]
    return {
        "rod_id": od - 2 * wall, "coupler_id": cod - 2 * cw, "fit_coupler": (od - 2 * wall - cod) / 2,
        "sections": sec, "x_collar": x_collar, "x_nose": x_nose, "x_tip": x_tip,
        "x_spigot_end": x_nose + p["spigot"][1], "length": x_tip, "grip_end": gend,
        "working_length": x_tip - gend, "head_len": x_tip - x_collar,
        "max_od": max(p["collar"][0], p["grip"][0], od + 2 * p["button"][2]),
        "cam_x0": x_nose + p["spigot"][1] + p["cam_ring"], "cam_x1": x_nose + p["spigot"][1] + p["cam_ring"] + p["camera"][1],
        "plenum": (x_collar + p["collar"][2], x_collar + cl),
        "case_x": (p["case_at"][0], p["case_at"][0] + p["case"][0]),
        "case_y": (p["case_at"][1], p["case_at"][1] + p["case"][1]),
        "plate_z": p["case"][4] + p["espacer"] + p["eplate"][2],
    }


# ------------------------------------------------------------------ components
def _section(i, p, D):
    """Rod section tube. i = 0 is section 4 (at the back), i = n - 1 is section 1 (at the front)."""
    od, wall, L = p["rod"]
    x0, x1 = D["sections"][i]
    zc = p["z_axis"]
    t = xtube(x0, x1, od / 2, od / 2 - wall, 0, zc)
    hole = p["button_hole"] / 2
    bd = p["button"][1]
    pd, px = p["pin"]
    if i > 0:            # back end receives the next section's coupler: button hole on +Y
        t = t - radial(x0 + bd, 0.0, 0, od / 2 + 2, hole, zc)
    else:                # section 4: tail cap pins at +/-Z
        for a in (90.0, 270.0):
            t = t - radial(x0 + p["tc_pin_x"], a, 0, od / 2 + 2, pd / 2, zc)
    for a in (90.0, 270.0):  # coupler pins at the front end
        t = t - radial(x1 - px, a, 0, od / 2 + 2, pd / 2, zc)
    return t


def _coupler(i, p, D):
    cod, cw, clen, cbond = p["coupler"]
    x1 = D["sections"][i][1]
    zc = p["z_axis"]
    c = xtube(x1 - cbond, x1 - cbond + clen, cod / 2, cod / 2 - cw, 0, zc)
    free = x1 - cbond + clen
    c = c - radial(free - p["button"][1], 0.0, 0, cod / 2 + 2, p["button_hole"] / 2, zc)
    for a in (90.0, 270.0):
        c = c - radial(x1 - p["pin"][1], a, 0, cod / 2 + 2, p["pin"][0] / 2, zc)
    return c


def _button(i, p, D):
    """Snap button head and its V-spring envelope inside the coupler of section i."""
    b = _b3d()
    cod, cw, clen, cbond = p["coupler"]
    od = p["rod"][0]
    x1 = D["sections"][i][1]
    zc = p["z_axis"]
    xb = x1 - cbond + clen - p["button"][1]
    ri = cod / 2 - cw
    btn = radial(xb, 0.0, ri - 1.2, od / 2 + p["button"][2], p["button"][0] / 2, zc)
    sw, sl = p["spring"]
    env = bx(xb - sl, xb + 3, -ri, ri - 1.2, zc - sw / 2, zc + sw / 2) & xcyl(xb - sl - 1, xb + 4, ri - 0.05, 0, zc)
    return btn, env


def _pins(i, p, D):
    od, wall, _ = p["rod"]
    cod, cw = p["coupler"][:2]
    x1 = D["sections"][i][1]
    zc = p["z_axis"]
    return fuse(radial(x1 - p["pin"][1], a, cod / 2 - cw, od / 2, p["pin"][0] / 2, zc) for a in (90.0, 270.0))


def _tailcap(p, D):
    fod, fl, pod, pl, bore, wall_t = p["tailcap"]
    zc = p["z_axis"]
    t = xcyl(0, fl, fod / 2, 0, zc) + xcyl(fl, fl + pl, pod / 2, 0, zc)
    t = t - xcyl(wall_t, fl + pl + 1, bore / 2, 0, zc)
    for k, (zg, dg) in p["grommets"].items():
        t = t - xcyl(-1, wall_t + 1, dg / 2, 0, zc + zg)
    thr, hexaf, bod, blen, bxp = p["barb"]
    t = t - radial(bxp, 180.0, bore / 2 - 1, fod / 2 + 1, thr / 2, zc)
    for a in (90.0, 270.0):
        t = t - radial(fl + p["tc_pin_x"], a, 0, fod / 2 + 2, p["pin"][0] / 2, zc)
    return t


def _barb(p):
    b = _b3d()
    fod, fl, pod, pl, bore, wall_t = p["tailcap"]
    thr, hexaf, bod, blen, bxp = p["barb"]
    zc = p["z_axis"]
    r0 = bore / 2
    th = radial(bxp, 180.0, r0, fod / 2, thr / 2, zc)
    hx = b.Pos(bxp, -(fod / 2 + 4), zc) * b.Rot(90, 0, 0) * b.Pos(0, 0, -4) * b.extrude(b.RegularPolygon(hexaf / math.sqrt(3), 6), 8)
    br = radial(bxp, 180.0, fod / 2 + 8, fod / 2 + 8 + blen, bod / 2, zc)
    return th + hx + br


def _tc_grommets(p):
    zc = p["z_axis"]
    wall_t = p["tailcap"][5]
    out = []
    for k, (zg, dg) in p["grommets"].items():
        line_od = p["cable"][1] if k == "cable" else p["guide"][1]
        out.append(xtube(0, wall_t, dg / 2, line_od / 2, 0, zc + zg))
    return fuse(out)


def _collar(p, D):
    b = _b3d()
    od, cl, sock, plen = p["collar"]
    x0 = D["x_collar"]
    zc = p["z_axis"]
    rid = D["rod_id"]
    so, sl = p["spigot"]
    sbd, sbz = p["spigot_bore"]
    c = xcyl(x0, x0 + cl, od / 2, 0, zc) + xcyl(x0 + cl, x0 + cl + sl, so / 2, 0, zc)
    c = c - xcyl(x0 - 1, x0 + sock, rid / 2, 0, zc)                 # socket
    c = c - xcyl(x0 + sock - 0.01, x0 + cl - 4, plen / 2, 0, zc)     # plenum (4 mm front wall)
    c = c - xcyl(x0 + cl - 5, x0 + cl + sl + 1, sbd / 2, 0, zc + sbz)  # spigot bore for the cable grommet
    # button hole and spotface on +Y
    c = c - radial(x0 + p["button"][1], 0.0, 0, od / 2 + 1, p["button_hole"] / 2, zc)
    sfd, sfdep = p["spotface"]
    c = c - radial(x0 + p["button"][1], 0.0, od / 2 - sfdep, od / 2 + 5, sfd / 2, zc)
    # air outlets
    hd, hx, angs = p["outlets"]
    for a in angs:
        c = c - radial(x0 + hx, a, plen / 2 - 1, od / 2 + 1, hd / 2, zc)
    # speaker pocket on -Y: flat floor at |y| = spk_floor
    sp = p["spk_pocket"]
    c = c - (b.Pos(x0 + p["spk_x"], -(p["spk_floor"] + 10), zc) * b.Rot(90, 0, 0) * b.Cylinder(sp / 2, 20))
    c = c - radial(x0 + p["spk_x"], 180.0, plen / 2 - 1, p["spk_floor"] + 1, 1.5, zc)   # wire hole
    # water exit at 45 deg and the top groove
    wd, wx = p["wexit"]
    gw, gz = p["groove"]
    c = c - rod_between((x0 + wx - 12, 0, zc), (x0 + wx + 20, 0, zc + 32), wd / 2)
    c = c - bx(x0 + wx + 7.5 - 4, x0 + cl + 1, -gw / 2, gw / 2, zc + gz, zc + od)
    # tapped holes for the nose screws in the spigot
    nsx, nangs = p["nose_screws"]
    for a in nangs:
        c = c - radial(D["x_nose"] + nsx, a, so / 2 - 6, so / 2 + 1, 1.65, zc)
    return c


def _nose(p, D):
    L, cb, camd, camz, lipd, lipl = p["nose"]
    od = p["collar"][0]
    x0 = D["x_nose"]
    zc = p["z_axis"]
    sl = p["spigot"][1]
    n = xcyl(x0, x0 + L, od / 2, 0, zc)
    n = n - xcyl(x0 - 1, x0 + sl, cb / 2, 0, zc)
    n = n - xcyl(x0 + sl - 0.01, x0 + L - lipl, camd / 2, 0, zc + camz)
    n = n - xcyl(x0 + L - lipl - 1, x0 + L + 1, lipd / 2, 0, zc + camz)
    pw, pz, plen = p["pocket"]
    n = n - bx(x0 + L - plen, x0 + L + 1, -pw / 2, pw / 2, zc + pz, zc + od)
    gw, gz = p["groove"]
    n = n - bx(x0 - 1, x0 + L - plen + 1, -gw / 2, gw / 2, zc + gz, zc + od)
    nsx, nangs = p["nose_screws"]
    for a in nangs:
        n = n - radial(x0 + nsx, a, cb / 2 - 1, od / 2 + 1, 2.25, zc)
    return n


def _nose_screws(p, D):
    nsx, nangs = p["nose_screws"]
    so = p["spigot"][0]
    od = p["collar"][0]
    zc = p["z_axis"]
    return fuse(radial(D["x_nose"] + nsx, a, so / 2 - 6, od / 2 - 0.3, 1.65, zc) for a in nangs)


def _camera(p, D):
    cd, cl = p["camera"]
    zc = p["z_axis"] + p["nose"][3]
    return xcyl(D["cam_x0"], D["cam_x1"], cd / 2, 0, zc)


def _cam_ring(p, D):
    cd = p["camera"][0]
    zc = p["z_axis"] + p["nose"][3]
    return xtube(D["x_spigot_end"], D["cam_x0"], cd / 2, p["cable"][1] / 2, 0, zc)


def _spigot_grommet(p, D):
    sbd, sbz = p["spigot_bore"]
    zc = p["z_axis"]
    x1 = D["x_spigot_end"]
    return xtube(x1 - 8, x1, sbd / 2, p["cable"][1] / 2, 0, zc + sbz)


def _speaker(p, D):
    b = _b3d()
    d, t, ct = p["speaker"]
    zc = p["z_axis"]
    x = D["x_collar"] + p["spk_x"]
    y0 = -p["spk_floor"]
    spk = b.Pos(x, y0 - t / 2, zc) * b.Rot(90, 0, 0) * b.Cylinder(d / 2, t)
    cov = b.Pos(x, y0 - t - ct / 2, zc) * b.Rot(90, 0, 0) * b.Cylinder(d / 2, ct)
    return spk, cov


def _lines(p, D):
    """Cable, guide tube and water tube from the stub behind the tail cap into the head."""
    zc = p["z_axis"]
    x_end = D["plenum"][0] + 6          # guide and cable leave the coupler 6 mm into the plenum
    st = -p["stub"]
    cz, cd = p["cable"]
    gz, god, gid = p["guide"]
    wod, wid = p["wtube"]
    camz = zc + p["nose"][3]
    # cable: straight, then a short slant to the camera axis, then through the spigot grommet to the camera
    xa = x_end + 9
    cable = fuse([xcyl(st, x_end, cd / 2, 0, zc + cz),
                  rod_between((x_end, 0, zc + cz), (xa, 0, camz), cd / 2),
                  _b3d().Pos(x_end, 0, zc + cz) * _b3d().Sphere(cd / 2),
                  _b3d().Pos(xa, 0, camz) * _b3d().Sphere(cd / 2),
                  xcyl(xa, D["cam_x0"], cd / 2, 0, camz)])
    guide = xtube(st, x_end, god / 2, gid / 2, 0, zc + gz)
    # water tube: inside the guide, then up the 45 degree exit, along the groove and into the bite valve
    wd, wx = p["wexit"]
    x0c = D["x_collar"]
    gw, gfz = p["groove"]
    zt = gfz + wod / 2                      # tube centre in the groove
    xe0 = x0c + wx + (gz - 12.0)            # where the exit axis crosses the guide line (z = gz)
    xe1 = x0c + wx + (zt - 12.0)            # where it reaches the groove line
    xb = D["x_tip"] - p["bite"][1] - 2.0
    zb = p["pocket"][1] + p["bite"][0] / 2
    b = _b3d()
    w = fuse([xcyl(st, xe0, wod / 2, 0, zc + gz),
              rod_between((xe0, 0, zc + gz), (xe1, 0, zc + zt), wod / 2),
              b.Pos(xe0, 0, zc + gz) * b.Sphere(wod / 2), b.Pos(xe1, 0, zc + zt) * b.Sphere(wod / 2),
              xcyl(xe1, xb - 6, wod / 2, 0, zc + zt),
              rod_between((xb - 6, 0, zc + zt), (xb + 1, 0, zc + zb), wod / 2),
              b.Pos(xb - 6, 0, zc + zt) * b.Sphere(wod / 2)])
    w = w - xcyl(st - 1, xe0 - 0.5, wid / 2, 0, zc + gz)
    bite = xcyl(xb, xb + p["bite"][1], p["bite"][0] / 2, 0, zc + zb)
    return cable, guide, w, bite


# ------------------------------------------------------------------ surface unit
def _case(p, D):
    b = _b3d()
    L, W, hb, hl, t = p["case"]
    x0, y0 = p["case_at"]
    base = bx(x0, x0 + L, y0, y0 + W, 0, hb) - bx(x0 + t, x0 + L - t, y0 + t, y0 + W - t, t, hb + 1)
    for k, (fx, fz) in p["fittings"].items():
        dia = {"camera": 16.0, "air": 12.5, "headset": 12.0}[k]
        base = base - b.Pos(x0 + fx, y0 + W - t / 2, fz) * b.Rot(90, 0, 0) * b.Cylinder(dia / 2, t + 2)
    fd, flen, fx, fz = p["filter"]
    base = base - b.Pos(x0 + fx, y0 + t / 2, fz) * b.Rot(90, 0, 0) * b.Cylinder(10.5, t + 2)
    lid = bx(x0, x0 + L, y0, y0 + W, hb, hb + hl) - bx(x0 + t, x0 + L - t, y0 + t, y0 + W - t, hb - 1, hb + hl - t)
    lid = _lid_pose(lid, p)
    return base, lid


def _lid_pose(shape, p):
    b = _b3d()
    L, W, hb, hl, t = p["case"]
    x0, y0 = p["case_at"]
    hx, hz = x0 + L, hb
    return b.Pos(hx, 0, hz) * b.Rot(0, p["lid_open"], 0) * b.Pos(-hx, 0, -hz) * shape


def _eplate(p, D):
    L, W, t = p["eplate"]
    cx0, cy0 = p["case_at"]
    ct = p["case"][4]
    ix, iy = p["eplate_in"]
    x0, y0 = cx0 + ct + ix, cy0 + ct + iy
    z0 = ct + p["espacer"]
    plate = bx(x0, x0 + L, y0, y0 + W, z0, z0 + t)
    sp = fuse(zcyl(x, y, ct, z0, 5.0) for x in (x0 + 15, x0 + L - 15) for y in (y0 + 15, y0 + W - 15))
    return plate, sp, (x0, y0, z0 + t)


def _on_plate(p, D, key):
    _, _, (px, py, pz) = _eplate(p, D)
    if key == "battery":
        L, W, H = p["battery"]; ax, ay = p["bat_at"]
        return bx(px + ax, px + ax + L, py + ay, py + ay + W, pz, pz + H)
    if key == "blower":
        L, W, H = p["blower"]; ax, ay = p["blower_at"]; o = p["blower_off"]
        body = bx(px + ax, px + ax + L, py + ay, py + ay + W, pz + o, pz + o + H)
        legs = fuse(zcyl(px + ax + dx, py + ay + dy, pz, pz + o, 4.0) for dx in (8, L - 8) for dy in (8, W - 8))
        inlet = zcyl(px + ax + L * 0.45, py + ay + W * 0.5, pz + o + H, pz + o + H + 6, 18.0)
        return body + inlet, legs
    if key == "modules":
        L, W, H = p["modules"]; ax, ay = p["mod_at"]
        tray = bx(px + ax, px + ax + L, py + ay, py + ay + W, pz, pz + H)
        sw = zcyl(px + ax + 25, py + ay + 35, pz + H, pz + H + 12, 6.0)
        knob = zcyl(px + ax + 70, py + ay + 35, pz + H, pz + H + 15, 9.0)
        return tray + sw + knob
    if key == "flowmeter":
        W_, Dd, H = p["flowmeter"]; ax, ay = p["fm_at"]; leg, t = p["fm_angle"]
        x0, y0 = px + ax, py + ay
        ang = bx(x0, x0 + leg, y0, y0 + Dd, pz, pz + t) + bx(x0 + leg - t, x0 + leg, y0, y0 + Dd, pz, pz + H - 5)
        body = bx(x0 + leg, x0 + leg + W_, y0, y0 + Dd, pz + 2, pz + 2 + H - 8)
        return body, ang
    raise KeyError(key)


def _fittings(p, D):
    b = _b3d()
    L, W, hb, hl, t = p["case"]
    x0, y0 = p["case_at"]
    yw = y0 + W
    out = []
    for k, (fx, fz) in p["fittings"].items():
        d = {"camera": 16.0, "air": 12.5, "headset": 12.0}[k]
        body = b.Pos(x0 + fx, yw - t / 2, fz) * b.Rot(90, 0, 0) * b.Cylinder(d / 2, t)
        flange = b.Pos(x0 + fx, yw + 1.5, fz) * b.Rot(90, 0, 0) * b.Cylinder(d / 2 + 5, 3)
        nut = b.Pos(x0 + fx, yw - t - 2.5, fz) * b.Rot(90, 0, 0) * b.Cylinder(d / 2 + 4, 5)
        ext = (b.Pos(x0 + fx, yw + 3 + 9, fz) * b.Rot(90, 0, 0) * b.Cylinder(6.0 if k == "air" else d / 2 - 1, 18))
        out.append(body + flange + nut + ext)
    return fuse(out)


def _filter(p, D):
    b = _b3d()
    fd, flen, fx, fz = p["filter"]
    x0, y0 = p["case_at"]
    t = p["case"][4]
    thread = b.Pos(x0 + fx, y0 + t / 2, fz) * b.Rot(90, 0, 0) * b.Cylinder(10.5, t)
    nut = b.Pos(x0 + fx, y0 + t + 3, fz) * b.Rot(90, 0, 0) * b.Cylinder(15, 6)
    body = b.Pos(x0 + fx, y0 - flen / 2, fz) * b.Rot(90, 0, 0) * b.Cylinder(fd / 2, flen)
    return body + thread + nut


def _display(p, D):
    """Monitor on its bracket in the lid. Built with the lid closed, then posed with it."""
    L, W, hb, hl, t = p["case"]
    x0, y0 = p["case_at"]
    mw, mh, md = p["monitor"]
    bt, so, foot = p["dbracket"]
    zf = hb + hl - t                    # lid inner floor (lid closed), facing down
    cx, cy = x0 + L / 2, y0 + W / 2
    # monitor face points down (toward the case contents when closed, toward the operator when open)
    # long side of the monitor along Y; its height along X
    pl = bx(cx - mh / 2 - 10, cx + mh / 2 + 10, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf - so)
    feet = fuse([bx(cx - mh / 2 - 10, cx - mh / 2 - 10 + bt, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf),
                 bx(cx + mh / 2 + 10 - bt, cx + mh / 2 + 10, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf),
                 bx(cx - mh / 2 - 10 - foot, cx - mh / 2 - 10 + bt, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - bt, zf),
                 bx(cx + mh / 2 + 10 - bt, cx + mh / 2 + 10 + foot, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - bt, zf)])
    mon = bx(cx - mh / 2, cx + mh / 2, cy - mw / 2, cy + mw / 2, zf - so - bt - md, zf - so - bt)
    return _lid_pose(mon, p), _lid_pose(pl + feet, p)


def _stand(p):
    b = _b3d()
    sx, sy, hub, top, spread, pd = p["stand"]
    pole = zcyl(sx, sy, 80, top, pd / 2) + zcyl(sx, sy, hub - 40, hub + 40, pd / 2 + 6)
    legs = []
    for k in range(3):
        a = math.radians(90 + 120 * k)
        foot = (sx + spread * math.cos(a), sy + spread * math.sin(a), 8)
        legs.append(rod_between((sx, sy, hub), foot, 8))
        legs.append(b.Pos(*foot) * b.Sphere(10))
    arm = rod_between((sx, sy, top - 20), (sx + 70, sy, top - 20), 5) + rod_between((sx + 70, sy, top - 20), (sx + 70, sy, top - 50), 4)
    return pole + fuse(legs) + arm


def _bottle(p):
    sx, sy = p["stand"][:2]
    bd, bh, bz = p["bottle"]
    x = sx + 70
    body = zcyl(x, sy, bz, bz + bh, bd / 2) + zcyl(x, sy, bz + bh, bz + bh + 20, 18)
    spig = zcyl(x, sy, bz - 25, bz, 5)
    loop = rod_between((x, sy, bz + bh + 20), (x, sy, p["stand"][3] - 50), 3)
    return body + spig + loop


# ------------------------------------------------------------------ assembly
def build_components(p=PARAMS):
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    n = p["n_sec"]
    for i in range(n):
        k = n - i      # section number counted from the head: section 1 is at the front
        add(f"rod{k}", f"Rod section {k}", _section(i, p, D), 5, "made", "rods")
        add(f"coupler{k}", f"Coupler {k}", _coupler(i, p, D), 6, "made", "couplers")
        btn, spr = _button(i, p, D)
        add(f"button{k}", f"Snap button {k}", btn, 6, "bought", "couplers")
        add(f"spring{k}", f"Snap button spring {k}", spr, 6, "bought", "couplers")
        add(f"pins{k}", f"Coupler pins {k}", _pins(i, p, D), 6, "fixing", "couplers")
    add("tailcap", "Tail cap", _tailcap(p, D), 7, "made", "tailcap")
    add("barb", "Air inlet barb", _barb(p), 7, "bought", "tailcap")
    add("tc_grommets", "Tail cap grommets", _tc_grommets(p), 7, "bought", "tailcap")
    od = p["rod"][0]
    zc = p["z_axis"]
    add("tc_pins", "Tail cap pins", fuse(radial(p["tailcap"][1] + p["tc_pin_x"], a, p["tailcap"][2] / 2 - 2.0, od / 2, p["pin"][0] / 2, zc)
                                         for a in (90.0, 270.0)), 7, "fixing", "tailcap")
    gd, gl, gs = p["grip"]
    add("grip", "Grip", xtube(gs, gs + gl, gd / 2, od / 2, 0, zc), 8, "bought", "grip")
    cable, guide, wt, bite = _lines(p, D)
    add("cable", "Camera and speaker cable", cable, 9, "bought", "cable")
    add("guide", "Water guide tube", guide, 10, "bought", "guide")
    add("wtube", "Water tube", wt, 11, "bought", "waterset")
    add("bite", "Bite valve", bite, 11, "bought", "waterset")
    add("collar", "Collar", _collar(p, D), 3, "made", "collar")
    add("nose", "Nose", _nose(p, D), 2, "made", "nose")
    add("nose_screws", "Nose screws (3)", _nose_screws(p, D), 2, "fixing", "nose")
    add("camera", "Camera head", _camera(p, D), 1, "bought", "camera")
    add("cam_ring", "Camera spacer ring", _cam_ring(p, D), 1, "bought", "camera")
    add("spg_grommet", "Spigot grommet", _spigot_grommet(p, D), 3, "bought", "collar")
    spk, cov = _speaker(p, D)
    add("speaker", "Speaker", spk, 4, "bought", "speaker")
    add("spk_cover", "Speaker cover", cov, 4, "made", "speaker")
    # surface unit
    base, lid = _case(p, D)
    add("case", "Case base, drilled", base, 14, "bought", "case")
    add("lid", "Case lid", lid, 14, "bought", "case")
    plate, sp, _ = _eplate(p, D)
    add("eplate", "Equipment plate", plate, 15, "made", "eplate")
    add("espacers", "Plate spacers and screws", sp, 15, "fixing", "eplate")
    add("battery", "Battery pack", _on_plate(p, D, "battery"), 17, "bought", "battery")
    bl, legs = _on_plate(p, D, "blower")
    add("blower", "Blower", bl, 18, "bought", "blower")
    add("blower_legs", "Blower standoffs", legs, 18, "fixing", "blower")
    add("modules", "Control modules", _on_plate(p, D, "modules"), 21, "bought", "modules")
    fm, fmb = _on_plate(p, D, "flowmeter")
    add("flowmeter", "Flow meter", fm, 20, "bought", "flowmeter")
    add("fm_bracket", "Flow meter bracket", fmb, 20, "made", "flowmeter")
    add("fittings", "Wall fittings", _fittings(p, D), 23, "bought", "fittings")
    add("filter", "Intake filter", _filter(p, D), 19, "bought", "filter")
    mon, dbr = _display(p, D)
    add("monitor", "Monitor with recorder", mon, 16, "bought", "display")
    add("dbracket", "Monitor bracket", dbr, 16, "made", "display")
    add("stand", "Reservoir stand", _stand(p), 13, "bought", "stand")
    add("bottle", "Water reservoir bottle", _bottle(p), 12, "bought", "bottle")
    return C


PROBE_KEYS = None  # filled by probe_keys()


def probe_keys(C):
    surf = {"case", "lid", "eplate", "espacers", "battery", "blower", "blower_legs", "modules", "flowmeter",
            "fm_bracket", "fittings", "filter", "monitor", "dbracket", "stand", "bottle"}
    return [k for k in C if k not in surf]


HEAD_KEYS = ["collar", "nose", "nose_screws", "camera", "cam_ring", "spg_grommet", "speaker", "spk_cover", "bite"]
SURFACE_KEYS = ["case", "lid", "eplate", "espacers", "battery", "blower", "blower_legs", "modules", "flowmeter",
                "fm_bracket", "fittings", "filter", "monitor", "dbracket"]


def build_parts(p=PARAMS, C=None):
    """Return [(name, shape, colour, BOM line, explode offset)] by BOM line, for the concept media."""
    C = C or build_components(p)
    groups = {}
    for c in C.values():
        if c.group:
            groups.setdefault(c.group, []).append(c.shape)
    col = {"camera": "#1F2937", "nose": "#9CA3AF", "collar": "#6B7280", "speaker": "#374151", "rods": "#D1D5DB",
           "couplers": "#0F766E", "tailcap": "#4B5563", "grip": "#111827", "cable": "#B45309", "guide": "#E5E7EB",
           "waterset": "#2563EB", "bottle": "#93C5FD", "stand": "#374151", "case": "#F59E0B", "eplate": "#A8A29E",
           "display": "#1E293B", "battery": "#C2410C", "blower": "#334155", "filter": "#E5E7EB", "flowmeter": "#0EA5E9",
           "modules": "#16A34A", "fittings": "#111827"}
    ex = {"camera": (260, 0, 120), "nose": (220, 0, 60), "collar": (120, 0, 60), "speaker": (120, -160, 60),
          "rods": (0, 0, 220), "couplers": (0, 0, 120), "tailcap": (-260, 0, 60), "grip": (0, 0, 320),
          "cable": (0, 0, -120), "guide": (0, 0, -200), "waterset": (360, 0, 200), "bottle": (200, 0, 300),
          "stand": (300, 0, 0), "case": (0, 0, 0), "eplate": (0, 0, 220), "display": (0, 0, 520), "battery": (0, 0, 380),
          "blower": (0, 0, 420), "filter": (0, -200, 0), "flowmeter": (160, 0, 400), "modules": (0, 0, 460),
          "fittings": (0, 180, 0)}
    out = []
    for key, (line, name) in sorted(BOM.items(), key=lambda kv: kv[1][0]):
        if key in groups:
            out.append((f"{line} {name}", fuse(groups[key]), col[key], line, ex[key]))
    return out


def assembly(p=PARAMS, keys=None, C=None):
    b = _b3d()
    C = C or build_components(p)
    ks = keys or list(C)
    return b.Compound([C[k].shape for k in ks])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS, C=None):
    """Pairs that must touch, fit with a small clearance or stay apart. Returns
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = C or build_components(p)
    D = derived(p)
    b = _b3d()
    S = lambda *ks: C[ks[0]].shape if len(ks) == 1 else b.Compound([C[k].shape for k in ks])  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        """expect: 'touch' (gap under 0.05), ('fit', g) (no overlap, gap at most g) or a minimum clearance."""
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        if expect == "touch":
            ok = v < 1e-3 and gp < 0.05
        elif isinstance(expect, tuple):
            ok = v < 1e-3 and gp <= expect[1] + 1e-6
        else:
            ok = v < 1e-3 and gp >= expect - 1e-6
        rows.append((desc, v, gp, expect, ok))

    n = p["n_sec"]
    for k in range(1, n + 1):
        chk(f"Coupler {k} bonded in rod section {k}", S(f"coupler{k}"), S(f"rod{k}"), ("fit", 0.2))
        chk(f"Pins {k} through section {k} and coupler {k}", S(f"pins{k}"), S(f"rod{k}", f"coupler{k}"), "touch")
        rk = f"rod{k - 1}" if k > 1 else "collar"
        recv = S(rk)
        rname = f"rod section {k - 1}" if k > 1 else "the collar socket"
        chk(f"Coupler {k} slides into {rname}", S(f"coupler{k}"), recv, ("fit", 0.2))
        chk(f"Section {k} front end butts {rname}", S(f"rod{k}"), recv, "touch")
        chk(f"Snap button {k} through its holes, clear", S(f"button{k}"), S(f"coupler{k}", rk), ("fit", 0.3))
        chk(f"Snap button spring {k} inside coupler {k}", S(f"spring{k}"), S(f"coupler{k}"), ("fit", 0.1))
        chk(f"Cable clear of snap button spring {k}", S("cable"), S(f"spring{k}"), 2.0)
        chk(f"Guide tube clear of snap button spring {k}", S("guide"), S(f"spring{k}"), 1.5)
        chk(f"Cable and guide clear of pins {k}", S("cable", "guide"), S(f"pins{k}"), 1.0)
        chk(f"Cable and guide clear of coupler {k} bore", S("cable", "guide"), S(f"coupler{k}"), 0.3)
    chk("Tail cap plug bonded in section 4", S("tailcap"), S("rod4"), ("fit", 0.1))
    chk("Tail cap flange butts section 4", S("tailcap"), S("rod4"), "touch")
    chk("Tail cap pins through section 4 and the plug", S("tc_pins"), S("rod4", "tailcap"), "touch")
    chk("Air barb in the tail cap flange", S("barb"), S("tailcap"), "touch")
    chk("Grommets in the tail cap end wall", S("tc_grommets"), S("tailcap"), "touch")
    chk("Cable and guide through the grommets", S("cable", "guide"), S("tc_grommets"), "touch")
    chk("Cable and guide clear of the tail cap bore", S("cable", "guide"), S("tailcap"), 0.5)
    chk("Grip on section 4", S("grip"), S("rod4"), "touch")
    chk("Grip clear of the air barb", S("grip"), S("barb"), 3.0)
    chk("Cable clear of the guide tube", S("cable"), S("guide"), 5.0)
    chk("Water tube inside the guide tube", S("wtube"), S("guide"), ("fit", 1.1))
    chk("Water tube through the 45 degree exit and groove, clear of the collar", S("wtube"), S("collar"), ("fit", 0.3))
    chk("Water tube clear of the nose groove sides", S("wtube"), S("nose"), ("fit", 0.3))
    chk("Water tube clear of the camera cable", S("wtube"), S("cable"), 3.0)
    chk("Bite valve in the nose pocket", S("bite"), S("nose"), ("fit", 0.3))
    chk("Nose on the collar spigot and shoulder", S("nose"), S("collar"), "touch")
    chk("Nose screws into the spigot", S("nose_screws"), S("collar"), "touch")
    chk("Camera head in the nose bore, against the lip", S("camera"), S("nose"), "touch")
    chk("Spacer ring between camera and spigot", S("cam_ring"), S("camera", "collar"), "touch")
    chk("Spigot grommet in the spigot bore", S("spg_grommet"), S("collar"), "touch")
    chk("Cable through the spigot grommet and spacer ring", S("cable"), S("spg_grommet", "cam_ring"), "touch")
    chk("Cable clear of the collar plenum and spigot", S("cable"), S("collar"), 1.0)
    chk("Cable meets the camera", S("cable"), S("camera"), "touch")
    chk("Speaker on the pocket floor", S("speaker"), S("collar"), ("fit", 0.3))
    chk("Speaker cover on the speaker", S("spk_cover"), S("speaker"), "touch")
    chk("Speaker clear of the outlets and water exit (cover)", S("spk_cover"), S("collar"), ("fit", 0.3))
    # head inside the 50 mm envelope (R1): nothing outside a 50 mm cylinder
    outside = xcyl(D["x_collar"] - 1, D["x_tip"] + 1, 60, 0, p["z_axis"]) - xcyl(D["x_collar"] - 2, D["x_tip"] + 2, 24.0 + 0.01, 0, p["z_axis"])
    for k in HEAD_KEYS + ["wtube"]:
        v = _vol(C[k].shape, outside)
        rows.append((f"{C[k].name} inside the 48 mm head outline", v, 0.0, "inside", v < 1e-3))
    # surface unit
    chk("Plate spacers on the case floor", S("espacers"), S("case"), "touch")
    chk("Equipment plate on its spacers", S("eplate"), S("espacers"), "touch")
    chk("Equipment plate clear of the case walls", S("eplate"), S("case"), 5.0)
    for k in ("battery", "modules", "fm_bracket", "blower_legs"):
        chk(f"{C[k].name} on the equipment plate", S(k), S("eplate"), "touch")
    chk("Blower on its standoffs", S("blower"), S("blower_legs"), "touch")
    chk("Flow meter on its bracket", S("flowmeter"), S("fm_bracket"), "touch")
    pairs = [("battery", "blower", 3.0), ("battery", "modules", 3.0), ("blower", "modules", 3.0), ("blower", "flowmeter", 5.0),
             ("modules", "flowmeter", 5.0), ("battery", "case", 3.0), ("blower", "case", 3.0), ("flowmeter", "case", 3.0),
             ("modules", "case", 3.0), ("fittings", "flowmeter", 5.0), ("fittings", "modules", 5.0), ("fittings", "battery", 5.0)]
    for a, b_, g in pairs:
        chk(f"{C[a].name} clear of {C[b_].name.lower()}", S(a), S(b_), g)
    chk("Wall fittings through the +Y wall", S("fittings"), S("case"), "touch")
    chk("Intake filter through the -Y wall", S("filter"), S("case"), "touch")
    chk("Monitor bracket on the lid", S("dbracket"), S("lid"), "touch")
    chk("Monitor on its bracket", S("monitor"), S("dbracket"), "touch")
    chk("Monitor clear of the lid walls", S("monitor"), S("lid"), 3.0)
    chk("Probe clear of the surface unit and stand", S(*probe_keys(C)), S(*SURFACE_KEYS, "stand", "bottle"), 300.0)
    chk("Reservoir stand clear of the case", S("stand"), S("case", "lid"), 20.0)
    # lid closes: tallest part below the rim, monitor above the contents
    pz = derived(p)["plate_z"]
    tops = {k: C[k].shape.bounding_box().max.Z for k in ("battery", "modules", "flowmeter", "blower")}
    rim = p["case"][2]
    m = rim - max(tops.values())
    rows.append((f"Tallest part in the base {m:.1f} mm below the rim (lid closes)", 0.0, m, 3.0, m >= 3.0))
    L, W, hb, hl, t = p["case"]
    stack = p["dbracket"][1] + p["dbracket"][0] + p["monitor"][2]
    rows.append((f"Monitor and bracket {stack:.0f} mm deep in a {hl - t:.0f} mm lid recess", 0.0, hl - t - stack, 1.0, hl - t - stack >= 1.0))
    return rows


def print_checks(p=PARAMS, C=None):
    rows = checks(p, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else (f"fit <= {exp[1]:g} mm" if isinstance(exp, tuple) else (exp if isinstance(exp, str) else f">= {exp:g} mm"))
        print(f"  {'ok ' if ok else 'BAD'}  {desc:70s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    C = build_components()
    if "--check" in sys.argv:
        sys.exit(1 if print_checks(C=C) else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    pk = probe_keys(C)
    groups = {
        "voidscope-assembly": list(C),
        "voidscope-probe": pk,
        "voidscope-head": HEAD_KEYS,
        "voidscope-surface-unit": SURFACE_KEYS,
    }
    for name, ks in groups.items():
        c = Compound([C[k].shape for k in ks])
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"probe length {D['length']:.0f} mm, working length {D['working_length']:.0f} mm, largest diameter {D['max_od']:.1f} mm")
    print_checks(C=C)
