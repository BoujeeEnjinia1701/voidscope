"""Options B and C of VoidScope at detail level D3 (VDS-OPT-001). Repo-specific helpers for cad/src/model.py.

Both options share option A's surface unit (case, equipment plate, battery, blower, flow meter, modules, monitor,
fittings, filter, reservoir stand and bottle, with their fasteners): the shared parts are passed in as `shared`.
What differs is how the camera head reaches the survivor.

B  Reel-fed flexible push cable. A 10 mm glass-fibre push rod runs off a hand reel (two aluminium flanges on a hub
   tube, tied by four M8 bolts, turning on two bushes on an M20 axle bolt that is carried by one welded upright).
   The air hose, water tube and camera cable are held beside the rod by round PA12 clips every 650 mm. The head is a
   turned 48 mm aluminium body: rod socket, hose, cable and water ports, air plenum with six outlets, speaker,
   bite valve pocket and a camera bore, as in option A but without a steerable tip.
   Axes as model.py: tip toward +X, Z up, ground z = 0, the rod at the deployed height b_z_axis.

C  Tripod and winch lowered sonde. Three aluminium legs pinned to a head plate over a drilled hole; a hand winch
   (drum, axle, crank, ratchet and pawl) on the head plate pays a stainless wire rope straight down the hole; the
   same head hangs on it by an eye bolt, camera down. The lines hang clipped to the rope and leave the hole at the
   slab. The hole is at the origin and the slab top is z = 0 (parts below it need ground_z = 0 in OPTION_VIEWS).
"""
from __future__ import annotations

import math
import cad_parts as cp
from cad_parts import part, at, break_edges
from build123d import Box, Cone, Cylinder, Location, Plane, Pos, Rot, Sketch, Torus, Circle, RegularPolygon, extrude, Compound


# ------------------------------------------------------------------------------------------------ helpers
def xcyl(x0, x1, r, y=0.0, z=0.0):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def xtube(x0, x1, ro, ri, y=0.0, z=0.0):
    return xcyl(x0, x1, ro, y, z) - xcyl(x0 - 1, x1 + 1, ri, y, z)


def ycyl(y0, y1, r, x=0.0, z=0.0):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def radial(x, ang, r0, r1, rad, zc=0.0):
    """Cylinder of radius rad on a radial axis at angle ang (deg from +Y toward +Z), from r0 to r1, at x."""
    a = math.radians(ang)
    from build123d import Vector, Solid
    d = Vector(0, math.cos(a), math.sin(a))
    c = Vector(x, 0, zc) + d * ((r0 + r1) / 2)
    return Solid.make_cylinder(rad, r1 - r0, Plane(origin=c - d * ((r1 - r0) / 2), z_dir=d))


def along_dir(shape, p0, d):
    """Place a shape built along +Z from the origin so that it starts at p0 and points along d."""
    from build123d import Vector
    return Location(Plane(origin=Vector(*p0), z_dir=Vector(*d))) * shape


def bead(length, leg, x0, y, z, sy, sz):
    """A fillet weld bead along +X from x0, in the corner at (y, z), legs toward sy (+1 or -1) along Y and sz along Z."""
    b = cp.weld_fillet(length, leg)
    rot = {(1, 1): (0, 0, 0), (-1, 1): (0, 0, 180), (1, -1): (0, 180, 0), (-1, -1): (180, 0, 0)}[(sy, sz)]
    b = Rot(*rot) * b
    bb = b.bounding_box()
    return Pos(x0 - bb.min.X, y, z) * b


def _mk(out, name, shape, material, kind="made", bom=None, group="shell", note="", explode=(0, 0, 0)):
    if kind in ("made", "bought"):
        from cad_check import is_bare
        if is_bare(shape):
            try:
                bb = shape.bounding_box()
                shape = break_edges(shape, max(0.2, min(1.5, 0.12 * min(bb.size.X, bb.size.Y, bb.size.Z))))
            except Exception:
                pass
    out.append(part(name, shape, material, kind=kind, bom=bom, group=group, note=note, explode=explode))


