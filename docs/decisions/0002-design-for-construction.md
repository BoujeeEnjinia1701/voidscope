---
doc_id: VDS-DDR-002
title: VoidScope design for construction
project: VoidScope
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Changes that make the TRL 2 concept physically buildable, with the reason for each; decided under Amish's 2026-10-03 pre-approval"
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

STANDARDS section 18 asks for the design to be made constructable while the build plan is written: every part made by a stated process and fixed to its neighbours (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept (VDS-PRC-001 v0.2, VDS-DDR-001) said what each part does but not how the rod sections join, how the lines cross the joints, how the head holds the camera, the bite valve and the speaker inside 50 mm, or how the surface unit is laid out. The changes below answer those questions. A first build123d check of the model found three more problems (P12 to P14), fixed the same way.

The changes keep what VoidScope does: the same reach, envelope, camera, water and air paths, audio, battery and safety stops. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which runs 106 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, slide fits have their clearance, and parts that must stay apart do. All 106 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | The concept had | The constructable design has | Why |
| --- | --- | --- | --- |
| P1 | A rigid rod "about 50 mm" in about 1 m sections, joints not defined | 38.1 x 1.47 mm (1.5 x 0.058 in) 6061-T6 tube in four 1,050 mm sections; 34.93 x 2.11 mm couplers, 120 mm long, 60 mm bonded and pinned into each front end | These two stock tube sizes telescope with 0.11 mm a side, so the coupler slides in by hand and no turning is needed; the 38.1 mm rod leaves room for a 48 mm head |
| P2 | No joint lock | A bought V-spring snap button in each coupler, through an 8.5 mm hole in the next section | Locks push, pull and twist; one press to undo; the spring strip lies across the bore and leaves room above and below for the lines (3.0 and 2.0 mm clear) |
| P3 | Lines with connectors at each joint | Cable and guide tube left threaded through all sections and the tail cap; sections slide along them for storage | No connectors inside the rod; setup is four clicks (R9) |
| P4 | A separate air line | The rod bore is the air duct, sealed at the tail cap and the head; the joints need no seals | 10 Pa loss instead of about 460 Pa in a 9 mm line; each joint leaks about 0.08 L/min |
| P5 | Water line inside the rod, not replaceable | A PTFE 8 x 6 mm guide tube in the rod; the single-use 4 x 2.5 mm water tube pushes through it | The water set is changed in about 4 minutes without tools (R10) |
| P6 | A one-piece sealed head | A turned collar (socket, plenum, six outlets, speaker pocket, 45° water exit, spigot) and a turned nose (camera bore, lip, bite valve pocket), joined by three M4 screws | Each part can be turned on a small lathe; the camera can be changed |
| P7 | Camera on the axis | Camera bore 6.5 mm below the axis | Makes room on top for an 11.5 mm bite valve pocket inside the 48 mm outline, with 2.85 mm minimum walls |
| P8 | A 28 mm speaker | A 20 mm IP67 speaker in a flat-floored pocket | A flat 28 mm part cannot sit under a 48 mm round outline; 20 mm fits with its cover flush |
| P9 | Button hole in the collar like the rods | The same 8.5 mm hole with a 14 mm spotface | The collar wall is 6.4 mm thick; the spotface lets a fingertip reach the button |
| P10 | A handheld display | Monitor with recorder in the lid of the surface unit, on a folded bracket | One battery and one cable; the crew's hands are on the rod |
| P11 | Surface unit not laid out | Equipment plate on four 6 mm spacers, screwed through the floor with bonded sealing washers; flow meter upright on an angle bracket; wall fittings on the side toward the probe; intake filter on the far side | The case stays sealed; a variable-area flow meter only reads upright; the tallest part is 19 mm below the rim so the lid closes |
| P12 | Tail cap 38.1 mm with a 25 mm bore (found by the check) | 44 mm flange and a 30 mm bore | The lines overlapped the 25 mm bore; the 44 mm flange gives 7 mm of wall for the 1/4 BSP barb thread and is still under the 48 mm head |
| P13 | Water groove floor 19.5 mm above the axis (found by the check) | Floor 20.0 mm | The tube overlapped the 40 mm spigot under the nose; now it rests on it and stays flush with the 48 mm outline |
| P14 | Bite valve pocket 45 mm long; reservoir stand beside the case (found by the check) | Pocket 50 mm; stand 450 mm further out | The tube's bend down into the valve hit the groove floor; a stand leg crossed the open case |

*Table 2. Parts added to the model and the BOM.*

| Added | BOM line |
| --- | --- |
| Couplers, snap buttons and pins | 6 |
| Tail cap, air barb and grommets | 7 |
| Water guide tube | 10 |
| Camera spacer ring and spigot grommet | 1, 3 |
| Equipment plate, spacers and sealing washers | 15 |
| Monitor bracket | 16 |
| Flow meter bracket | 20 |
| Lathe time allowance | 29 |

## Consequences

- The calculations (VDS-CAL-001 v0.1) are made on the constructable design; nothing in them was computed on the concept.
- Drawing VDS-DWG-001 is at Rev P2; making sketches VDS-DWG-101 to 109 are new; the concept media are regenerated from the model.
- Estimated cost USD 1,578 against the USD 2,000 value-engineering target, USD 422 under it.
- `project.yaml`: `design_state: constructable`.
- What remains to confirm with real parts is listed in VDS-DEC-001, "To confirm when parts are bought".
