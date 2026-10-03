---
doc_id: VDS-CAL-001
title: VoidScope sizing calculations
project: VoidScope
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "First issue for TRL 3 on the constructable design (VDS-DDR-002): envelope and reach, rod structure and handling, vision, water, air, power, robustness, deployment, mass and cost"
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Steerable camera tip (VDS-DDR-003, Amish's decision 3A): new section J for R11 as restated; envelope, reach, masses, handling, setup time and cost recomputed"
---

# VoidScope sizing calculations

On paper the constructable design, now with a steerable camera tip (VDS-DDR-003), meets eleven of its twelve requirements and estimates R9 within its target. The probe is 48 mm at its widest with the tip straight and goes 4.13 m into a void; the rod buckles at 940 N, 4.7 times a hard two-handed push. The tip bends up to 90° each way from a thumb lever, so the camera looks around a 45° bend with half its travel to spare (R11 as restated by Amish on 2026-10-03). The camera puts 19 pixels across a 20 mm letter at 1 m, twice what reading needs. The water ceiling is 1.5 mL/min at the allowed 1 m height at 20 °C and never more than 4.5 mL/min even at twice that height on a 40 °C day. The air path loses 0.38 kPa at 20 L/min, so the blower delivers 44 L/min at full speed while it can never put more than 0.9 kPa on a blocked tip. One battery pack runs video and light for 6.2 h at 20 °C and 4.3 h at -10 °C. The kit costs an estimated USD 1,780, USD 220 under the USD 2,000 value-engineering target. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the probe is safe to use in a collapsed structure, that the water line is safe for a survivor, or that the battery is safe. The drip ceiling, the blocked-tip pressure and the snap-button pull strength must be measured on hardware before any use. VoidScope is not certified rescue equipment and not a medical device; see VDS-PRC-001, Safety.

## Scope and method

The note checks every requirement in VDS-REQ-001 v0.4 against the design in VDS-PRC-001 v0.3, as changed by VDS-DDR-003, and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()` and builds the model once for part volumes, so the rod, head and case used here are the ones in the STEP files and in drawing VDS-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a probe pushed horizontally or downward through a 51 mm core hole into a dark, dusty void, with the water bottle hung at most 1 m above the tip and the blower set to 20 L/min.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Rod | 6061-T6: E = 69 GPa, yield 240 MPa, density 2.7 g/cm³; stress concentration 3 at an 8.5 mm button hole | Handbook values |
| Loads | Two-handed push 200 N; pull to free a stuck probe 300 N | Assumed; to confirm in drills |
| Masses | Aluminium parts from model volumes; printed nylon (PA12) 0.95 g/cm³, stainless 7.9 g/cm³, silicone 1.15 g/cm³ from model volumes; camera 0.18 kg; cable 45 g/m; steering housings 25 g/m; PTFE guide, water tube and water from their sections; grip 0.15 kg; case 2.6 kg, pack 0.85 kg, monitor 0.6 kg | Catalogue-typical; to weigh at TRL 4 |
| Steering | Camera cable bending stiffness 5,000 N·mm²; housing friction coefficient 0.15 over 180° of bends; 0.6 mm 7x7 stainless wire rope breaks at 250 N; a firm thumb push is 30 N; printed PA12 yields at about 45 MPa | Assumed; the cable stiffness and wire strength to confirm when bought |
| Camera | 1920 pixels across a 90° horizontal view; 10 pixels needed across a letter; LEDs 60 lm in a 120° beam; minimum illumination 0.01 lx | Typical pipe-inspection head data; to confirm when bought |
| Dust | Extinction 0.5 per metre of path | Assumed for heavy suspended dust |
| Water | Poiseuille flow in a 0.5 mm by 600 mm capillary and 8 m of 2.5 mm tube; viscosity 1.52, 1.00 and 0.65 mPa·s at 5, 20 and 40 °C; bite valve and strainer losses ignored (they only lower the flow) | Laminar flow; standard water properties |
| Air | Smooth tubes (laminar or Blasius friction); minor loss 1.5 at each barb, 0.5 at each joint, 1.5 at the outlets; filter 2.5 Pa per L/min; flow meter 0.2 kPa at any flow (variable-area meters are near constant); blower curve shut-off 0.9 kPa and free flow 300 L/min, scaling with speed squared and speed | Screening values; the blower and flow meter figures are to confirm when bought |
| Power | Camera with LEDs 3 W; monitor and recorder 7 W; converter 90 %; blower 4 W at full speed, scaling with speed cubed, plus 0.3 W controller; amplifier standby 0.4 W | Typical module data |
| Battery | 12.8 V 6 Ah LiFePO4, 90 % usable, 70 % of capacity at -10 °C | Typical cell data |

## A. Envelope and reach (R1, R2)

With the tip locked straight the probe passes a 51 mm core hole along its whole length: the head, bending section and tip housing all lie inside 48 mm, the grip is 47 mm and the snap buttons stand 1.5 mm proud of the 38.1 mm rod [A1], leaving 1.5 mm a side at the head [A2]. The model checks every head part, the steerable tip included, inside the 48 mm outline. The steering control on section 4 is wider, but it sits behind the grip's front hand position and never enters the hole. The assembled probe is 4,538 mm long [A3]. The probe can go 4,131 mm into a void before the steering control reaches the hole [A4] (4,203 mm measured from the front of the grip [A4g]), so R2 is met with 131 mm to spare. The head is 313 mm long [A5], of which the steerable tip is the front 140 mm [A6].

## B. Rod structure and handling

The 38.1 x 1.47 mm tube has a second moment of area of 28,400 mm⁴ and a section modulus of 1,490 mm³ [B1, B2]. With couplers, steering housings and filled lines the rod weighs 0.65 kg per metre [B3]; the head weighs 0.77 kg [B4], of which 0.28 kg is the steerable tip ahead of the nose [B4t]. The steering housings, wires and control add 0.41 kg [B4s], and the assembled probe weighs 4.18 kg [B5].

*Table 2. Handling with the hole lip as the pivot and the tip hanging free.*

| Length in the void | Tip droop | Hand force at the grip | Tag |
| --- | --- | --- | --- |
| 1 m | 1.7 mm | 8.6 N lift | [B6a], [B71] |
| 2 m | 17 mm | 3.1 N push down | [B6b], [B72] |
| 3 m | not computed | 32 N push down | [B73] |

The rod is stiff enough to aim, and the operator holds it easily until about 2 m is in the void with nothing under the tip. Beyond that the hand force rises quickly, so in practice the tip should rest on debris; the build plan's first checks include it. At 3 m with the tip unsupported the moment at the hole lip is 51.2 N·m [B8], 34 MPa in the plain tube [B9] and 103 MPa at a button hole [B10], a factor of 2.33 on yield [B11].

The whole rod buckles, pinned at both ends, at 940 N [B12], 4.7 times a 200 N two-handed push [B13]. A 300 N pull to free a stuck probe bears 25.5 MPa on a button hole [B14], shears 3.4 MPa behind it [B15] and puts 11.9 MPa on the two coupler pins with no help from the epoxy [B16]. The button itself is a bought part; its pull strength is to be confirmed when bought (VDS-DEC-001).

## C. Vision (R3)

The camera head is the same bought unit, now carried in the tip housing. At 1 m it sees a 2,000 mm wide field [C1], which puts 19.2 pixels across a 20 mm letter [C2] against the 10 assumed to read it [C3]. The LEDs give about 19 lx on axis at 1 m [C4], about 1,900 times the sensor's minimum [C5], and about 7 lx after 2 m of heavily dusty air [C6]. R3 is met on paper; backscatter from dust close to the lens is the real risk and is a TRL 4 test.

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

A 1 m drop of the head and the first section together carries about 14 J [G1]. The nose keeps a minimum wall of 2.85 mm [G2]. The camera, already rated IP68, now sits in a 1.85 mm aluminium tip housing with its window recessed 3 mm behind the housing's front edge, and the bending section is covered by a replaceable 0.6 mm silicone sheath. The printed links and the sheath are the new weak points in a drop or against sharp rubble. R4 is met by design and is a TRL 4 test, now including drops with the tip bent and straight.

## H. Deployment (R9)

*Table 5. Setup time estimate, two people [H1 to H6].*

| Step | Minutes |
| --- | --- |
| Open both cases, lift out the rod bundle and head | 0.4 |
| Join the head and four sections (snap buttons) | 0.7 |
| Plug the camera cable, fit the air hose, hang the bottle | 0.6 |
| Switch on, check the picture and voice | 0.4 |
| Steer the tip both ways, lock it straight | 0.1 |
| Total | 2.2 |

The steering wires stay threaded with the other lines, so steering adds no connection, only a check.

## I. Mass and cost (R8)

The surface unit weighs about 6.2 kg with one pack fitted [I1]; with the 4.2 kg probe in its long case the kit is a two-person carry. The bill of materials prices the constructable design at USD 1,780 [I2]. Value-engineering target: USD 2,000 [I3]. Estimated cost of the constructable design: USD 1,780 (USD 220 under the target) [I4]. The steerable tip added USD 202: the printed links, pins and sheaths (USD 42), the base link (USD 6), the tip housing (USD 8), the wires and housings (USD 38), the steering control (USD 48) and one more hour of lathe time (USD 60). A builder with a lathe saves the USD 240 machining allowance, bringing it to USD 1,540 [I5].

## J. Steerable tip (R11, R1)

R11 as restated by Amish on 2026-10-03: see around a 45° bend from a straight hole. The tip is five pinned joints [J1] in a 66 mm bending section [J4] between the base link in the nose and the tip housing that carries the camera. Each joint's link faces close at 18.1° [J2], so with every joint closed the tip bends 90.4° each way [J3]; the lever's stops end the travel at 90°. The model was posed at 90° each way and no two neighbouring links overlap [J7]: the lug ends are rounded about their pins so a link face can swing past them.

*Table 6. Where the camera points (bend shared equally by the five joints).*

| Bend | Camera face, ahead of the nose front | Camera face, to the side | Sideways reach of the bent tip from the centreline | Tag |
| --- | --- | --- | --- | --- |
| 45° | 115 mm | 72 mm | 83 mm | [J5-45], [J6] |
| 90° | 51 mm | 109 mm | 109 mm | [J5-90], [J8] |

To look down a passage that turns 45°, the tip needs half its travel. Bent 45°, the camera points straight down the turned passage and its 90° field of view takes in everything from the line of the probe to 90° off it, so a 20 mm letter 1 m down the turned passage still gets 19 pixels [C2], nearly twice the 10 needed [C3]. The bent tip needs 83 mm to the side of the probe's line [J6], so it turns in any passage about 170 mm wide or wider; the R11 test passage is 300 mm wide. R11 is met on paper with 45° of bend to spare.

**Steering effort.** A 45° bend pulls in 11.1 mm of wire on the inside and pays out 10.9 mm on the outside [J9-45]; 90° pulls in 22.2 mm and pays out 21.6 mm [J9-90]. The 0.6 mm difference is taken up by the housings and needs no spring at this stage. On the 18 mm drum the lever turns 35° for 45° at the tip [J11] and 71° for 90° [J10]. Holding the camera cable bent 90° takes about 119 N·mm [J12], 8.5 N in the wire at the tip and 13.6 N at the drum with friction in the housings [J13], or about 5 N at the thumb on the 50 mm lever [J14].

**Strength.** A 30 N thumb push against the stop puts 83 N in the wire [J15], a factor of 3.0 on its assumed breaking load [J16], 13 MPa of shear in a joint's two 2 mm pins [J17] and 8.7 MPa of bearing on the printed lugs [J18], about a fifth of what PA12 takes. The lugs are the part to watch in drop and abrasion tests; the wire's breaking load is to confirm when bought.

**Getting out again (R1).** The friction lock only holds the lever; the wires are not self-locking. If the probe is withdrawn with the tip still bent, the hole's edge pushes the tip straight against at most a few newtons of wire tension. The procedure is still to steer straight and lock before pulling back through the hole.

What would relax it: a measured bending stiffness for the bought camera cable (a stiffer cable raises the thumb force, a softer one lowers it) and drop tests of the printed links. A two-plane tip (up and down as well) is possible later with four wires; one plane plus turning the rod covers R11.

## Results against requirements

*Table 7. Requirement status.*

| ID | Result | Status |
| --- | --- | --- |
| R1 | 48 mm largest diameter with the tip straight | Met |
| R2 | 4,131 mm into the void (4,203 mm from the grip) | Met |
| R3 | 19 pixels per letter; 7 lx in dust | Met on paper |
| R4 | IP68 camera in an aluminium tip housing; sheathed bending section; 2.85 mm minimum nose wall | By design, to test |
| R5 | Ceiling 1.47 mL/min at 1 m and 20 °C; 4.51 mL/min at most | Met |
| R6 | 44 L/min at full speed; 0.9 kPa blocked | Met |
| R7 | 6.2 h at 20 °C; 4.3 h at -10 °C | Met |
| R8 | USD 1,780 against the USD 2,000 target | USD 220 under the target |
| R9 | 2.2 min estimated | Estimate; timed drills needed |
| R10 | About 4 min, no tools | By design, to time |
| R11 | Tip bends 90° each way; 45° bend seen with 19 px per letter at 1 m; bent tip needs 83 mm to the side | Met on paper |
| R12 | Speaker and microphone on the head, about 0.2 m behind the camera | By design |
