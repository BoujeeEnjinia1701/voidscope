---
doc_id: VDS-CAL-001
title: VoidScope sizing calculations
project: VoidScope
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "First issue for TRL 3 on the constructable design (VDS-DDR-002): envelope and reach, rod structure and handling, vision, water, air, power, robustness, deployment, mass and cost"
---

# VoidScope sizing calculations

On paper the constructable design meets ten of its twelve requirements, estimates R9 within its target and misses R11. The probe is 48 mm at its widest and reaches 4.06 m; the rod buckles at 1,001 N, five times a hard two-handed push. The camera puts 19 pixels across a 20 mm letter at 1 m, twice what reading needs. The water ceiling is 1.5 mL/min at the allowed 1 m height at 20 °C and never more than 4.5 mL/min even at twice that height on a 40 °C day. The air path loses 0.38 kPa at 20 L/min, so the blower delivers 44 L/min at full speed while it can never put more than 0.9 kPa on a blocked tip. One battery pack runs video and light for 6.2 h at 20 °C and 4.3 h at -10 °C. The kit costs an estimated USD 1,578, USD 422 under the USD 2,000 value-engineering target. The miss is R11: the rigid rod cannot follow a bent path. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the probe is safe to use in a collapsed structure, that the water line is safe for a survivor, or that the battery is safe. The drip ceiling, the blocked-tip pressure and the snap-button pull strength must be measured on hardware before any use. VoidScope is not certified rescue equipment and not a medical device; see VDS-PRC-001, Safety.

## Scope and method

