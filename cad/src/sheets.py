"""VoidScope general arrangement sheet VDS-DWG-001, Rev P3 (TRL 3; constructable design VDS-DDR-002 with the
steerable camera tip of VDS-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/VDS-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is VDS-DWG-010; the making sketches are VDS-DWG-101 onward.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, build_components, derived, HEAD_KEYS  # noqa: E402

DATE = "2026-10-03"


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]
    tw, th = dims["top"]
    rw, rh = dims["right"]
    k = sheet.scale
    dl = 11
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    C = build_components(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(C=C)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="VoidScope", title="Rubble void search probe and surface unit: general arrangement",
              dwg_no="VDS-DWG-001", rev="P3", author="Amish Chadha", date=DATE, scale=1 / 25, theme="technical",
              material="6061-T6 aluminium tube and bar; bought parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "VDS-DDR-002: design for construction", DATE, "AC"),
                         ("P3", "VDS-DDR-003: steerable camera tip and steering control", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    zc = P["z_axis"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k   # noqa: E731
    Zf = lambda mz: y + h - (mz - bb.min.Z) * k   # noqa: E731
    s._dim(X(0), Zf(zc), X(D["length"]), Zf(zc), f"{D['length']:,.0f} PROBE", "above", off=34)
    s._dim(X(D["ctrl_x"][1]), Zf(zc), X(D["length"]), Zf(zc), f"{D['working_length']:,.0f} INTO THE VOID", "below", off=6)
    L += leader(X(D["x_tip"] - 60), Zf(zc), X(D["x_tip"] - 260), Zf(zc + 260), "HEAD AND STEERABLE TIP, 48 OD; SEE DETAIL A", "end")
    L += leader(X(D["ctrl_x"][0] + 30), Zf(zc + 60), X(-60), Zf(zc + 200), "STEERING CONTROL (34)", "start")
    xs = [X(a) for a, _ in D["sections"]]
    for i, xa in enumerate(xs):
        L.append(_t(xa + 1050 * k / 2, Zf(zc) - 2.5, f"SECTION {4 - i} (5)", 1.9, 400, MUTED, "middle"))
    L += leader(X(D["case_x"][1] - 60), Zf(100), X(2000), Zf(300), "SURFACE UNIT (14 TO 23), LID OPEN")
    L += leader(X(P["stand"][0] + 60), Zf(1300), X(2000), Zf(1180), "RESERVOIR STAND (13) AND BOTTLE (12)")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k   # noqa: E731
    Yt = lambda my: y + h - (my - bb.min.Y) * k   # noqa: E731
    L += leader(Xt(25 + 30), Yt(0), Xt(-60), Yt(160), "TAIL CAP AND AIR INLET (7); GRIP (8)", "start")
    L.append(_t(Xt(2600), Yt(-450), "OPERATOR STANDS BEHIND THE TAIL CAP (-X); TIP POINTS +X", 1.9, 400, MUTED, "middle"))

    s._layers += L
    s.add_svg(views["iso"], 276, 37, 140, 50, label="Isometric view", sublabel="Not to scale")
    # Detail A: the head at 1:2
    from build123d import Compound
    hv = safe_project_views(Compound([C[k_].shape for k_ in HEAD_KEYS]), work / "head", names=("top",))
    s.add_svg(hv["top"], 276, 102, 140, 30, scale=0.4, label="Detail A: head and steerable tip",
              sublabel="Scale 1:2.5; plan from above, tip to the right, straight; bends 90 deg each way in this plane")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Probe {D['length']:,.0f} long; working length {D['working_length']:,.0f}; axis {zc:.0f} above ground as held",
        f"Rod: 4 sections 38.1 x 1.47 6061-T6 tube, {P['rod'][2]:,.0f} long",
        f"Couplers 34.93 x 2.11 x {P['coupler'][2]:.0f}, {P['coupler'][3]:.0f} bonded and pinned; snap button",
        "Head 48 OD at most, tip straight; passes a 51 mm core hole (R1)",
        "Collar: socket, plenum, 6 x 5 outlets, speaker, water exit",
        "Nose: base link 6.5 below the axis; bite valve on top",
        f"Tip: 5 joints, 90 deg each way; {D['tip_len']:.0f} long; 29 mm IP68 camera",
        "Steering: lever and drum on section 4, two wires in housings",
        "Air: rod bore is the duct; inlet barb on the tail cap",
        "Water: 4 x 2.5 tube inside an 8 x 6 PTFE guide",
        f"Case {P['case'][0]:.0f} x {P['case'][1]:.0f} x {P['case'][2] + P['case'][3]:.0f}; lid opened {P['lid_open']:.0f} deg",
        "Third-angle; front view from -Y; (n) = BOM line",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "VDS-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