def _bolt_y(out, d, grip, y_top, x, z, group, label, sign=1, kind="fastener"):
    """ISO bolt set along Y: joint face at y_top, clamping toward -Y (sign=1) or +Y (sign=-1)."""
    for name, shp in cp.hex_bolt_set(d, grip):
        rot = (-90, 0, 0) if sign == 1 else (90, 0, 0)
        out.append(part(f"{label}: {name}", at(shp, (x, y_top, z), rot), "stainless", kind=kind, group=group))


def _clip(out, name, x0, y, z, holes, od=44.0, t=15.0):
    """Round PA12 clip along X holding the rod or rope and the three lines: holes = [(dy, dz, dia), ...]."""
    s = xcyl(x0, x0 + t, od / 2, y, z)
    for dy, dz, d in holes:
        s = s - xcyl(x0 - 1, x0 + t + 1, d / 2, y + dy, z + dz)
    s = break_edges(s, 1.0)
    out.append(part(name, s, "hdpe_natural", kind="made", group="clips"))


# ------------------------------------------------------------------------------------------------ the head
def head_parts(p, rear):
    """The turned head, camera, speaker, bite valve and screws, built with the tip toward +X from x = 0 at the back
    face, axis on y = z = 0. rear = 'rod' (option B, 10.1 mm socket) or 'eye' (option C, M8 eye-bolt socket)."""
    out = []
    OD, LEN = 48.0, 150.0
    R = OD / 2
    cam_d, cam_len, cam_z = 29.0, 55.0, -6.5
    h = xcyl(0, LEN, R)
    # rear sockets and ports
    if rear == "rod":
        h = h - xcyl(-1, 24, 5.05)                      # 10 mm rod socket, 24 deep, bonded with epoxy
    else:
        h = h - xcyl(-1, 22, 4.0)                       # M8 tapped socket for the eye bolt (drawn at the thread major dia)
    h = h - xcyl(-1, 25, 6.1, 0, 13.0)                  # 12 mm air hose port, 25 deep, opens into the plenum
    h = h - xcyl(-1, 75, 3.1, 10.0, 0)                  # camera cable port through the plenum to the camera cavity
    h = h - xcyl(-1, 20, 2.05, -10.0, 0)                # 4 mm water tube port, 20 deep
    h = h - xcyl(25, 75, 15.0)                          # air plenum, 30 mm bore
    for a in (0.0, 45.0, 135.0, 240.0, 270.0, 300.0):   # six 5 mm air outlets
        h = h - radial(65.0, a, 10.0, R + 1, 2.5)
    h = h - xcyl(75 - 0.01, LEN + 1, 14.65, 0, cam_z)   # 29.3 mm camera bore from the front, 75 deep
    # bite valve pocket (11.5 wide, floor z = 12, 50 long) and the water tube groove (4.5 wide, floor z = 16)
    h = h - Pos(LEN - 25 + 0.5, 0, 12 + 7) * Box(51, 11.5, 14)
    h = h - Pos(55, 0, 16 + 4) * Box(112, 4.5, 8)
    # speaker pocket on -Y: floor at |y| = 16.8, 20.5 mm dia, with a 3 mm wire hole into the plenum
    h = h - ycyl(-R - 1, -16.8, 10.25, 45.0, 0)
    h = h - ycyl(-16.8 - 0.5, -14.0, 1.5, 45.0, 0)
    # grub screw holes: two M3 on the camera, two M4 on the rod/eye
    for a in (60.0, 120.0):
        h = h - radial(110.0, a, 14.5, R + 1, 1.5, cam_z)
    for a in (270.0, 235.0):
        h = h - radial(12.0, a, 5.0, R + 1, 2.0)
    out.append(part("Head body", break_edges(h, 0.5), "aluminium", kind="made", group="head"))
    cam = xcyl(LEN - cam_len - 1, LEN - 1, cam_d / 2, 0, cam_z)
    out.append(part("Camera head, IP68, 29 mm", break_edges(cam, 0.8), "matte_black", kind="bought", group="head"))
    for i, a in enumerate((60.0, 120.0), 1):
        out.append(part(f"Camera grub screw M3 {i}", radial(110.0, a, 14.5, R - 0.5, 1.5, cam_z), "stainless", kind="fastener", group="head"))
    for i, a in enumerate((270.0, 235.0), 1):
        out.append(part(f"Rod grub screw M4 {i}", radial(12.0, a, 5.0, R - 0.5, 2.0), "stainless", kind="fastener", group="head"))
    spk = ycyl(-16.8 - 4.0, -16.8, 10.0, 45.0, 0)
    out.append(part("Speaker, 20 mm IP67", break_edges(spk, 0.4), "matte_black", kind="bought", group="head"))
    cov = ycyl(-16.8 - 4.5, -16.8 - 4.0, 10.0, 45.0, 0)
    out.append(part("Speaker cover disc", break_edges(cov, 0.1), "stainless", kind="made", group="head"))
    bite = xcyl(LEN - 45, LEN - 5, 5.5, 0, 17.5)
    out.append(part("Bite valve", break_edges(bite, 1.0), "hdpe_natural", kind="bought", group="head"))
    return out


