# Review note: VoidScope

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (VDS-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (VDS-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (VDS-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## Session 2026-10-03: TRL 2 (populate)

Run as the first half of `/to-trl3` under Amish's instruction of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Kit 1.7.0 installed first (`.kit/`, `.claude/commands/`, root `CLAUDE.md`; `.kit/PHASE.yaml` as installed). No commit or push, by instruction.

### What was done

- VDS-PRB-001 v0.2: constraints tied to the requirements; co-design checklist; first co-design candidate named; the v0.1 open questions answered by the TRL 2 decisions.
- VDS-PRC-001 v0.2: how it works, components, key design choices with first-order numbers, safety section.
- VDS-REQ-001 v0.2: R2 split into straight reach (R2) and bends (R11); R5 restated as a drip ceiling with a bite valve; R6 adds a blocked-tip limit; R8 worded as a value-engineering target; R12 two-way voice added.
- Concept media: because the whole TRL 3 path ran in one session, the massing model was taken straight into the constructable model, and every concept picture was generated from that (see the TRL 3 section).

### Key results at TRL 2 (first-order, superseded by VDS-CAL-001)

- Lines inside the rod fit with room to spare once the rod bore carries the air; a separate 9 mm air line would have lost about 0.46 kPa at 20 L/min, more than a pressure-limited blower can give.
- A fixed capillary is the simplest way to cap a gravity drip whatever the bottle height; an open 2.5 mm tube alone would pass about 70 mL/min at 1 m.
- A rigid rod cannot meet the TRL 1 verification of "a test channel with two 45° bends"; that part of R2 became R11.

### Decisions made under Amish's pre-approval (VDS-DDR-001)

D1 to D13, each with options and the reason, in `docs/decisions/0001-trl2-review-decisions.md`: lines inside with the bore as the air duct; 38.1 mm aluminium sections with snap buttons, tent-pole storage; no articulation; bought IP68 camera head; monitor in the surface unit lid; tip speaker as speaker and microphone, fitted as standard; gravity drip with a capillary ceiling and a bite valve; blower chosen by its shut-off pressure; two LiFePO4 packs; independent of the tethered crawler block; requirements restated; budget, pitch and problem kept. Safety choices S1 to S6 taken on the conservative side, each with the evidence that would relax it. First co-design candidate to approach: the disaster management training school of the Armed Police Force, Nepal; second: Turkey's AFAD training centres (not contacted, not partners).

### Safety concerns

- Aspiration: water to a drowsy or badly lying survivor. Mitigated by the medical lead's direction, the bite valve (no flow unless bitten) and the capillary ceiling.
- Air: pressurising or dusting a void. Mitigated by a blower whose shut-off pressure is at most 1 kPa, an intake filter and a flow meter.
- Structure: the operator never enters the void; the probe is never a lever.
- Battery: LiFePO4 packs with built-in protection, charged away from the kit.

## Session 2026-10-03: TRL 3 (advance, constructable design and build plan)

The second half of `/to-trl3`: `/advance-trl3` including `/build-plan` steps 1 to 4, with every decision recorded as made under Amish's pre-approval quoted above. TRL cap respected: no hardware, test plans, firmware, PCB layouts, purchasing lists or build-log entries. No commit or push.

### What was done

- `cad/src/model.py`: parametric build123d model of the whole kit as deployed (probe, surface unit, reservoir stand), built from components with every fixing, and 106 constructability checks (`python cad/src/model.py --check`). All 106 pass. STEP and STL in `cad/step/` and `cad/stl/` (assembly, probe, head, surface unit).
- `docs/04-calcs/sizing.py` and `docs/04-calcs/01-sizing.md` (VDS-CAL-001 v0.1): envelope and reach, rod structure and handling, vision, water, air, power, robustness, deployment, mass and cost; `results.csv`.
- `cad/src/sheets.py`: general arrangement VDS-DWG-001 at Rev P2 (P1 preliminary GA, P2 design for construction), with a 1:2 detail of the head.
- `bom/bom.csv`: 29 lines, every one priced, with a supplier type.
- `cad/src/concept_media.py`: hero (1.75 m figure standing where the operator stands), head cutaway, exploded view, air and water flow diagram, blueprint VDS-DWG-010 Rev P2, `model.glb` (1.2 MB, exported at 1.0 mm linear and 0.35 rad angular deflection) and `viewer.html`.
- `docs/decisions/0002-design-for-construction.md` (VDS-DDR-002): fourteen changes, P1 to P14, with reasons.
- `cad/src/build_plan_media.py`: overview, nine making sketches VDS-DWG-101 to 109, eight joint close-ups, fifteen step pictures and the wiring and lines diagram.
- `docs/05-build-plan.md` (VDS-BLD-001 v0.1) and `docs/06-design-decisions.md` (VDS-DEC-001 v0.1).
- `cad/src/product_model.py`: appearance model with `product_parts()`, `TITLE` and `RENDER_VIEWS` (hero, exploded, detail); render scenes exported to `/home/claude/renders/voidscope` for the photoreal renders on Amish's Mac.
- VDS-PRB-001 v0.3, VDS-PRC-001 v0.3, VDS-REQ-001 v0.3; `project.yaml` at TRL 3 with `design_state: constructable` and the evidence list; README with the render hero, links line and a "Building the prototype" section.

### Key results (VDS-CAL-001)

- Envelope 48 mm (head) in a 51 mm core hole; probe 4,398 mm; working length 4,063 mm.
- Probe 3.66 kg; surface unit about 6.2 kg with one pack.
- Rod buckling 1,001 N (5 times a 200 N push); 2.55 on yield at a button hole with 3 m unsupported in a void; tip droop 15 mm at 2 m.
- Vision: 19 pixels across a 20 mm letter at 1 m; 7 lx after 2 m of heavy dust.
- Water ceiling 1.47 mL/min at 1 m and 20 °C; never more than 4.51 mL/min (2 m, 40 °C).
- Air: 0.38 kPa loss at 20 L/min, 44 L/min at full speed, 0.9 kPa with the tip blocked.
- Battery: 6.2 h at 20 °C and 4.3 h at -10 °C of video and light on one pack.
- Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,578 (USD 422 under the target); USD 1,398 for a builder with a lathe.

### Requirements not met

- **R11, two 45° bends:** not met. The rigid rod goes straight only. A flexible lead section between section 1 and the head is a later version (recorded as decided, not redesigned at TRL 3).
- R9 (3 min setup) is an estimate, 2.1 min, that only a timed drill can settle. R3, R4, R10 and R12 are met on paper or by design and need TRL 4 tests.

### Decisions made under the pre-approval

- VDS-DDR-001 (TRL 2 review, D1 to D13 and S1 to S6) and VDS-DDR-002 (design for construction, P1 to P14), indexed in VDS-DEC-001. Open decisions: none. Nine items are listed in VDS-DEC-001 to confirm when parts are bought (camera size and rating, blower shut-off pressure, flow meter drop, snap button strength, tube telescoping fit, capillary flow, bite valve, speaker, cable, case, monitor and battery sizes).
- Appearance model departures from `model.py`, accepted under the same pre-approval: painted depth bands every 100 mm, a screen face on the monitor, LED dots and a lens on the camera face, the hose, cable and water tube drawn from the probe to the surface unit and bottle, a broken concrete wall with a 51 mm core hole, rubble and a standing 1.75 m mannequin. All main dimensions come from `model.py`.

### Build plan findings

- The concept said nothing about how the sections join; two stock tube sizes (1.5 x 0.058 in and 1.375 x 0.083 in) telescope with 0.11 mm a side and made the coupler a cut-to-length part, no turning.
- A flat 28 mm speaker cannot sit inside a 48 mm round outline; the 20 mm speaker fits with its cover flush.
- Putting the camera 6.5 mm below the axis made room for the bite valve pocket on top inside the 48 mm outline, with 2.85 mm minimum walls.
- The first model check found three clashes, each fixed: the lines against a 25 mm tail cap bore (now 30 mm with a 44 mm flange), the water tube 0.25 mm into the collar spigot (groove floor raised to 20 mm), and the tube's bend into the bite valve hitting the groove floor (pocket lengthened to 50 mm); a stand leg crossed the open case (stand moved).
- A variable-area flow meter reads only upright and must fit under the lid: it stands on a bracket at the end of the plate; the tallest part is 19 mm below the rim.
- With 3 m in the void and the tip unsupported, the operator must push down 34 N at the grip; in practice the tip must rest on debris beyond about 2 m. This is in the first checks.

### Safety concerns

- The water line is the main hazard: aspiration by a survivor who cannot drink safely. The bite valve, the capillary ceiling sized for twice the allowed height, the medical lead's direction and the rule never to connect a pump or pressurised container are the stops (build plan S5, S7).
- The blower's shut-off pressure is the only air pressure stop; it must be confirmed on the datasheet when bought and measured at a blocked tip before use (S4).
- Lathe work with an offset four-jaw set-up (nose, collar) and tube cutting (S1).
- LiFePO4 packs: fuse and lead out until the checks pass; charging away from the kit (S2, S3, S8).
- Structural: the operator stays outside the void; the probe is never a lever (S6).

### Kit notes (reported for the kit source, kit not edited)

- `.kit/concept.py` `cutaway_parts()` centres its cutting box on x = 0 and z = 0, so it removes nothing from parts far from the origin; `concept_media.py` moves the head to the origin before cutting.
- `.kit/concept.py` `export_web_model()` uses the default 0.001 mm glTF deflection and `Compound(children=...)`; `concept_media.py` calls `export_gltf` itself with `Compound([...])` and 1.0 mm and 0.35 rad deflection.

### Not done here

- Photoreal renders, captions, `media/render-*.png`, `media/card.png` and `media/social-preview.png`: made on Amish's Mac from the exported scenes. The README already leads with `media/render-hero.png`, so `render.py --check` warns until it exists.

### Recommended next step

The design looks ready for TRL 4: build the prototype to VDS-BLD-001 and run the first checks, starting with the parts in "To confirm when parts are bought", and approach the first co-design candidate so its medical lead can review the water line before any drill with a person at the tip. TRL 4 stays on hold under the portfolio cap until Amish lifts it.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
