---
doc_id: VDS-PRS-001
title: VoidScope product requirements and specifications
project: VoidScope
doc_type: Product requirements and specifications
version: "1.0"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "TRL 2: R2 split into reach (R2) and bends (R11); R5 restated as a ceiling with a bite valve; R6 adds the blocked-tip limit; R8 worded as a value-engineering target; R12 two-way voice added; concept status for each"
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: "TRL 3: status from VDS-CAL-001 on the constructable design (VDS-DDR-002)"
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: "R11 restated by Amish (decision 3A) as seeing around a 45-degree bend from a straight hole, with a test-box verification; met on paper by the steerable camera tip (VDS-DDR-003); status of R1, R2, R4, R8 and R9 updated from VDS-CAL-001 v0.2"
- version: "0.5"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Round-2 decision 3A (VDS-DDR-004): water offered with the tip steered aside; medical lead's confirmation in drills. Requirement wording unchanged"
- version: "1.0"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: migrated from REQ to PRS (PR-001 to PR-019, each traced to a user requirement in VDS-URS-001, old R numbers in the Was column); PR-014 (tip temperature) added by the STEM fix F1; PR-015 to PR-019 added for repair, mass, structure and publication; units and tolerance columns added"
---

# VoidScope product requirements and specifications

Sixteen of the nineteen product requirements are met on paper or by design by option A, the design of record with its steerable camera tip. The other three wait for tests: PR-006 (no flow unless bitten) needs the real bite valve, PR-007 (blocked-tip pressure) needs the real blower's shut-off pressure, and PR-010 (setup in 3 minutes) is estimated at 2.2 minutes and only timed drills can settle it. Targets are proposals for review with a co-design partner. The user needs behind them are in VDS-URS-001; the links to evidence are in the generated matrix `03b-traceability.md`. Method: STANDARDS section 22. Statuses are for option A; VDS-OPT-001 says how options B and C compare.

