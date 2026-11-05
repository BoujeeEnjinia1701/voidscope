"""VoidScope product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is: rod sections, couplers with
their pins and snap buttons, collar, nose, base link, bending links with their hinge pins, tip housing,
camera, steering wires and housings, tail cap, grip, the surface unit case with its equipment plate,
battery, blower, flow meter, modules, monitor and bracket, wall fittings, intake filter, reservoir
stand and bottle, and every screw. Only these are added: the steered pose of the camera tip for the
hero and detail views (the same links, pins, tip housing and camera turned about their own pivots,
with a sleeve sheath), the three lines from the probe to the surface unit (air hose, camera cable,
water tube), and the site as context parts: a broken concrete wall with a 51 mm core hole, a slab
resting on rubble piers over the void, rubble at the foot of the wall and a 1.75 m mannequin standing on
the ground behind the tail cap. Ground level is model z = 0 (photoreal --ground-z=0) and every site
part reaches below it. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "product" (everything except the tip and the head), "head" (collar, nose, base link, speaker),
"tipstraight" and "tipbent" (the tip parts, straight or steered), "lines", "context" (site and figure).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot, Sphere  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402
from vds_geom import derived, xcyl, xtube, rod_between, bx  # noqa: E402

TITLE = "VoidScope: rubble void search probe with water and air lines"

TIP_BEND = -45.0        # deg; the hero and detail views show the tip steered 45 deg toward -Y (toward the viewer)

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=38,-55", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["product", "head", "tipbent", "lines", "context"], "explode": False, "el": 20, "az": -35,
     "args": _SITE,
     "note": "Site render from the front right and above (about 20 deg elevation): the probe pushed through a 51 mm "
             "core hole in a broken wall into a rubble void, head under a fallen slab with its camera tip steered "
             "45 deg, steering lever on the rod ahead of the grip, surface unit with its lid open and water bottle on "
             "its stand beside the operator (1.75 m mannequin standing on the ground)"},
    {"name": "studio", "groups": ["product", "head", "tipstraight"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render from the front right and above (about 24 deg elevation): the whole probe straight, "
             "surface unit with its lid open, reservoir stand and bottle, without the site"},
    {"name": "exploded", "groups": ["product", "head", "tipstraight"], "explode": True, "el": 28, "az": -50,
     "note": "Exploded view from the front right and above (about 28 deg elevation): rod sections, couplers and snap "
             "buttons pulled apart along the probe; collar, speaker, nose, base link, bending links, tip housing and "
             "camera ahead of section 1; steering control lifted off section 4; tail cap and grip behind; surface unit "
             "plate, battery, blower, flow meter, modules and monitor lifted out of the case"},
    {"name": "detail", "groups": ["head", "tipbent"], "explode": False, "el": 18, "az": -30,
     "note": "Detail from the front right, slightly above (about 18 deg elevation), close on the head: camera tip "
             "steered 45 deg on its sheathed bending section, camera window and LEDs in the tip housing, bite valve "
             "on the nose with its water tube, six air outlets and the speaker grille on the collar, front of "
             "section 1"},
]

# model groups that make up the head (framed for the detail view)
_HEAD = {"collar", "nose", "base", "speaker", "waterset"}
_TIP = {"links", "tiph", "camera"}


def _pivots():
    D = derived()
    return D["pivots"]


def _camz():
    return M.PARAMS["z_axis"] + M.PARAMS["nose"][3]


def _pose(shape, k):
    """Turn a shape that lies beyond joint k (count of joints behind it) by its share of the bend."""
    nj = M.PARAMS["n_joint"]
    phi = TIP_BEND / nj
    zc = _camz()
    for j in reversed(range(k)):
        x = _pivots()[j]
        shape = Pos(x, 0, zc) * Rot(0, 0, phi) * Pos(-x, 0, -zc) * shape
    return shape


def _bent_sheath():
    P = M.PARAMS
    D = derived()
    nj = P["n_joint"]
    R = P["link"][0] / 2
    t = P["sheath"]
    zc = _camz()
    sl = [xtube(D["x_nf"] + 0.5, D["gaps"][0] + P["link"][3] / 2, R + t, R, 0, zc)]
    for i in range(1, nj):
        sl.append(_pose(xtube(D["pivots"][i - 1] - 1.0, D["pivots"][i] + 1.0, R + t, R, 0, zc), i))
    sl.append(_pose(xtube(D["pivots"][-1] - 1.0, D["x_th0"] + 6.0, R + t, R, 0, zc), nj))
    out = sl[0]
    for s in sl[1:]:
        out = out + s
    return out


def _tip_bent(p):
    """The steered version of a tip part of the model, or None for a part that stays out of the bent view."""
    n = p["name"]
    if n.startswith("Bending link "):
        return _pose(p["shape"], int(n.split()[-1]))
    if n.startswith("Hinge pin"):
        k = (int(n.split()[-1]) - 1) // 2          # two pins per joint
        return _pose(p["shape"], k)
    if n.startswith(("Tip housing", "Camera grub", "Camera head")):
        return _pose(p["shape"], M.PARAMS["n_joint"])
    if n == "Bending section sheath":
        return _bent_sheath()
    return None


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


def lines():
    """Air hose, camera cable and water tube from the tail end of the probe to the surface unit (appearance
    only: they lie on the ground in loops, as the 7 m hose and 8 m tube do in use)."""
    P = M.PARAMS
    zc = P["z_axis"]
    out = []
    ctx = lambda n, sh, mat, col: out.append(part(n, sh, mat, kind="context", group="lines", color=col))
    barb = (12.0, -52.0, zc)
    air_in = (550.0, -660.0, 70.0)
    cam_sock = (370.0, -660.0, 70.0)
    bottle_sp = (1170.0, -830.0, 1325.0)
    hose = _polyline(_bezier(barb, (0, -420, 400), (420, -420, 20), air_in), 9.0)
    ctx("Air hose, translucent silicone", hose, "polycarbonate", "#E5E7EB")
    cable = _polyline(_bezier((-150.0, 0.0, 940.0), (-380, -60, 500), (150, -380, 25), cam_sock), 3.0)
    ctx("Camera cable to the surface unit, black", cable, "epdm", "#111111")
    wline = _polyline(_bezier((-150.0, 0.0, 962.0), (-340, 120, 1000), (700, -500, 1300), bottle_sp), 2.0)
    ctx("Water tube to the bottle, blue polyurethane", wline, "polycarbonate", "#3B82F6")
    return out


def site():
    """Site context: a broken concrete wall (core hole 51 mm at the probe axis), a slab resting on two rubble
    piers over the void, rubble at the foot of the wall, and a mannequin standing behind the tail cap. Ground level
    is model z = 0; every site part reaches below it."""
    P = M.PARAMS
    zc = P["z_axis"]
    out = []
    ctx = lambda n, sh, mat="concrete": out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    xw = 1800.0
    wall = Pos(xw + 120, 0, 600) * Box(240, 1700, 1800)
    wall = wall + Pos(xw + 120, -400, 1650) * Rot(18, 0, 0) * Box(240, 800, 300)
    wall = wall - xcyl(xw - 10, xw + 260, 25.5, 0, zc)
    ctx("Broken concrete wall with a 51 mm core hole", wall)
    # slab over the void, on two rubble piers
    ctx("Fallen slab over the void", Pos(4100, 0, 1650) * Rot(0, 3, 0) * Box(2300, 1600, 170))
    ctx("Rubble pier at the near end", Pos(3180, 0, 700) * Rot(0, 0, 8) * Box(380, 1500, 1500))
    ctx("Rubble pier at the far end", Pos(5000, 0, 700) * Rot(0, 0, -6) * Box(380, 1500, 1500))
    for i, (rx, ry, a, s) in enumerate(((xw - 150, 520, 20, 260), (xw - 60, -640, -35, 200), (xw + 500, 320, 10, 300),
                                         (xw + 760, -420, 40, 220), (xw - 280, 160, 65, 120), (3600, 520, 25, 240),
                                         (4600, -460, -20, 260))):
        h = s * 0.5
        blk = Pos(rx, ry, h / 2 - 25) * Rot(0, 0, a) * Rot(10, 6, 0) * Box(s, s * 0.7, h)
        ctx(f"Concrete rubble {i + 1}", blk)
    try:
        from context_parts import mannequin
        person = Pos(-430, 330, 0) * Rot(0, 0, 90) * mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", person, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        q = dict(p)
        if p["group"] in _TIP:
            if p["name"] == "Tip housing":
                q["color"] = "#1B1D20"           # black anodised (VDS-DDR-006 F1)
            q["group"] = "tipstraight"
            out.append(q)
            r = dict(p)
            r["group"] = "tipbent"
            if p["name"] == "Tip housing":
                r["color"] = "#1B1D20"
            sh = _tip_bent(p)
            if sh is not None:
                r["shape"] = sh
                out.append(r)
            continue
        if p["name"].startswith("Steering wire") or p["group"] == "cable":
            # the part of the wire or cable ahead of the nose lies inside the tip; leave it out so it never
            # shows through the steered sheath
            q["shape"] = p["shape"] & bx(-1000, derived()["x_nf"], -200, 200, -10, 2000)
            q["group"] = "product"
            out.append(q)
            continue
        q["group"] = "head" if p["group"] in _HEAD else "product"
        out.append(q)
    return out + lines() + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "context" for p in ps), "context;", sorted({p["group"] for p in ps}))
    for p in ps:
        if p["group"] in ("tipbent", "lines", "context"):
            s = p["shape"]
            print(f"{p['name']:52s} {p['group']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
