"""VoidScope concept media from the TRL 3 parametric model (constructable design, VDS-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process. Geometry
comes from cad/src/model.py; the flow values come from VDS-CAL-001 (docs/04-calcs/sizing.py).
The pictures are made with the pieces of .kit/concept.py render_all, one at a time.

Axes: the probe lies along X at waist height with its tip toward +X; the surface unit stands on
the ground on the -Y side with its lid open toward the operator; the reservoir stand beside it.
The cutaway is of the head and the front of section 1 only, since the head is where the inside
matters (camera, air plenum, speaker, water exit and bite valve).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad/src"))
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
from model import PARAMS as P, build_components, build_parts, derived  # noqa: E402

PROJECT, TITLE, DWG, DATE = "VoidScope", "Rubble void search probe with water and air lines: concept", "VDS-DWG-010", "2026-10-03"
MD = ROOT / "media"


def parts(C=None):
    return [Part(name, shape, color, bom, explode) for name, shape, color, bom, explode in build_parts(C=C)]


def with_operator(ps):
    """The 1.75 m scale figure stands where the operator stands, behind the tail cap."""
    return ps + [K.human_figure(1750.0, x=-520.0, y=60.0, z=0.0)]


def hero():
    return K._render(with_operator(parts()), MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale, standing where the operator stands")


def cutaway():
    import build123d as b
    C = build_components()
    D = derived()
    x0, x1 = D["x_collar"] - 70, D["x_tip"] + 2
    zc = P["z_axis"]
    win = b.Pos((x0 + x1) / 2, 0, zc) * b.Box(x1 - x0, 80, 80)
    sel = [("Rod section 1 and coupler", ("rod1", "coupler1", "button1", "spring1"), "#D1D5DB"),
           ("Collar: socket, air plenum, outlets", ("collar", "spg_grommet"), "#6B7280"),
           ("Nose", ("nose", "nose_screws"), "#9CA3AF"), ("Camera head", ("camera", "cam_ring"), "#1F2937"),
           ("Camera cable", ("cable",), "#B45309"),
           ("Water guide", ("guide",), "#E5E7EB"), ("Water tube and bite valve", ("wtube", "bite"), "#2563EB")]
    ps = []
    for name, ks, col in sel:
        sh = None
        for k in ks:
            s = C[k].shape & win
            sh = s if sh is None else sh + s
        ps.append(Part(name, b.Pos(-(x0 + x1) / 2, 0, -zc) * sh, col))   # centred: the kit cutter is centred on x = z = 0
    ps = [p for p in K.cutaway_parts(ps, keep="+Y") if p.shape is not None and p.shape.volume > 1e-3]
    return K._render(ps, MD / "cutaway.png", azim=-90, elev=12,
                     title=f"{PROJECT}: cutaway of the head",
                     note="Head and front of section 1 cut on the vertical centre plane, near half removed (the speaker is on that half); seen from the -Y side, 12 deg elevation")


def exploded():
    return K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def web():
    import matplotlib.colors as mc
    from build123d import Color, Compound, export_gltf
    kids = []
    for p in parts():
        sh = p.shape
        sh.color = Color(*mc.to_rgb(p.color))
        sh.label = p.name
        kids.append(sh)
    MD.mkdir(parents=True, exist_ok=True)
    export_gltf(Compound(kids), str(MD / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
    # viewer page as written by .kit/concept.py export_web_model
    (MD / "viewer.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROJECT}: {TITLE}</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}}model-viewer{{width:100vw;height:100vh}}
.tag{{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="{PROJECT}: {TITLE}" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
    return MD / "model.glb"


def flow():
    import subprocess
    from PIL import Image
    r = {}
    res = subprocess.run([sys.executable, str(ROOT / "docs/04-calcs/sizing.py")], capture_output=True, text=True, cwd=ROOT).stdout
    for line in res.splitlines():
        if line.startswith("["):
            tag, rest = line[1:].split("]", 1)
            r[tag] = rest.rsplit(":", 1)[1].strip()
    tmp = MD / "_flow"
    tmp.mkdir(parents=True, exist_ok=True)
    a = K.flow_diagram(
        [("Clean air in through the intake filter", 20.0), ("Blower, 0.9 kPa at most", 20.0), ("Flow meter, set by the knob", 20.0),
         ("Hose and rod bore, 7 m", 20.0), ("Six outlets at the tip", 19.7)],
        tmp / "air.png", f"{PROJECT}: air path at the 20 L/min setting (estimates, VDS-CAL-001)", "L/min",
        [(3, "Coupler leaks, 4 joints (est.)", 0.3)])
    b = K.flow_diagram(
        [("1 L bottle, at most 1 m above the tip", "1 L"), ("Strainer and 600 mm capillary", f"{r['D3']} at 1 m, 20 C"),
         ("Roller clamp, 0 to open", "0 to ceiling"), ("Tube in the guide, 8 m", "39 mL primed"),
         ("Bite valve at the tip", "flows only when bitten")],
        tmp / "water.png", f"{PROJECT}: water path, gravity drip (estimates; never above {r['D2']} at 2 m and 40 C)", "")
    ia, ib = Image.open(a), Image.open(b)
    w = max(ia.width, ib.width)
    im = Image.new("RGB", (w, ia.height + ib.height), "white")
    im.paste(ia, (0, 0)); im.paste(ib, (0, ia.height))
    im.save(MD / "flow.png")
    shutil.rmtree(tmp, ignore_errors=True)
    return MD / "flow.png"


def blueprint():
    from build123d import Compound
    from drawing import Sheet, project_views
    D = derived()
    ps = parts()
    shown = with_operator(ps)
    views = project_views(Compound([p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound([p.shape for p in shown]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P2", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Massing model for concept communication",
              revisions=[("P1", "Concept sheet", DATE, "AC"), ("P2", "Redrawn from the constructable design (VDS-DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", [
        f"Probe {D['length'] / 1000:.2f} m long; {D['working_length'] / 1000:.2f} m working length",
        f"Head and rod {D['max_od']:.0f} mm at most; passes a 51 mm core hole",
        "Four 1,050 mm aluminium sections, snap-button joints",
        "Camera 1080p, IP68, 12 LEDs; two-way voice at the tip",
        "Air through the rod bore: 20 L/min set, 0.9 kPa at most",
        "Water by gravity drip and bite valve; 4.5 mL/min at most",
        "Battery 12.8 V 6 Ah LiFePO4, two packs; 4.3 h at -10 C",
        "Probe about 3.7 kg; surface unit about 6.2 kg (est.)"], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True); shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w]())