*Table 1. Product requirements and specifications. Tags in brackets refer to VDS-CAL-001 (docs/04-calcs/01-sizing.md).*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Physical architecture | Passes a core hole | The outer diameter of the tip, head and rod shall pass a standard 51 mm core hole along the full length, with the tip locked straight | 50 | max | mm | Analysis (VDS-CAL-001 A1: 48 mm at the head, 47 mm at the grip); pass the assembled probe through a 51 mm test ring at TRL 4 | Met on paper | R1 |
| PR-002 | UR-002 | Physical architecture | Reach | The probe shall reach at least 4 m along a straight path from the grip | 4000 | min | mm | Analysis (A4g: 4,203 mm; A4: 4,131 mm before the steering control reaches the hole). Beyond about 2 m in the void the tip must rest on debris: unsupported, the tip droops 39 mm at 2 m and the factor on yield at a button hole falls to 1.4 at 4.1 m (VDS-CAL-001 B); measure at TRL 4 | Met on paper | R2 |
| PR-003 | UR-003 | Performance | Vision in dark and dust | The camera shall give at least 10 pixels across a 20 mm letter at 1 m in a dark, dusty test box | 10 | min | px | Analysis (C2: 19.2 px; C6: 7 lx after 2 m of dusty air); dust test box at TRL 4 | Met on paper | R3 |
| PR-004 | UR-004 | Materials | Rubble handling | The head shall survive 20 drops of 1 m onto concrete and 30 minutes of immersion in 1 m of water | 20 | min | drops | Design (IP68 camera in an aluminium tip housing, G2: 2.85 mm minimum wall); drop and immersion tests at TRL 4, with the tip straight and bent | Met by design | R4 |
| PR-005 | UR-005 | Performance | Water ceiling | The water drip shall not exceed 5 mL/min at any allowed bottle height up to 2 m and any temperature up to 40 C | 5 | max | mL/min | Analysis (D1, D2: 1.2 mL/min at 1 m and 20 C, 4.4 mL/min at 2 m and 40 C with the bore 5 per cent oversize); timed collection at TRL 4 | Met on paper | R5 |
| PR-006 | UR-005 | Safety | No flow unless bitten | No water shall flow with the clamp closed or the bite valve not bitten, at up to 20 kPa of water head | 20 | min | kPa | Design (D7: 19.6 kPa at 2 m); valve cracking pressure and drill with the medical lead at TRL 4 | To verify at TRL 4 | R5 |
| PR-007 | UR-006 | Performance | Air flow and pressure | The air path shall deliver at least 20 L/min of filtered air at the tip and never more than 1 kPa above ambient, even with the tip blocked | 20 and 1 | min and max | L/min and kPa | Analysis (E3: 44 L/min at full speed; E5: 0.9 kPa at shut-off, to confirm: the blower runs from the converter's regulated output with a fixed speed cap, fix F5); flow meter and manometer at TRL 4 | To verify at TRL 4 | R6 |
| PR-008 | UR-007 | Electrical | Battery life | One pack shall run video and light for at least 4 h at 20 C and at -10 C | 4 | min | h | Analysis (F4: 6.2 h at 20 C, 4.35 h at -10 C); run-down tests at TRL 4 | Met on paper | R7 |
| PR-009 | UR-008, UR-015 | Physical architecture | Cost | The parts cost of the full kit shall stay at or below the value-engineering target | 2000 | max | USD | Analysis (bom/bom.csv: USD 1,780; I2, I4) | Met on paper | R8 |
| PR-010 | UR-009 | Usability | Setup time | Two trained people shall assemble the kit and start searching within 3 minutes | 3 | max | min | Estimate (H6: 2.2 min); timed drills with a USAR partner at TRL 4 | To verify at TRL 4 | R9 |
| PR-011 | UR-010 | Usability | Water path change | The water path parts shall be replaceable in under 5 minutes without tools | 5 | max | min | Design (D8: about 4 min, single-use water set); timed replacement at TRL 4 | Met by design | R10 |
| PR-012 | UR-011 | Performance | Look round a 45-degree bend | With the probe pushed straight through a 51 mm hole, the camera tip shall steer to look down a passage that turns 45 degrees either side and read 20 mm letters 1 m down it | 45 | min | deg | Analysis (J3: 90 degrees each way; J6: 83 mm to the side; C2: 19 px); test box at TRL 4 | Met on paper | R11 |
| PR-013 | UR-012 | Electrical | Two-way voice | The tip speaker and the operator headset shall give two-way speech between the operator and a person at the tip | 1 | min | channel | Design (tip speaker used as speaker and microphone, push-to-talk headset); speech test in a rubble box at TRL 4 | Met by design | R12 |
| PR-014 | UR-013 | Safety | Tip surface temperature | The tip housing surface shall not exceed 48 C (10 minute touch of bare metal) at 35 C ambient with the camera and dimmed LEDs running; above 35 C ambient the tip is kept off the survivor | 48 | max | C | Analysis (K5: 44.4 C at 35 C, 53.9 C at 45 C, STM S14, fix F1); thermocouple on the tip housing at TRL 4 | Met on paper | New (STM S14) |
| PR-015 | UR-014 | Materials | Commodity parts and hand tools | The made parts shall be cut from stock sizes with hand tools and a lathe, and the printed parts shall be printable on a basic printer | 1 | min | outside lathe job | Design (build plan VDS-BLD-001, outside lathe allowance in BOM line 29); build at TRL 4 | Met by design | New |
| PR-016 | UR-009 | Packaging and transport | Carried load | Each carried load (probe and rod case, surface unit) shall not exceed what one person carries | 15 | max | kg | Analysis (B5: probe 4.18 kg; I1: surface unit 6.2 kg); weigh at TRL 4 | Met on paper | New |
| PR-017 | UR-004, UR-002 | Physical architecture | Rod structure | The rod shall not buckle under a 200 N two-handed push, and a button hole shall keep a factor of 2 on yield with 3 m unsupported in a void | 200 and 2 | min | N and factor | Analysis (B12: 940 N; B11: 2.33; STM S1, S3); load test at TRL 4 | Met on paper | New (STM) |
| PR-018 | UR-005, UR-013 | Safety | Steering and battery stops | The steering wires shall keep a factor of 3 on their breaking load at a 30 N thumb push, and the battery packs shall have built-in protection and be charged away from the kit | 3 | min | factor | Analysis (J16: 3.0, wire breaking load assumed 250 N); supplier data and stops S2 and S8 in the build plan | Met on paper | New (STM S5) |
| PR-019 | UR-016 | Regulatory | Status statement | Every document and the README shall state that VoidScope is an open engineering reference, not certified rescue equipment and not a medical device | 1 | min | statement per document | Inspection of the documents | Met by design | New |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirements not met

None is unmet on paper. PR-006, PR-007 and PR-010 can only be settled by test or drills at TRL 4, and PR-005's margin to 5 mL/min at 2 m and 40 C with an oversize bore is 12 per cent (STM S7).

## Assumptions

- Local crews can open or find gaps of about 50 mm into most voids of interest.
- A rigid, sectioned rod is good enough for a first version, with a camera tip that bends in one plane; turning the rod chooses the plane. Following a bent channel with the rod itself is not required (PR-012 as restated).
- A slow gravity drip through a bite valve is an acceptable way to give water when a medical lead directs it; the bite valve stays on the nose and the operator steers the tip aside to give water (drill card, build plan section 5a); the medical lead's confirmation in drills is a TRL 4 item.
- Commodity sealed pipe-inspection camera heads meet the image, light and sealing targets; the camera's power at the dimmed LED setting is a datasheet figure to confirm (STM S14).
- The 15 kg carried-load target (PR-016) is a proposal; no standard has been looked up for it.

> **Safety:** These requirements describe rescue equipment that delivers water and air to a trapped person and carries a lithium battery. The steerable tip must be locked straight before it goes into or comes out of a hole. Meeting them on paper does not make the design safe to use. VoidScope is an open engineering reference, not certified rescue equipment and not a medical device; see VDS-PRC-001, Safety.