def _place(parts, tf):
    """Apply a Location/Pos*Rot transform to copies of parts."""
    out = []
    for q in parts:
        r = dict(q)
        r["shape"] = tf * q["shape"]
        out.append(r)
    return out


# ------------------------------------------------------------------------------------------------ option B
def option_b(p, shared):
    out = []
    rod_d, _ = p["b_rod"]
    zc = p["b_z_axis"]
    x_h0 = 4538.0 - 150.0                                # tip at the same x as option A's probe tip
    rx = p["b_reel_at"][0] + 1200.0                      # reel axis x (behind the operator's hand): -300
    hub_r, fl_r, tie_r, light_r, spin_r = 320.0, 400.0, 300.0, 355.0, 380.0   # reel: hub, flange, tie bolts, lightening holes, spinner
    r_wind = hub_r + rod_d / 2                           # centre of the wound rod (bending strain d / 2R = 1.5 per cent, VDS-STM-001)
    z_ax = zc - r_wind                                   # reel axis height
    y_ofs = -57.0                                        # puts the rod's exit turn on y = 0
    flA, flB = (14.0, 17.0), (77.0, 80.0)
    hub_y = (17.0, 77.0)
    plate_t, plate_w, plate_h = 8.0, 140.0, 840.0
    sh = Pos(rx, y_ofs, 0)                                # the whole reel is moved so the exit turn is on y = 0

    def reel(name, shape, material, kind="made", group="reel"):
        _mk(out, name, sh * shape, material, kind, group=group)

    # frame: foot bar, upright plate, two fillet welds
    foot = Pos(0, 80.0, 20.0) * Rot(-90, 0, 0) * Pos(0, 0, -200) * cp.rhs(60, 40, 3, 400)      # RHS along Y, z 0 to 40
    reel("Reel foot bar, RHS 60 x 40 x 3", foot, "aluminium")
    plate = cp.sheet(plate_w, plate_h, plate_t, holes=[(0, z_ax - 40.0 - plate_h / 2, 20.0)], r_corner=12.0)
    plate = Pos(0, 0, 40.0 + plate_h / 2) * Rot(90, 0, 0) * plate      # plane XZ, thickness toward -Y
    reel("Reel upright plate, 8 mm", plate, "aluminium")
    for i, ys in enumerate((0.0, -plate_t), 1):
        sy = 1 if ys == 0.0 else -1
        out.append(part(f"Weld bead plate to foot {i}", sh * bead(60.0, 6.0, -30.0, ys, 40.0, sy, 1), "mild_steel", kind="weld", group="reel"))
    # flanges, hub, bushes
    ar_s = math.radians(60)
    spin = (spin_r * math.cos(ar_s), spin_r * math.sin(ar_s))

    def flange(y0, y1, spinner=False):
        f = ycyl(y0, y1, fl_r)
        if spinner:
            f = f - ycyl(y0 - 1, y1 + 1, 4.2, spin[0], spin[1])
        f = f - ycyl(y0 - 1, y1 + 1, 15.0, 0, 0)
        for a in range(0, 360, 90):
            ar = math.radians(a + 45)
            f = f - ycyl(y0 - 1, y1 + 1, 4.25, tie_r * math.cos(ar), tie_r * math.sin(ar))
        for a in range(0, 360, 60):
            ar = math.radians(a + 30)
            f = f - ycyl(y0 - 1, y1 + 1, 35.0, light_r * math.cos(ar), light_r * math.sin(ar))
        return break_edges(f, 0.8)
    for nm, (y0, y1) in (("A", flA), ("B", flB)):
        fl = flange(y0, y1, nm == "B")
        reel(f"Reel flange {nm}, 3 mm", Pos(0, 0, z_ax) * fl, "aluminium")
    hub = ycyl(*hub_y, hub_r) - ycyl(hub_y[0] - 1, hub_y[1] + 1, hub_r - 3.0)
    reel("Reel hub tube, 640 x 3", Pos(0, 0, z_ax) * break_edges(hub, 0.5), "aluminium")
    for nm, (y0, y1) in (("A", flA), ("B", flB)):
        yc = (y0 + y1) / 2
        b = ycyl(yc - 7.5, yc + 7.5, 15.0) - ycyl(yc - 8.5, yc + 8.5, 10.0)
        reel(f"Axle bush {nm}, 30 x 20 x 15", Pos(0, 0, z_ax) * break_edges(b, 0.3), "brass", "bought")
    # axle bolt M20: head and washer on the -Y side of the plate, washer and nut after bush B
    y_w = -plate_t - 3.0
    y_b = flB[1] - 7.5 + 15.0 + 0.0 + 0.0 + 0.5 - 0.5
    y_bush_end = (flB[0] + flB[1]) / 2 + 7.5
    L_ax = (y_bush_end + 3.0 + 18.0 + 3.0) - y_w
    out.append(part("M20 axle bolt (ISO 4017)", sh * (Pos(0, y_w, z_ax) * Rot(90, 0, 0) * cp.hex_bolt(20, L_ax)), "stainless", kind="fastener", group="reel"))
    out.append(part("M20 axle washer A (ISO 7089)", sh * at(cp.washer(20), (0, y_w, z_ax), (-90, 0, 0)), "stainless", kind="fastener", group="reel"))
    out.append(part("M20 axle washer B (ISO 7089)", sh * at(cp.washer(20), (0, y_bush_end, z_ax), (-90, 0, 0)), "stainless", kind="fastener", group="reel"))
    out.append(part("M20 axle nut (ISO 4032)", sh * at(cp.hex_nut(20), (0, y_bush_end + 3.0, z_ax), (-90, 0, 0)), "stainless", kind="fastener", group="reel"))
    # four M8 tie bolts through both flanges clamp the hub between them
    for i in range(4):
        ar = math.radians(90 * i + 45)
        x, z = tie_r * math.cos(ar), z_ax + tie_r * math.sin(ar)
        for name, shp in cp.hex_bolt_set(8, 66.0):
            out.append(part(f"Tie bolt {i + 1}: {name}", sh * at(shp, (x, flB[1], z), (-90, 0, 0)), "stainless", kind="fastener", group="reel"))
    # spinner handle on flange B at r = 230: bolt head outboard, grip sleeve, washer and nut between the flanges
    ar = math.radians(60)
    hx, hz = spin_r * math.cos(ar), z_ax + spin_r * math.sin(ar)
    sleeve = ycyl(flB[1], flB[1] + 70.0, 11.0, hx, hz) - ycyl(flB[1] - 1, flB[1] + 71.0, 4.2, hx, hz)
    reel("Spinner grip sleeve", break_edges(sleeve, 1.5), "epdm", "bought")
    for name, shp in cp.hex_bolt_set(8, 73.0):
        out.append(part(f"Spinner bolt: {name}", sh * at(shp, (hx, flB[1] + 70.0, hz), (-90, 0, 0)), "stainless", kind="fastener", group="reel"))
    # stored turns of rod: two turns on the hub, the exit turn at y = 57 and one beside it
    for i, yy in enumerate((57.0, 37.0), 1):
        t = Pos(0, yy, z_ax) * Rot(90, 0, 0) * Torus(r_wind, rod_d / 2)
        reel(f"Push rod, stored turn {i}", t, "safety_yellow", "bought")
    # push rod, straight run from the exit point to the head
    x_end = x_h0 + 24.0
    rod = break_edges(xcyl(rx, x_end, rod_d / 2, 0, zc), 0.8) - (sh * Pos(0, 57.0, z_ax) * Rot(90, 0, 0) * Torus(r_wind, rod_d / 2))
    out.append(part("Push rod, glass fibre 10 mm", rod, "safety_yellow", kind="bought", group="rod"))
    # lines beside the rod: hose 12 mm above, cable 6 mm and water tube 4 mm to the sides
    pos_h, pos_c, pos_w = (0.0, 13.0), (10.0, 0.0), (-10.0, 0.0)
    x_l0 = 120.0
    out.append(part("Air hose, 12 x 10 mm", break_edges(xcyl(x_l0, x_h0 + 20.0, 6.0, pos_h[0], zc + pos_h[1]) - xcyl(x_l0 - 1, x_h0 + 21.0, 5.0, pos_h[0], zc + pos_h[1]), 0.4), "epdm", kind="bought", group="lines"))
    out.append(part("Camera and speaker cable, 6 mm", break_edges(xcyl(x_l0, x_h0 + 60.0, 3.0, pos_c[0], zc), 0.4), "rubber_belt", kind="bought", group="lines"))
    out.append(part("Water tube, 4 x 2.5 mm", break_edges(xcyl(x_l0, x_h0 + 18.0, 2.0, pos_w[0], zc), 0.3), "polycarbonate", kind="bought", group="lines"))
    # clips every 650 mm and one behind the head
    holes = [(0.0, 0.0, 10.4), (pos_h[0], pos_h[1], 12.4), (pos_c[0], 0.0, 6.4), (pos_w[0], 0.0, 4.4)]
    xs = [250.0 + p["b_clip_pitch"] * i for i in range(7)] + [x_h0 - 45.0]
    for i, x in enumerate(xs, 1):
        _clip(out, f"Rod clip {i}", x, 0.0, zc, holes)
    # head
    out += _place(head_parts(p, "rod"), Pos(x_h0, 0, zc))
    # shared surface unit
    out += [q for q in shared]
    return out