The note checks every requirement in VDS-REQ-001 v0.3 against the design in VDS-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()` and builds the model once for part volumes, so the rod, head and case used here are the ones in the STEP files and in drawing VDS-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a probe pushed horizontally or downward through a 51 mm core hole into a dark, dusty void, with the water bottle hung at most 1 m above the tip and the blower set to 20 L/min.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Rod | 6061-T6: E = 69 GPa, yield 240 MPa, density 2.7 g/cm³; stress concentration 3 at an 8.5 mm button hole | Handbook values |
| Loads | Two-handed push 200 N; pull to free a stuck probe 300 N | Assumed; to confirm in drills |
| Masses | Aluminium parts from model volumes; camera 0.18 kg; cable 45 g/m; PTFE guide, water tube and water from their sections; grip 0.15 kg; case 2.6 kg, pack 0.85 kg, monitor 0.6 kg | Catalogue-typical; to weigh at TRL 4 |
| Camera | 1920 pixels across a 90° horizontal view; 10 pixels needed across a letter; LEDs 60 lm in a 120° beam; minimum illumination 0.01 lx | Typical pipe-inspection head data; to confirm when bought |
| Dust | Extinction 0.5 per metre of path | Assumed for heavy suspended dust |
| Water | Poiseuille flow in a 0.5 mm by 600 mm capillary and 8 m of 2.5 mm tube; viscosity 1.52, 1.00 and 0.65 mPa·s at 5, 20 and 40 °C; bite valve and strainer losses ignored (they only lower the flow) | Laminar flow; standard water properties |
| Air | Smooth tubes (laminar or Blasius friction); minor loss 1.5 at each barb, 0.5 at each joint, 1.5 at the outlets; filter 2.5 Pa per L/min; flow meter 0.2 kPa at any flow (variable-area meters are near constant); blower curve shut-off 0.9 kPa and free flow 300 L/min, scaling with speed squared and speed | Screening values; the blower and flow meter figures are to confirm when bought |
| Power | Camera with LEDs 3 W; monitor and recorder 7 W; converter 90 %; blower 4 W at full speed, scaling with speed cubed, plus 0.3 W controller; amplifier standby 0.4 W | Typical module data |
| Battery | 12.8 V 6 Ah LiFePO4, 90 % usable, 70 % of capacity at -10 °C | Typical cell data |

## A. Envelope and reach (R1, R2, R11)

The probe passes a 51 mm core hole along its whole length: the head is 48 mm, the grip 47 mm and the snap buttons stand 1.5 mm proud of the 38.1 mm rod [A1], leaving 1.5 mm a side at the head [A2]. The assembled probe is 4,398 mm long [A3] and the working length from the front of the grip to the tip is 4,063 mm [A4], so R2 is met with 63 mm to spare. The head is 173 mm long [A5]. A rigid rod follows no bend [A6], so R11 is not met.

## B. Rod structure and handling

The 38.1 x 1.47 mm tube has a second moment of area of 28,400 mm⁴ and a section modulus of 1,490 mm³ [B1, B2]. With couplers and filled lines the rod weighs 0.61 kg per metre [B3]; the head weighs 0.67 kg [B4] and the assembled probe 3.66 kg [B5].

*Table 2. Handling with the hole lip as the pivot and the tip hanging free.*

| Length in the void | Tip droop | Hand force at the grip | Tag |
| --- | --- | --- | --- |
| 1 m | 1.5 mm | 7.8 N lift | [B6a], [B71] |
| 2 m | 15 mm | 3.6 N push down | [B6b], [B72] |
| 3 m | not computed | 34 N push down | [B73] |

The rod is stiff enough to aim, and the operator holds it easily until about 2 m is in the void with nothing under the tip. Beyond that the hand force rises quickly, so in practice the tip should rest on debris; the build plan's first checks include it. At 3 m with the tip unsupported the moment at the hole lip is 46.8 N·m [B8], 31 MPa in the plain tube [B9] and 94 MPa at a button hole [B10], a factor of 2.55 on yield [B11].

The whole rod buckles, pinned at both ends, at 1,001 N [B12], five times a 200 N two-handed push [B13]. A 300 N pull to free a stuck probe bears 25.5 MPa on a button hole [B14], shears 3.4 MPa behind it [B15] and puts 11.9 MPa on the two coupler pins with no help from the epoxy [B16]. The button itself is a bought part; its pull strength is to be confirmed when bought (VDS-DEC-001).

## C. Vision (R3)

At 1 m the camera sees a 2,000 mm wide field [C1], which puts 19.2 pixels across a 20 mm letter [C2] against the 10 assumed to read it [C3]. The LEDs give about 19 lx on axis at 1 m [C4], about 1,900 times the sensor's minimum [C5], and about 7 lx after 2 m of heavily dusty air [C6]. R3 is met on paper; backscatter from dust close to the lens is the real risk and is a TRL 4 test.

## D. Water (R5, R10)

*Table 3. Drip ceiling with the clamp fully open (mL/min) [D1].*

| Water height above the tip | 5 °C | 20 °C | 40 °C |
| --- | --- | --- | --- |
| 0.5 m | 0.49 | 0.74 | 1.13 |
| 1.0 m (the allowed height) | 0.97 | 1.47 | 2.26 |
| 2.0 m (twice the allowed height) | 1.94 | 2.94 | 4.51 |

The capillary is sized conservatively: even with the bottle hung a metre too high on a 40 °C day, the flow cannot pass 4.51 mL/min [D2], under the 5 mL/min ceiling of R5. At the allowed 1 m and 20 °C the ceiling is 1.47 mL/min [D3], about 88 mL an hour [D4], or roughly 2 L a day; the roller clamp sets any lower rate down to zero. Without the capillary the same line would pass 70 mL/min [D6], which is why it is fitted and never removed. The primed line holds 39 mL [D5]; at most 19.6 kPa of water head sits behind the bite valve [D7], within what a hydration bite valve holds shut. Changing the water set takes about 4 minutes by the steps in [D8], within R10.

What would relax the ceiling: measured flows at the tip with the bought capillary, and the co-design medical lead's view of the rate a survivor should be offered. A shorter capillary could then raise the ceiling toward 5 mL/min at 1 m.

## E. Air (R6)

*Table 4. Pressure losses at 20 L/min [E1].*

| Part of the path | Loss (Pa) |
| --- | --- |
| Intake filter | 50 |
| Flow meter | 200 |
| Hose, 12 mm, 2.5 m | 55 |
| Two barbs (case outlet and tail cap) | 54 |
| Rod bore with four joints | 10 |
| Six outlets | 7 |
| Total | 376 |

The rod bore is a generous duct: it loses only 10 Pa. Most of the loss is in the flow meter and the filter. The air leaves the six outlets at 2.8 m/s [E2], gentle enough not to blast dust. With the assumed blower curve the system passes 44 L/min at full speed [E3], and the speed knob near 65 % [E4] gives 20 L/min. With every outlet blocked the pressure cannot exceed the blower's shut-off, 0.9 kPa [E5], under the 1 kPa limit of R6; this is why the blower is chosen by its shut-off pressure. Each coupler leaks about 0.08 L/min at 50 Pa [E6], negligible. At 20 L/min the blower draws 1.4 W [E7].

What would relax it: none is needed for R6. If the flow meter's real pressure drop is larger than 0.2 kPa, the flow at full speed falls; a flow meter with a lower drop is the fix.

## F. Power (R7)

Video and light draw 11.1 W at the battery [F1], 12.9 W with air and audio [F2]. One 76.8 Wh pack [F3] runs video and light for 6.2 h at 20 °C and 4.3 h at -10 °C [F4], meeting R7 at both temperatures; with air and audio it runs 5.4 h and 3.8 h [F5]. The two packs together give 7.5 h at -10 °C with everything on [F6]. The peak current is 1.4 A [F7], far below the 7.5 A fuse and the pack's rating.

## G. Robustness (R4)

A 1 m drop of the head and the first section together carries about 13 J [G1]. The nose has a minimum wall of 2.85 mm [G2] around a camera that is already rated IP68, and the window is recessed 3 mm behind the nose lip. R4 is met by design and is a TRL 4 test.

## H. Deployment (R9)

*Table 5. Setup time estimate, two people [H1 to H5].*

| Step | Minutes |
| --- | --- |
| Open both cases, lift out the rod bundle and head | 0.4 |
| Join the head and four sections (snap buttons) | 0.7 |
| Plug the camera cable, fit the air hose, hang the bottle | 0.6 |
| Switch on, check the picture and voice | 0.4 |
| Total | 2.1 |

## I. Mass and cost (R8)

The surface unit weighs about 6.2 kg with one pack fitted [I1]; with the 3.7 kg probe in its long case the kit is a two-person carry. The bill of materials prices the constructable design at USD 1,578 [I2]. Value-engineering target: USD 2,000 [I3]. Estimated cost of the constructable design: USD 1,578 (USD 422 under the target) [I4]. A builder with a lathe saves the USD 180 machining allowance, bringing it to USD 1,398 [I5].

## Results against requirements

*Table 6. Requirement status.*

| ID | Result | Status |
| --- | --- | --- |
| R1 | 48 mm largest diameter | Met |
| R2 | 4,063 mm working length | Met |
| R3 | 19 pixels per letter; 7 lx in dust | Met on paper |
| R4 | IP68 camera, 2.85 mm minimum wall | By design, to test |
| R5 | Ceiling 1.47 mL/min at 1 m and 20 °C; 4.51 mL/min at most | Met |
| R6 | 44 L/min at full speed; 0.9 kPa blocked | Met |
| R7 | 6.2 h at 20 °C; 4.3 h at -10 °C | Met |
| R8 | USD 1,578 against the USD 2,000 target | USD 422 under the target |
| R9 | 2.1 min estimated | Estimate; timed drills needed |
| R10 | About 4 min, no tools | By design, to time |
| R11 | Rigid rod | **Not met** |
| R12 | Speaker and microphone at the tip | By design |
