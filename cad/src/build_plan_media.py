"""VoidScope prototype build plan pictures (VDS-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/VDS-DWG-101 to 109        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring and the air and water lines (matplotlib)
Long lines (cable, guide tube, water tube) are drawn cut short where a picture would otherwise be
four metres wide; the caption says so. Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
C = build_components(P)
ZC = P["z_axis"]

COL = {"rod": "#D1D5DB", "coupler": "#0F766E", "button": "#B91C1C", "pins": "#111827", "tailcap": "#4B5563",
       "barb": "#B45309", "grommet": "#111827", "grip": "#1F2937", "cable": "#B45309", "guide": "#E5E7EB",
       "wtube": "#2563EB", "bite": "#1D4ED8", "collar": "#6B7280", "nose": "#9CA3AF", "camera": "#1F2937",
       "ring": "#111827", "speaker": "#374151", "cover": "#A8A29E", "case": "#F59E0B", "lid": "#FBBF24",
       "eplate": "#A8A29E", "spacer": "#111827", "battery": "#C2410C", "blower": "#334155", "modules": "#16A34A",
       "flowmeter": "#0EA5E9", "fmb": "#64748B", "fittings": "#111827", "filter": "#E5E7EB", "monitor": "#1E293B",
       "dbracket": "#64748B", "stand": "#374151", "bottle": "#93C5FD"}


def _b():
    import build123d as b
    return b


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*ks):
    return fuse([C[k].shape for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(shape, dx=0, dy=0, dz=0):
    return _b().Pos(dx, dy, dz) * shape


def win(shape, x0, x1, y0=-60, y1=60, z0=None, z1=None):
    b = _b()
    z0 = ZC - 60 if z0 is None else z0
    z1 = ZC + 60 if z1 is None else z1
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def sec_x(k):
    """(back, front) x of rod section k (1 is at the front)."""
    return D["sections"][P["n_sec"] - k]


def section_set(k):
    return S(f"rod{k}")


def coupler_set(k):
    return S(f"coupler{k}", f"button{k}", f"spring{k}", f"pins{k}")


SU = ["case", "lid", "eplate", "espacers", "battery", "blower", "blower_legs", "modules", "flowmeter", "fm_bracket",
      "fittings", "filter", "monitor", "dbracket"]


# ----------------------------------------------------------------- overview
def overview():
    """Rod sections side by side as they lie in the carry case, head parts pulled apart ahead of
    section 1, surface unit and stand behind. Long lines are cut to 1 m."""
    xc = D["x_collar"]
    s1b = sec_x(1)[0]
    items = []
    # sections side by side, back ends level with section 1's back end
    rods = [mv(S(f"rod{k}"), s1b - sec_x(k)[0], (k - 1) * 90.0) for k in range(1, 5)]
    items.append(part("Rod sections (4), side by side", fuse(rods), COL["rod"]))
    cps = [mv(coupler_set(k), s1b - sec_x(k)[0] + 120, (k - 1) * 90.0) for k in range(1, 5)]
    items.append(part("Couplers with snap buttons and pins (4)", fuse(cps), COL["coupler"]))
    items.append(part("Collar", mv(S("collar", "spg_grommet"), 260), COL["collar"]))
    items.append(part("Nose", mv(S("nose", "nose_screws"), 420), COL["nose"]))
    items.append(part("Tail cap, air barb, grommets", mv(S("tailcap", "barb", "tc_grommets", "tc_pins"), s1b - sec_x(4)[0] - 140, 270), COL["tailcap"]))
    items.append(part("Camera head and spacer ring", mv(S("camera", "cam_ring"), 560, 0, 0), COL["camera"]))
    items.append(part("Speaker and cover", mv(S("speaker", "spk_cover"), 260, -110), COL["speaker"]))
    cut = lambda k_, a, b_: win(C[k_].shape, a, b_, -80, 80)  # noqa: E731
    items.append(part("Camera cable (7 m, shown cut)", mv(cut("cable", xc - 900, xc), 0, -200, 0), COL["cable"]))
    items.append(part("Water guide tube (6.5 m, shown cut)", mv(cut("guide", xc - 900, xc), 0, -260, 0), "#9CA3AF"))
    items.append(part("Grip", mv(S("grip"), s1b - sec_x(4)[0], 270, 90), COL["grip"]))
    items.append(part("Water tube and bite valve (shown cut)", mv(win(S("wtube", "bite"), xc - 500, D["x_tip"] + 5, -80, 80), 300, -330), COL["wtube"]))
    # surface unit, pulled apart upward, placed behind the rods
    sdx, sdy = (s1b - 1150) - D["case_x"][0], -1250 - D["case_y"][0]
    su = lambda k_, dz=0: mv(C[k_].shape, sdx, sdy, dz)  # noqa: E731
    items.append(part("Equipment plate and spacers", fuse([su("eplate", 140), su("espacers", 140)]), COL["eplate"]))
    items.append(part("Flow meter and bracket", fuse([su("flowmeter", 300), su("fm_bracket", 300)]), COL["flowmeter"]))
    items.append(part("Battery, blower, control modules", fuse([su("battery", 300), su("blower", 300), su("blower_legs", 300), su("modules", 300)]), COL["battery"]))
    items.append(part("Case, drilled, with wall fittings and filter", fuse([su("case"), su("fittings"), su("filter")]), COL["case"]))
    items.append(part("Lid with monitor bracket and monitor", fuse([su("lid"), su("dbracket"), su("monitor")]), COL["lid"]))
    items.append(part("Reservoir stand and bottle", mv(S("stand", "bottle"), (s1b - 1900) - P["stand"][0], 200 - P["stand"][1]), COL["stand"]))
    return bv.overview(items, OUT / "overview.png", "VoidScope prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Rods side by side as stored; cable and tubes drawn cut short. Seen from the front right and above",
                       elev=22, azim=-55, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    b = _b()
    out = []
    base = dict(project="VoidScope", date=DATE)
    s2x = sec_x(2)
    rod2 = S("rod2")
    nb = [part("Coupler", S("coupler2"), COL["coupler"]), part("Section 1", win(S("rod1"), sec_x(1)[0], sec_x(1)[0] + 200), COL["rod"]),
          part("Section 3", win(S("rod3"), sec_x(3)[1] - 200, sec_x(3)[1]), COL["rod"])]
    # 101 rod section
    out.append(bv.component_sheet(
        Part("Rod section", win(rod2, s2x[0] - 1, s2x[1] + 1), COL["rod"]), nb,
        dwg_no="VDS-DWG-101", title="VoidScope rod section (make 4): making sketch",
        material="6061-T6 drawn tube 38.1 x 1.47 mm (1.5 x 0.058 in)",
        view_shape=mv(rod2, -s2x[0], 0, -ZC), inset_view=(25, -60),
        notes=["Make four. Cut 1,050 mm, square, from 38.1 x 1.47 mm tube.",
               "Deburr inside and out; the inside edge must not cut the cable.",
               "Scribe a straight line along the tube: the button line (+Y).",
               "Back end, sections 1 to 3: drill 8.5 mm on the button line,",
               "  30 mm from the end. This takes the next section's button.",
               "",
               "",
               "Back end, section 4: no button hole; the tail cap pins go in",
               "  4.0 mm holes top and bottom, 20 mm from the end (step 2).",
               "Front end: the coupler pin holes, 4.0 mm top and bottom 30 mm",
               "  from the end, are drilled through with the coupler fitted.",
               "Depth marks every 100 mm from the tip, section number at each",
               "  end, paint marker under clear heat-shrink.",
               "Check: the next coupler slides in by hand with no rock."], **base))
    # 102 coupler
    cp = S("coupler2")
    cx0 = s2x[1] - P["coupler"][3]
    out.append(bv.component_sheet(
        Part("Coupler", cp, COL["coupler"]), [part("Section 2", win(rod2, s2x[1] - 150, s2x[1]), COL["rod"]),
                                              part("Section 1", win(S("rod1"), sec_x(1)[0], sec_x(1)[0] + 120), COL["rod"]),
                                              part("Snap button", S("button2", "spring2"), COL["button"])],
        dwg_no="VDS-DWG-102", title="VoidScope coupler (make 4): making sketch",
        material="6061-T6 drawn tube 34.93 x 2.11 mm (1.375 x 0.083 in)",
        view_shape=mv(cp, -cx0, 0, -ZC), inset_view=(25, -60),
        notes=["Make four. Cut 120 mm from 34.93 x 2.11 mm tube; deburr.",
               "Chamfer the outside of one end 1 mm x 45 deg: the free end.",
               "Drill 8.5 mm for the snap button 30 mm from the free end.",
               "Fit the V-spring button from inside, button out through",
               "  the hole. Spring legs lie flat across the bore (top to",
               "  bottom stays clear for the cable and guide tube).",
               "Bond: the plain end goes 60 mm into the section's front end",
               "  with structural epoxy, button on the section's button line.",
               "Drill 4.0 mm through tube and coupler, top and bottom, 30 mm",
               "  from the section end; press in the pins flush both sides.",
               "Fit: 0.11 mm a side in the next tube; it must slide freely.",
               "Check: pull hard by hand; nothing moves; button pops fully."], **base))
    # 103 nose
    xn = D["x_nose"]
    out.append(bv.component_sheet(
        Part("Nose", S("nose"), COL["nose"]), [part("Collar", S("collar"), COL["collar"]), part("Camera", S("camera"), COL["camera"]),
                                               part("Bite valve", S("bite"), COL["bite"])],
        dwg_no="VDS-DWG-103", title="VoidScope nose: making sketch", material="6061-T6 round bar 50 mm, 80 mm long",
        view_shape=mv(S("nose"), -xn, 0, -ZC), inset_view=(30, -55),
        notes=["Lathe: face and turn to 48 mm outside, 75 mm long.",
               "Back end: bore 40.2 mm, 12 mm deep, for the collar spigot.",
               "Offset the work 6.5 mm (4-jaw chuck): bore the camera",
               "  29.3 mm from 12 to 72 mm, then 26 mm through the front",
               "  3 mm. The camera sits below the axis; walls 2.85 mm.",
               "Mill or saw and file on top: pocket 11.5 mm wide, floor",
               "  12 mm above the axis, 50 mm back from the front face.",
               "Groove on top 4.5 mm wide, floor 20 mm above the axis,",
               "  from the back face to the pocket (breaks into the bore).",
               "Three 4.5 mm holes 6 mm from the back face, at 30, 150",
               "  and 270 deg from the side; countersink for M4.",
               "Break all edges 0.5 mm. Check: camera slides in by hand."], **base))
    # 104 collar
    xcl = D["x_collar"]
    out.append(bv.component_sheet(
        Part("Collar", S("collar"), COL["collar"]), [part("Section 1 and coupler", win(S("rod1", "coupler1"), xcl - 200, xcl + 70), COL["rod"]),
                                                     part("Nose", S("nose"), COL["nose"]), part("Speaker", S("speaker", "spk_cover"), COL["speaker"])],
        dwg_no="VDS-DWG-104", title="VoidScope collar: making sketch", material="6061-T6 round bar 50 mm, 115 mm long",
        view_shape=mv(S("collar"), -xcl, 0, -ZC), inset_view=(30, -55),
        notes=["Lathe: 48 mm outside x 98 mm, then a 40 mm spigot 12 long.",
               "Back: bore 35.16 mm, 60 deep (a coupler must slide in).",
               "Bore 30 mm from 60 to 94 mm: the air plenum; 4 mm front wall.",
               "Spigot: 14 mm bore 6.5 mm below the axis, through, for the",
               "  cable grommet. Tap three M4 holes 6 mm deep, 4 from its end.",
               "Button hole 8.5 mm on the button line, 30 mm from the back;",
               "  spotface 14 mm down to 20.3 mm from the axis.",
               "Six 5 mm outlets 79 mm from the back face, at 0, 45, 135,",
               "  225, 270 and 315 deg from the button line toward the top.",
               "Speaker pocket on the far side: 20.5 mm, flat floor 16.8 mm",
               "  from the axis, 79 mm back; 3 mm wire hole into the plenum.",
               "Water exit 4.5 mm at 45 deg on top, axis crossing 12 mm",
               "  above the axis 72 mm from the back; groove 4.5 x 4 on top.",
               "Check: coupler, nose and speaker fit; blow through outlets."], **base))
    # 105 tail cap
    out.append(bv.component_sheet(
        Part("Tail cap", S("tailcap"), COL["tailcap"]), [part("Section 4", win(S("rod4"), 0, 200), COL["rod"]),
                                                         part("Air barb", S("barb"), COL["barb"]), part("Grommets", S("tc_grommets"), COL["grommet"])],
        dwg_no="VDS-DWG-105", title="VoidScope tail cap: making sketch", material="6061-T6 round bar 50 mm, 70 mm long",
        view_shape=mv(S("tailcap"), 0, 0, -ZC), inset_view=(30, -120),
        notes=["Lathe: flange 44 mm outside x 25 mm; plug 35.0 mm x 40 mm",
               "  (0.08 mm a side in the rod: bonded, not a slide fit).",
               "Bore 30 mm from the plug end to 8 mm from the back face.",
               "End wall: 10 mm hole 10 mm below the axis (cable) and",
               "  12 mm hole 10 mm above it (guide tube); deburr; grommets.",
               "Side of the flange, away from the button line: drill and",
               "  tap 1/4 BSP 12.5 mm from the back face into the bore.",
               "Pins: drill 4.0 mm top and bottom through rod and plug",
               "  20 mm in front of the flange after bonding (step 2).",
               "Check: plug enters the rod fully; barb seals with tape."], **base))
    # 106 equipment plate
    pl = S("eplate")
    bb = pl.bounding_box()
    out.append(bv.component_sheet(
        Part("Equipment plate", pl, COL["eplate"]), [part("Case base", S("case"), COL["case"]), part("Battery", S("battery"), COL["battery"]),
                                                     part("Blower", S("blower"), COL["blower"]), part("Modules", S("modules"), COL["modules"])],
        dwg_no="VDS-DWG-106", title="VoidScope equipment plate: making sketch", material="5052 aluminium sheet 3 mm",
        view_shape=mv(pl, -bb.min.X, -bb.min.Y, -bb.min.Z), inset_view=(45, -60),
        notes=["Cut 330 x 300 mm from 3 mm sheet; round corners 5 mm.",
               "Corner holes 5.5 mm, 15 mm in from each edge: the four",
               "  spacers and M5 screws through the case floor.",
               "Mark the parts from the corner nearest the case's -X, -Y",
               "  corner: battery at 12, 12 (151 x 65); strap slots 4 x 25",
               "  mm each side of it; blower at 12, 110 on four standoffs;",
               "  modules tray at 175, 12; flow meter angle at 280, 230.",
               "Drill each fixing to suit the part as bought (M3 or M4).",
               "Deburr; no sharp edge near the battery leads.",
               "Check: lay every part on the plate before drilling."], **base))
    # 107 monitor bracket (posed with the lid; drawn flat)
    db = S("dbracket")
    out.append(bv.component_sheet(
        Part("Monitor bracket", db, COL["dbracket"]), [part("Lid", S("lid"), COL["lid"]), part("Monitor", S("monitor"), COL["monitor"])],
        dwg_no="VDS-DWG-107", title="VoidScope monitor bracket: making sketch", material="5052 aluminium sheet 2 mm",
        view_shape=_b().Pos(0, 0, 0) * _flat_bracket(), inset_view=(20, -150),
        notes=["Blank 210 x 195 mm from 2 mm sheet. Fold lines 20 and 35 mm",
               "  in from each 195 mm end: 140 mm plate, 15 mm legs, 20 mm feet.",
               "Fold the legs 90 deg, then the feet 90 deg outward, so the",
               "  plate stands 15 mm off the lid floor.",
               "Feet: two 5.5 mm holes each, 25 mm in from the ends, for",
               "  M5 screws through the lid with bonded sealing washers.",
               "Plate: holes to suit the monitor's rear M4 holes; a 25 mm",
               "  hole for its leads.",
               "Check: monitor and bracket stand 45 mm deep; the lid closes."], **base))
    # 108 case drilling
    cs = S("case")
    cb = cs.bounding_box()
    out.append(bv.component_sheet(
        Part("Case base, drilled", cs, COL["case"]), [part("Wall fittings", S("fittings"), COL["fittings"]), part("Filter", S("filter"), COL["filter"]),
                                                      part("Plate", S("eplate"), COL["eplate"])],
        dwg_no="VDS-DWG-108", title="VoidScope surface unit case: drilling sketch", material="Bought IP67 case, polypropylene",
        view_shape=mv(cs, -cb.min.X, -cb.min.Y, 0), inset_view=(30, -60),
        notes=["Bought case 410 x 330 x 175 mm; drill the base only as here.",
               "Wall toward the probe (the +Y long side), 70 mm up from the",
               "  floor outside: 16 mm for the camera socket 120 mm from the",
               "  left end; 12 mm for the headset socket at 200 mm; 12.5 mm",
               "  for the air outlet bulkhead at 300 mm.",
               "Opposite wall: 21 mm for the intake filter, 150 mm from the",
               "  left end, 65 mm up.",
               "Floor: four 5.5 mm holes matching the plate's corner holes.",
               "Lid: four 5.5 mm holes for the monitor bracket feet.",
               "Use a step drill, slow; deburr; every hole gets its seal.",
               "Check: the case still closes and latches."], **base))
    # 109 flow meter bracket
    fb = S("fm_bracket")
    fbb = fb.bounding_box()
    out.append(bv.component_sheet(
        Part("Flow meter bracket", fb, COL["fmb"]), [part("Flow meter", S("flowmeter"), COL["flowmeter"]), part("Plate", S("eplate"), COL["eplate"])],
        dwg_no="VDS-DWG-109", title="VoidScope flow meter bracket: making sketch", material="Aluminium angle 40 x 40 x 3 mm",
        view_shape=mv(fb, -fbb.min.X, -fbb.min.Y, -fbb.min.Z), inset_view=(25, -50),
        notes=["Cut 30 mm off 40 x 40 x 3 mm angle; trim the upright leg",
               "  to 95 mm long from a longer piece, or bolt a 30 x 95 mm",
               "  strip to the angle with two M4 screws.",
               "Base leg: two 4.5 mm holes for M4 to the plate.",
               "Upright: holes to match the flow meter's panel screws.",
               "The meter must stand upright for its float to read.",
               "Check: meter vertical to within 2 deg with a level."], **base))
    return out


def _flat_bracket():
    """The monitor bracket as built with the lid closed (plate parallel to the floor), for the views."""
    import model as m
    L, W, hb, hl, t = P["case"]
    x0, y0 = P["case_at"]
    mw, mh, md = P["monitor"]
    bt, so, foot = P["dbracket"]
    zf = hb + hl - t
    cx, cy = x0 + L / 2, y0 + W / 2
    bx = m.bx
    pl = bx(cx - mh / 2 - 10, cx + mh / 2 + 10, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf - so)
    feet = [bx(cx - mh / 2 - 10, cx - mh / 2 - 10 + bt, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf),
            bx(cx + mh / 2 + 10 - bt, cx + mh / 2 + 10, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - so - bt, zf),
            bx(cx - mh / 2 - 10 - foot, cx - mh / 2 - 10 + bt, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - bt, zf),
            bx(cx + mh / 2 + 10 - bt, cx + mh / 2 + 10 + foot, cy - mw / 2 - 5, cy + mw / 2 + 5, zf - bt, zf)]
    s = fuse([pl] + feet)
    bb = s.bounding_box()
    return mv(s, -bb.min.X, -bb.min.Y, -bb.min.Z)


# ----------------------------------------------------------------- joints
def joints():
    out = []
    # 01 rod joint: coupler 2 in section 1... use the joint between sections 2 and 1
    j = sec_x(2)[1]
    out.append(bv.joint([
        part("Section 2 (front end)", win(S("rod2"), j - 90, j), COL["rod"]),
        part("Section 1 (back end)", win(S("rod1"), j, j + 90), "#E5E7EB"),
        part("Coupler, bonded in section 2", win(S("coupler2"), j - 90, j + 90), COL["coupler"]),
        part("Snap button and V-spring", win(S("button2", "spring2"), j - 90, j + 90), COL["button"]),
        part("Pins, top and bottom", win(S("pins2"), j - 90, j + 90), COL["pins"]),
        part("Cable", win(S("cable"), j - 90, j + 90), COL["cable"]),
        part("Guide tube", win(S("guide"), j - 90, j + 90), "#9CA3AF")],
        OUT / "joint-01.png", "Joint 1: two rod sections joined by the coupler and snap button",
        subtitle="Cut on the vertical centre plane, seen from the side. Tube ends butt; the button locks; cable and guide pass the spring",
        cut="+Y", elev=10, azim=-75, size=(8, 6)))
    # 02 collar socket
    xc = D["x_collar"]
    out.append(bv.joint([
        part("Section 1 (front end)", win(S("rod1"), xc - 80, xc), COL["rod"]),
        part("Coupler 1", win(S("coupler1"), xc - 80, xc + 70), COL["coupler"]),
        part("Snap button in the spotface", win(S("button1", "spring1"), xc - 80, xc + 70), COL["button"]),
        part("Collar socket", win(S("collar"), xc, xc + 70), COL["collar"])],
        OUT / "joint-02.png", "Joint 2: section 1 into the collar socket",
        subtitle="Seen from the button side. The button stands just proud in a 14 mm spotface so a fingertip can press it",
        elev=20, azim=-15, size=(8, 6)))
    # 03 head cut open
    out.append(bv.joint([
        part("Collar", win(S("collar"), xc + 40, D["x_tip"] + 1), COL["collar"]),
        part("Nose", S("nose"), COL["nose"]),
        part("Camera head", S("camera"), COL["camera"]),
        part("Spacer ring and grommet", S("cam_ring", "spg_grommet"), COL["ring"]),
        part("M4 screws", S("nose_screws"), COL["pins"]),
        part("Camera cable", win(S("cable"), xc + 40, D["x_tip"]), COL["cable"]),
        part("Water tube and bite valve", win(S("wtube", "bite"), xc + 40, D["x_tip"] + 1), COL["wtube"])],
        OUT / "joint-03.png", "Joint 3: nose on the collar spigot, camera clamped against the lip",
        subtitle="Cut on the vertical centre plane. The spacer ring pushes the camera onto the 26 mm lip; three M4 screws hold the nose",
        cut="+Y", elev=8, azim=-80, size=(8, 6)))
    # 04 water path at the head (from above)
    out.append(bv.joint([
        part("Collar", win(S("collar"), xc + 50, D["x_tip"] + 1), COL["collar"]),
        part("Nose", S("nose"), COL["nose"]),
        part("Water tube in the 45 degree exit and top groove", win(S("wtube"), xc + 50, D["x_tip"] + 1), COL["wtube"]),
        part("Bite valve in its pocket", S("bite"), COL["bite"])],
        OUT / "joint-04.png", "Joint 4: water tube out of the collar, along the groove, into the bite valve pocket",
        subtitle="Seen from above and in front. The tube lies flush in a 4.5 mm groove; the valve presses into an 11.5 mm pocket",
        elev=50, azim=-30, size=(8, 6)))
    # 05 speaker pocket and outlets
    out.append(bv.joint([
        part("Collar, outlets and speaker pocket", win(S("collar"), xc + 30, xc + 110), COL["collar"]),
        part("Speaker (20 mm, IP67)", S("speaker"), COL["speaker"]),
        part("Perforated cover, bonded", S("spk_cover"), COL["cover"])],
        OUT / "joint-05.png", "Joint 5: speaker in its pocket on the collar",
        subtitle="Seen from the speaker side. Flat pocket floor; cover flush below the 48 mm outline; outlets at 45 deg either side",
        elev=10, azim=-100, size=(8, 6)))
    # 06 tail cap cut open
    out.append(bv.joint([
        part("Section 4 (back end)", win(S("rod4"), -5, 130), COL["rod"]),
        part("Tail cap", S("tailcap"), COL["tailcap"]),
        part("Air barb", S("barb"), COL["barb"]),
        part("Grommets", S("tc_grommets"), COL["grommet"]),
        part("Pins", S("tc_pins"), COL["pins"]),
        part("Grip", win(S("grip"), -5, 130), COL["grip"]),
        part("Cable and guide tube", win(S("cable", "guide"), -60, 130), COL["cable"])],
        OUT / "joint-06.png", "Joint 6: tail cap bonded and pinned in section 4",
        subtitle="Cut on the vertical centre plane. Air enters by the barb; cable and guide slide through split grommets",
        cut="+Y", elev=15, azim=-65, size=(8, 6)))
    # 07 inside the base
    out.append(bv.joint([
        part("Case base", S("case"), COL["case"]),
        part("Equipment plate on 6 mm spacers", S("eplate", "espacers"), COL["eplate"]),
        part("Battery (strapped)", S("battery"), COL["battery"]),
        part("Blower on standoffs", S("blower", "blower_legs"), COL["blower"]),
        part("Control modules", S("modules"), COL["modules"]),
        part("Flow meter on its bracket", S("flowmeter", "fm_bracket"), COL["flowmeter"]),
        part("Wall fittings", S("fittings"), COL["fittings"]),
        part("Intake filter", S("filter"), COL["filter"])],
        OUT / "joint-07.png", "Joint 7: inside the surface unit base",
        subtitle="Seen from above, lid not shown. Everything stands on the plate; the tallest part is 19 mm below the rim",
        elev=55, azim=-60, size=(8, 6)))
    # 08 monitor in the lid
    out.append(bv.joint([
        part("Lid (open)", S("lid"), COL["lid"]),
        part("Monitor bracket", S("dbracket"), COL["dbracket"]),
        part("Monitor with recorder", S("monitor"), COL["monitor"])],
        OUT / "joint-08.png", "Joint 8: monitor on its bracket in the lid",
        subtitle="Seen from the operator's side. Bracket feet bolted through the lid with sealing washers",
        elev=15, azim=-160, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []
    xc = D["x_collar"]

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
    j = sec_x(2)[1]
    w2 = lambda k_: win(S(k_), j - 300, j + 70)  # noqa: E731
    st(1, [part("Section 2 (front end)", w2("rod2"), COL["rod"])],
       [part("Coupler with snap button", win(S("coupler2", "button2", "spring2"), j - 300, j + 70), COL["coupler"], (160, 0, 0)),
        part("Pins, after drilling", win(S("pins2"), j - 100, j), COL["pins"], (0, 0, 60))],
       "coupler into each section (do this four times)",
       "Epoxy on the plain end; push it 60 mm in, button on the button line; drill and pin top and bottom; cure 24 h",
       elev=20, azim=-60)
    st(2, [part("Section 4 (back end)", win(S("rod4"), -5, 400), COL["rod"])],
       [part("Tail cap with barb and grommets", S("tailcap", "barb", "tc_grommets"), COL["tailcap"], (-150, 0, 0)),
        part("Pins", S("tc_pins"), COL["pins"], (0, 0, 60))],
       "tail cap into section 4", "Epoxy on the plug; push it home against the flange, barb away from the button line; drill and pin",
       elev=20, azim=-60)
    st(3, [part("Section 4 with tail cap", win(S("rod4", "tailcap", "barb"), -5, 600), COL["rod"])],
       [part("Grip", S("grip"), COL["grip"], (500, 0, 0))],
       "grip onto section 4", "Wet the inside with soapy water; slide it on from the front end until it is 10 mm from the flange",
       elev=20, azim=-60)
    st(4, [part("Collar", S("collar"), COL["collar"])],
       [part("Speaker, leads through the wire hole", S("speaker"), COL["speaker"], (0, -50, 0)),
        part("Perforated cover", S("spk_cover"), COL["cover"], (0, -90, 0))],
       "speaker into the collar", "Neutral-cure silicone on the pocket floor; leads into the plenum; cover bonded flush",
       elev=15, azim=-110)
    st(5, [part("Section 4 with tail cap and grip (sections 3, 2, 1 beyond)", win(S("rod4", "tailcap", "grip", "barb", "tc_grommets"), -5, 700), COL["rod"])],
       [part("Camera cable", win(S("cable"), -150, 700), COL["cable"], (-400, 0, 0)), part("Guide tube", win(S("guide"), -150, 700), "#9CA3AF", (-400, 0, 0))],
       "thread the cable and guide tube through every section",
       "From the tail cap end, through both grommets and on through sections 4, 3, 2 and 1; 1 m of each left out at the front. Lines drawn cut short",
       elev=20, azim=-60)
    st(6, [part("Collar", S("collar", "speaker", "spk_cover"), COL["collar"])],
       [part("Guide tube end", win(S("guide"), xc - 200, xc + 80), "#9CA3AF", (-120, 0, 0)),
        part("Cable through the spigot grommet", win(S("cable", "spg_grommet"), xc - 200, D["x_nose"] + 20), COL["cable"], (-120, 0, 0))],
       "cable and guide into the collar",
       "Guide 6 mm into the plenum; cable through the grommet; solder to the camera pigtail and speaker leads, heat-shrink",
       elev=20, azim=-60)
    st(7, [part("Collar", S("collar", "spg_grommet"), COL["collar"])],
       [part("Spacer ring", S("cam_ring"), COL["ring"], (60, 0, 0)), part("Camera head", S("camera"), COL["camera"], (120, 0, 0)),
        part("Nose", S("nose"), COL["nose"], (220, 0, 0)), part("M4 screws (3)", S("nose_screws"), COL["pins"], (220, 0, 0))],
       "camera and nose onto the collar",
       "Camera into the nose from behind, LEDs against the lip; ring next; nose over the spigot; three M4 screws, threadlocker",
       elev=20, azim=-60)
    head = S("collar", "nose", "camera", "speaker", "spk_cover", "nose_screws")
    st(8, [part("Head", head, COL["collar"])],
       [part("Section 1 with coupler", win(S("rod1", "coupler1", "button1"), xc - 400, xc + 70), COL["rod"], (-150, 0, 0))],
       "section 1 into the collar",
       "Press the button, slide the coupler home until the tube butts the collar, and the button clicks into the spotface",
       elev=20, azim=-60)
    j1 = sec_x(1)[0]
    st(9, [part("Section 1 (back end) and the head beyond", win(S("rod1", "cable", "guide"), j1 - 5, j1 + 500), COL["rod"])],
       [part("Section 2 with its coupler (front end shown)", win(S("rod2", "coupler2", "button2"), j1 - 500, j1 + 70), COL["coupler"], (-250, 0, 0))],
       "join sections 2, 3 and 4",
       "The same at each joint: slide the section along the lines, press its button, push home until it clicks and the tube ends butt",
       elev=20, azim=-60)
    st(10, [part("Head", head, COL["collar"])],
       [part("Water tube (single use), through the guide", win(S("wtube"), xc - 150, D["x_tip"]), COL["wtube"], (-80, 0, 0)),
        part("Bite valve", S("bite"), COL["bite"], (0, 0, 40))],
       "water tube through the guide and into the bite valve pocket",
       "Push it in from the surface end until it shows at the exit; lay it in the groove; fit the valve and press it into the pocket",
       elev=35, azim=-50)
    st(11, [part("Case base", S("case"), COL["case"])],
       [part("Equipment plate on spacers", S("eplate", "espacers"), COL["eplate"], (0, 0, 150))],
       "equipment plate into the case", "Four M5 screws up through the floor with bonded sealing washers, 6 mm spacers, nyloc nuts on top",
       elev=40, azim=-60)
    st(12, [part("Case and plate", S("case", "eplate", "espacers"), COL["case"])],
       [part("Battery and strap", S("battery"), COL["battery"], (0, 0, 160)), part("Blower", S("blower", "blower_legs"), COL["blower"], (0, 0, 160)),
        part("Control modules", S("modules"), COL["modules"], (0, 0, 160)), part("Flow meter and bracket", S("flowmeter", "fm_bracket"), COL["flowmeter"], (0, 0, 200))],
       "battery, blower, modules and flow meter onto the plate", "Wire as the wiring picture shows; battery lead unplugged and fuse out",
       elev=45, azim=-60, label_done=False)
    st(13, [part("Case with everything on the plate", S("case", "eplate", "battery", "blower", "modules", "flowmeter", "fm_bracket"), COL["case"])],
       [part("Camera socket, headset socket, air outlet", S("fittings"), COL["fittings"], (0, 80, 0)), part("Intake filter", S("filter"), COL["filter"], (0, -100, 0))],
       "wall fittings and intake filter", "Each through its hole with its seal outside and nut inside; hoses from filter to blower to meter to outlet",
       elev=30, azim=-60, label_done=False)
    st(14, [part("Lid", S("lid"), COL["lid"])],
       [part("Monitor bracket", S("dbracket"), COL["dbracket"], (-40, 0, 0)), part("Monitor", S("monitor"), COL["monitor"], (-100, 0, 0))],
       "monitor and bracket into the lid", "Bracket feet through the lid on four M5 screws with sealing washers; monitor on its rear M4 holes",
       elev=15, azim=-160)
    allp = [k for k in C if k not in ("stand", "bottle")]
    st(15, [part("Probe and surface unit", S(*allp), "#D1D5DB")],
       [part("Reservoir stand", S("stand"), COL["stand"], (300, 0, 0)), part("Water bottle", S("bottle"), COL["bottle"], (300, 0, 300))],
       "set up at the hole: stand, bottle, hose and plugs",
       "Bottle at most 1 m above the tip; water set to the guide; air hose to the barb; cable plug in; then the safety stops",
       elev=24, azim=-58, size=(10, 6), label_done=False)
    return out


# ----------------------------------------------------------------- wiring and lines
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    INK, MUT = "#111827", "#4B5563"
    RED, BLU, GRY, AIR, WAT = "#B91C1C", "#1D4ED8", "#6B7280", "#0F766E", "#2563EB"
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    fig.text(0.02, 0.975, "VoidScope: wiring, air line and water line (block level)", fontsize=11, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.94, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT. All circuits are extra-low voltage: 12.8 V nominal, 14.6 V at most.",
             fontsize=8, color="#B45309", va="top")

    def blk(x, y, w, h, title, sub, col):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=col, lw=1.6))
        ax.text(x + w / 2, y + h - 1.6, title, ha="center", va="top", fontsize=8, fontweight="bold", color=INK)
        if sub:
            ax.text(x + w / 2, y + h - 4.6, sub, ha="center", va="top", fontsize=6.8, color=MUT, linespacing=1.25)

    def wire(pts, col, lw=1.8):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=lw, solid_capstyle="round")

    def lab(x, y, t, col, ha="left"):
        ax.text(x, y, t, fontsize=6.6, color=col, ha=ha, va="center")
    ax.add_patch(FancyBboxPatch((2, 6), 66, 52, boxstyle="round,pad=0.4", fc="#FFFBEB", ec="#F59E0B", lw=1.2))
    ax.text(4, 56.5, "Surface unit case", fontsize=8, fontweight="bold", color="#B45309")
    blk(5, 38, 14, 12, "Battery pack", "12.8 V 6 Ah LiFePO4\nbuilt-in BMS, XT60", "#C2410C")
    blk(24, 40, 13, 10, "Fuse and switch", "7.5 A blade fuse,\nlit main switch", RED)
    blk(42, 40, 12, 10, "12 V converter", "buck-boost, 3 A", "#16A34A")
    blk(42, 24, 12, 10, "Blower speed", "PWM controller\nwith knob", "#16A34A")
    blk(24, 24, 13, 10, "Blower", "0.9 kPa at most\n(shut-off)", "#334155")
    blk(5, 22, 14, 12, "Intake filter", "fine dust, on the\nwall away from void", GRY)
    blk(24, 9, 13, 10, "Flow meter", "5 to 50 L/min,\nset 20 to 40", AIR)
    blk(42, 9, 12, 10, "Air outlet", "bulkhead barb\n12 mm", AIR)
    blk(57, 40, 9, 10, "Monitor", "7 in AHD\nrecorder", "#1E293B")
    blk(57, 24, 9, 10, "Talk amp", "push-to-talk,\nrelay", "#7C3AED")
    blk(57, 9, 9, 10, "Sockets", "camera GX16,\nheadset", INK)
    ax.add_patch(FancyBboxPatch((76, 6), 40, 52, boxstyle="round,pad=0.4", fc="#F9FAFB", ec=GRY, lw=1.2))
    ax.text(78, 56.5, "Probe (rod bore is the air duct)", fontsize=8, fontweight="bold", color=MUT)
    blk(79, 40, 15, 10, "Camera head", "AHD 1080p, 12 LEDs,\nIP68, 12 V", "#1F2937")
    blk(98, 40, 15, 10, "Speaker", "20 mm IP67, also\nthe microphone", "#374151")
    blk(79, 22, 15, 10, "Tail cap barb", "air in", AIR)
    blk(98, 22, 15, 10, "Six outlets", "at the collar,\n2.8 m/s at 20 L/min", AIR)
    blk(79, 9, 15, 9, "Guide tube", "PTFE 8 x 6", GRY)
    blk(98, 9, 15, 9, "Bite valve", "flows only when\nbitten", WAT)
    wire([(19, 45), (24, 45)], RED); lab(19.5, 47, "1.0 mm²", RED)
    wire([(37, 45), (42, 45)], RED); lab(37.5, 47, "1.0 mm²", RED)
    wire([(54, 45), (57, 45)], RED); lab(54.2, 47.5, "12 V", RED)
    wire([(30.5, 40), (30.5, 37), (48, 37), (48, 34)], RED); lab(40, 38.2, "0.75 mm²", RED)
    wire([(42, 29), (37, 29)], GRY, 1.2); lab(37.4, 31, "PWM", GRY)
    wire([(48, 40), (48, 37.5), (61.5, 37.5), (61.5, 34)], RED, 1.2)
    wire([(61.5, 24), (61.5, 19)], "#7C3AED", 1.2); lab(62, 21.5, "speaker pair", "#7C3AED")
    wire([(66, 14), (76, 14), (76, 45), (79, 45)], RED); lab(78, 3.2, "hybrid cable 7 m (red and purple lines): coax video, 12 V, ground, speaker pair", RED)
    wire([(66, 12.5), (77.5, 12.5), (77.5, 53), (105.5, 53), (105.5, 50)], "#7C3AED", 1.2); lab(88, 54.5, "speaker pair in the same cable", "#7C3AED")
    wire([(61.5, 50), (61.5, 53), (70, 53), (70, 16)], BLU, 1.0); lab(70.5, 34, "video\nto monitor", BLU)
    wire([(19, 28), (24, 28)], AIR, 3); lab(19.2, 30.5, "air", AIR)
    wire([(30.5, 24), (30.5, 19)], AIR, 3)
    wire([(37, 14), (42, 14)], AIR, 3)
    wire([(54, 12), (56, 12), (56, 4), (72, 4), (72, 27), (79, 27)], AIR, 3); lab(57, 2.4, "air hose 12 mm, 2.5 m", AIR)
    wire([(94, 27), (98, 27)], AIR, 3); lab(94.3, 29.5, "rod bore", AIR)
    ax.text(97, 64, "Water line (no electrics):", fontsize=7.5, fontweight="bold", color=WAT, ha="center")
    ax.text(97, 61, "bottle, at most 1 m above the tip  >  stopcock (priming)  >  strainer  >  600 mm capillary", fontsize=6.8, color=WAT, ha="center")
    ax.text(97, 59, ">  roller clamp  >  4 x 2.5 mm tube inside the guide  >  bite valve", fontsize=6.8, color=WAT, ha="center")
    wire([(94, 13.5), (98, 13.5)], WAT, 2.4)
    ax.text(4, 64, "Safety: battery lead and fuse out until the stop points in section 6 of the plan are passed.", fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(4, 61, "Red: power. Blue: video. Purple: speaker. Teal: air. The charger is used only away from the kit, on a bench.", fontsize=7.0, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