# ------------------------------------------------------------------------------------------------ option C
def option_c(p, shared):
    out = []
    zh = p["c_head_z"]
    R_plate, plate_t = 130.0, 10.0
    r_p, spread = 105.0, p["c_spread"]
    leg_od, leg_t, _ = p["c_leg"]
    ear_len, ear_h, ear_t, gap = 40.0, 50.0, 6.0, 32.6
    # head plate with the rope hole
    plate = Pos(0, 0, zh) * (Cylinder(R_plate, plate_t) - Cylinder(10.0, plate_t + 2))
    plate = break_edges(plate, 1.0)
    out.append(part("Head plate, 10 mm", plate, "aluminium", kind="made", group="tripod"))
    z_pin = zh - plate_t / 2 - ear_h / 2
    Ppin_l = (r_p, 0.0, z_pin)
    F_l = (spread, 0.0, 0.0)
    d = [F_l[i] - Ppin_l[i] for i in range(3)]
    n = math.sqrt(sum(v * v for v in d)); d = [v / n for v in d]
    back = 15.0
    P0_l = tuple(Ppin_l[i] - back * d[i] for i in range(3))
    L_leg = math.dist(P0_l, F_l)
    for k in range(3):
        phi = 90.0 + 120.0 * k
        rotz = Rot(0, 0, phi)
        # local frame: radial = +X, tangent = +Y
        leg = cp.round_tube(leg_od, leg_t, L_leg)
        leg = leg - along_dir(Cylinder(4.1, 40.0), Ppin_l, (0, 1, 0)) .moved(Location((0, 0, 0))) if False else leg
        legp = along_dir(leg, P0_l, d)
        legp = legp - Pos(*Ppin_l) * Rot(90, 0, 0) * Cylinder(4.1, 40.0)
        out.append(part(f"Tripod leg {k + 1}, tube 32 x 2", rotz * legp, "aluminium", kind="made", group="tripod"))
        # foot cap
        cap = along_dir(cp.round_tube(36.0, 2.0, 30.0), tuple(F_l[i] - 25.0 * d[i] for i in range(3)), d)
        out.append(part(f"Leg foot cap {k + 1}", rotz * break_edges(cap, 0.8), "epdm", kind="bought", group="tripod"))
        # two ear plates either side of the leg, welded to the underside of the head plate
        for j, sy in enumerate((1, -1), 1):
            yc = sy * (gap / 2 + ear_t / 2)
            ear = cp.sheet(ear_len, ear_h, ear_t, holes=[(0, 0, 8.2)], r_corner=4.0)
            ear = Pos(r_p, yc + ear_t / 2, z_pin) * Rot(90, 0, 0) * ear            # plane XZ, thickness toward -Y from yc + t/2
            out.append(part(f"Leg ear {k + 1}.{j}", rotz * ear, "aluminium", kind="made", group="tripod"))
            zplate = zh - plate_t / 2
            for m, (ys, ssy) in enumerate(((yc + ear_t / 2, 1), (yc - ear_t / 2, -1)), 1):
                out.append(part(f"Weld bead ear {k + 1}.{j}.{m}", rotz * bead(ear_len, 5.0, r_p - ear_len / 2, ys, zplate, ssy, -1), "mild_steel", kind="weld", group="tripod"))
        # clevis pin through ears and leg (head on the +Y ear), split pin beyond the -Y ear
        grip = gap + 2 * ear_t
        y_head = gap / 2 + ear_t
        pin = Pos(r_p, y_head, z_pin) * Rot(-90, 0, 0) * cp.clevis_pin(8, grip)
        out.append(part(f"Leg clevis pin {k + 1}, 8 mm (ISO 2341)", rotz * pin, "stainless", kind="fastener", group="tripod"))
        sp = Pos(r_p, y_head - grip - 8.0, z_pin) * cp.split_pin(8)
        out.append(part(f"Leg split pin {k + 1}", rotz * sp, "stainless", kind="fastener", group="tripod"))
    # ---- winch on the head plate: two cheeks, drum with flanges, axle, collars, crank, ratchet and pawl
    xd, zd = 62.0, zh + plate_t / 2 + 100.0
    dr, dw = 60.0, 80.0
    zp = zh + plate_t / 2
    for j, (y0, sy) in enumerate(((46.0, 1), (-52.0, -1)), 1):
        sh_ = cp.sheet(100.0, 220.0, 6.0, holes=[(0.0, zd - zp - 110.0, 12.5)], r_corner=8.0)
        sh_ = Pos(xd, y0 + 6.0, zp + 110.0) * Rot(90, 0, 0) * sh_
        out.append(part(f"Winch cheek {j}, 6 mm", sh_, "aluminium", kind="made", group="winch"))
        for m, (ys, ssy) in enumerate(((y0 + 6.0, 1), (y0, -1)), 1):
            if (sy == 1 and m == 2) or (sy == -1 and m == 1):
                pass
            out.append(part(f"Weld bead cheek {j}.{m}", bead(100.0, 5.0, xd - 50.0, ys, zp, ssy, 1), "mild_steel", kind="weld", group="winch"))
    drum = ycyl(-dw / 2, dw / 2, dr) - ycyl(-dw / 2 - 1, dw / 2 + 1, dr - 3.0)
    out.append(part("Winch drum tube, 120 x 3", Pos(xd, 0, zd) * break_edges(drum, 0.5), "aluminium", kind="made", group="winch"))
    for j, (y0, y1) in enumerate(((-dw / 2 - 3.0, -dw / 2), (dw / 2, dw / 2 + 3.0)), 1):
        f = ycyl(y0, y1, 80.0) - ycyl(y0 - 1, y1 + 1, 6.0)
        out.append(part(f"Winch drum flange {j}", Pos(xd, 0, zd) * break_edges(f, 0.5), "aluminium", kind="made", group="winch"))
    ax = ycyl(-85.0, 85.0, 6.0)
    out.append(part("Winch axle, 12 mm", Pos(xd, 0, zd) * break_edges(ax, 0.6), "stainless", kind="bought", group="winch"))
    for j, (y0, y1) in enumerate(((-62.0, -52.0), (52.0, 62.0)), 1):
        c = ycyl(y0, y1, 12.0) - ycyl(y0 - 1, y1 + 1, 6.0)
        out.append(part(f"Shaft collar {j}", Pos(xd, 0, zd) * break_edges(c, 0.5), "stainless", kind="bought", group="winch"))
    # ratchet wheel on the -Y end outside the collar; the pawl turns on a pin screwed into the cheek
    rw = ycyl(-72.0, -62.0, 40.0) - ycyl(-73.0, -61.0, 6.0)
    for i in range(12):
        a = math.radians(30 * i + 15)
        rw = rw - ycyl(-73.0, -61.0, 4.0, 40.0 * math.cos(a), 40.0 * math.sin(a))
    out.append(part("Ratchet wheel, 12 teeth", Pos(xd, 0, zd) * break_edges(rw, 0.3), "mild_steel", kind="made", group="winch"))
    px, pz = xd + 70.0, zd - 60.0                      # pawl pivot
    tx, tz = xd + 41.0 * math.cos(math.radians(-30)), zd + 41.0 * math.sin(math.radians(-30))
    dx, dz = tx - px, tz - pz
    ln = math.hypot(dx, dz)
    th = math.degrees(math.atan2(dx / ln, dz / ln))
    pawl = cp.sheet(12.0, 56.0, 4.0, holes=[(0, -25.0, 6.4)], r_corner=3.0)
    pawl = Pos(0, 0, 0) * Rot(90, 0, 0) * pawl                       # plane XZ, thickness toward -Y
    pawl = Pos(0, 0, 25.0) * pawl
    pawl = Pos(px, -67.0 + 0.0, pz) * Rot(0, th, 0) * pawl
    out.append(part("Ratchet pawl, 4 mm", pawl, "mild_steel", kind="made", group="winch"))
    out.append(part("Pawl pivot pin M6", Pos(px, -52.0, pz) * Rot(90, 0, 0) * (Pos(0, 0, 11.0) * Cylinder(3.0, 22.0)), "stainless", kind="fastener", group="winch"))
    # crank on the +Y end: arm, washer, nut, spinner grip
    arm = cp.sheet(26.0, 170.0, 4.0, holes=[(0, -70.0, 12.4), (0, 70.0, 8.4)], r_corner=8.0)
    arm = Pos(xd, 66.0, zd + 70.0) * Rot(90, 0, 0) * arm                       # plane XZ, y from 62 to 66
    out.append(part("Winch crank arm, 4 mm", arm, "aluminium", kind="made", group="winch"))
    out.append(part("M12 washer (ISO 7089)", at(cp.washer(12), (xd, 66.0, zd), (-90, 0, 0)), "stainless", kind="fastener", group="winch"))
    out.append(part("M12 hex nut (ISO 4032)", at(cp.hex_nut(12), (xd, 68.5, zd), (-90, 0, 0)), "stainless", kind="fastener", group="winch"))
    gx, gz = xd, zd + 140.0
    sleeve = ycyl(66.0, 126.0, 11.0, gx, gz) - ycyl(65.0, 127.0, 4.2, gx, gz)
    out.append(part("Crank grip sleeve", break_edges(sleeve, 1.5), "epdm", kind="bought", group="winch"))
    for name, shp in cp.hex_bolt_set(8, 4.0 + 60.0):
        out.append(part(f"Crank handle bolt: {name}", at(shp, (gx, 126.0, gz), (-90, 0, 0)), "stainless", kind="fastener", group="winch"))
    # ---- rope, sonde and lines hanging in the hole
    depth = p["c_depth"]
    tip = -depth
    head_len = 150.0
    # rope runs from the drum tangent (x = 0) down to the eye of the eye bolt
    z_eye = tip + head_len + 22.0 + 6.0 + 4.0 + 26.0
    rope = Pos(0, 0, (zd + z_eye) / 2) * Cylinder(p["c_rope"] / 2, zd - z_eye)
    _mk(out, "Stainless wire rope 4 mm, 7x19", rope, "stainless", "bought", group="rope")
    # sonde: head with its tip down. Local +X (the head axis, tip end) maps to -Z.
    sonde = _place(head_parts(p, "eye"), Pos(0, 0, tip + head_len) * Rot(0, 90, 0))
    out += sonde
    # eye bolt (M8) screwed into the head's rear socket: shank down, ring above
    zt = tip + head_len
    eb = Pos(0, 0, zt + 22.0 - 11.0) * Cylinder(4.0, 22.0)
    ring = Pos(0, 0, zt + 22.0 + 6.0) * Rot(90, 0, 0) * (Torus(4.8, 1.8))
    out.append(part("Eye bolt M8", eb + ring, "stainless", kind="fastener", group="rope"))
    fer = Pos(0, 0, zt + 22.0 + 6.0 + 9.5 + 10.0) * (Cylinder(4.5, 20.0) - Cylinder(2.0, 22.0))
    _mk(out, "Rope end ferrule", fer, "stainless", "bought", group="rope")
    # lines clipped to the rope, from the sonde up to 300 mm above the slab (local head port y, z -> world x, y)
    ph, pc, pw = (13.0, 0.0), (0.0, 10.0), (0.0, -10.0)
    hose = Pos(ph[0], ph[1], (zt - 20.0 + 300.0) / 2) * (Cylinder(6.0, 300.0 - zt + 20.0) - Cylinder(5.0, 300.0 - zt + 22.0))
    _mk(out, "Air hose, 12 x 10 mm", hose, "epdm", "bought", group="lines")
    _mk(out, "Camera and speaker cable, 6 mm", Pos(pc[0], pc[1], (zt - 60.0 + 300.0) / 2) * Cylinder(3.0, 300.0 - zt + 60.0), "rubber_belt", "bought", group="lines")
    _mk(out, "Water tube, 4 x 2.5 mm", Pos(pw[0], pw[1], (zt - 18.0 + 300.0) / 2) * Cylinder(2.0, 300.0 - zt + 18.0), "polycarbonate", "bought", group="lines")
    holes = [(0.0, 0.0, 4.6), (ph[0], ph[1], 12.4), (pc[0], pc[1], 6.4), (pw[0], pw[1], 4.4)]
    n_clip = 6
    for i in range(n_clip):
        zc_ = (zt + 600.0) + (0.0 - zt - 600.0) * i / (n_clip - 1)
        s_ = Pos(0, 0, zc_) * Cylinder(22.0, 15.0)
        for dx_, dy_, dd in holes:
            s_ = s_ - Pos(dx_, dy_, zc_) * Cylinder(dd / 2, 17.0)
        out.append(part(f"Rope clip {i + 1}", break_edges(s_, 1.0), "hdpe_natural", kind="made", group="clips"))
    # the slab with the 51 mm hole (context)
    slab = Pos(0, 0, -150.0) * Box(2400, 2400, 300.0) - Pos(0, 0, -150.0) * Cylinder(p["c_hole"] / 2, 302.0)
    out.append(part("Concrete slab with 51 mm hole (site)", slab, "concrete", kind="context", group="context"))
    out += [q for q in shared]
    return out
