---
doc_id: VDS-STM-001
title: VoidScope STEM check
project: VoidScope
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): 26 claims on options A, B and C screened against known science; five failures fixed or restated under the standing instruction after the first pass and the independent review (tip heat F1, option B free reach F2, capillary margin F3, tip touch criterion F4, blower supply F5; VDS-DDR-006)"
---

# VoidScope STEM check

Of 26 claims checked, 12 sit within known science and 14 are plausible and are bounded by VDS-CAL-001 or left to bought-part datasheets and TRL 4 tests; none fails now. The first pass and an independent review found five failures, all fixed or restated under Amish's standing instruction of 2026-10-23 without changing the working principle: the camera tip would reach 85 C at 45 C ambient (black anodised housing, LEDs dimmed, 44 C at 35 C ambient), the drip ceiling had no margin for an oversize capillary bore (capillary lengthened to 750 mm, 4.4 mL/min worst case), the droop at 2 m was 17 mm and is 39 mm once the back span is included, the blocked-tip air pressure could exceed 1 kPa on a blower run straight from the pack (regulated supply with a speed cap), and a 10 mm glass-fibre rod cannot hold a head in free air (option B reach restated). Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py` (results in `docs/04-calcs/stem_results.csv`).

> **Safety:** This is a paper screen of physical claims. It does not show that the probe, the water line or the battery is safe to use. VoidScope is an open engineering reference, not certified rescue equipment and not a medical device.

## Claims checked

*Table 1. Claims, governing science and verdicts (S1 to S22 option A, the design of record; SB1 and SB2 option B; SC1 and SC2 option C).*

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | The whole rod survives a hard two-handed push of 200 N without buckling (twice the push as margin) | Physics | Strength of materials | Euler column buckling, P = pi^2 E I / L^2, pinned at both ends, 6061-T6 38.1 x 1.47 mm tube, 4.54 m: 940 N against 400 N needed. This is the ideal upper bound for a uniform tube; the slack at four couplers (0.11 mm a side) and the rod's own sag lower it (independent review) | 940 N ideal against 400 N needed; couplers fitted to test at TRL 4 | Plausible, to confirm at TRL 3 | VDS-CAL-001 B12 (940 N); PR-017 |
| S2 | With 2 m of probe unsupported beyond the hole the tip droops by a few per cent of that length, so the tip is rested on debris beyond about 2 m | Physics | Strength of materials | Cantilever d = w L^4 / 8EI + P L^3 / 3EI = 16.8 mm, plus the turn of the back span about the hole lip (pivot, grip held): 37 mm in all. The first version took the lip as a clamp (16.8 mm) and the independent review corrected it | 37 mm at 2 m, about 2 per cent of the length; the camera looks about 1 degree low, which the steering takes up | Plausible, to confirm at TRL 3 | VDS-CAL-001 B6b (39 mm); build plan section 5 |
| S3 | At a snap-button hole the rod keeps a safety factor of at least 2 on yield with 3 m unsupported in a void | Physics | Strength of materials | Bending stress M / Z with a stress concentration of 3 at an 8.5 mm hole; 6061-T6 yield 240 MPa | 103 MPa <= 120 MPa | Within known science | VDS-CAL-001 B11 (factor 2.33) |
| S4 | The two coupler pins carry a 300 N pull to free a stuck probe | Engineering and technology | Strength of materials | Double shear of two 4 mm aluminium pins, tau = F / (2 n A); shear strength taken as 0.58 of 240 MPa | 6 MPa <= 139.2 MPa | Within known science | VDS-CAL-001 B16 (11.9 MPa) |
| S5 | A steering wire keeps a factor of 3 on its assumed breaking load under a 30 N thumb push against the stop | Physics | Strength of materials | Lever and drum: wire tension T = F x lever / drum radius = 30 N x 50 mm / 18 mm radius (36 mm drum) = 83 N; 0.6 mm 7x7 stainless rope breaking load 250 N assumed (to confirm from the supplier) | 83.3 N <= 83.33 N | Plausible, to confirm at TRL 3 | VDS-CAL-001 J15, J16 (factor 3.0) |
| S6 | The printed PA12 hinge lugs bear the wire tension without yielding | Engineering and technology | Strength of materials | Bearing stress F / (n d t) on two 2 mm pins in 2.4 mm lugs at 83 N; PA12 yield about 45 MPa (datasheet value, to confirm) | 8.7 MPa <= 30 MPa | Within known science | VDS-CAL-001 J18 (8.7 MPa) |
| S7 | The gravity drip never exceeds 5 mL/min, even with the bottle 2 m up (1 m allowed plus 1 m error) and water at 40 C | Physics | Fluid mechanics | Hagen-Poiseuille flow in a 0.5 mm bore (5 per cent oversize as worst case), 750 mm long capillary (600 mm failed the margin, fix F3), Q = pi r^4 dP / 8 mu L (8 m of 2.5 mm tube in series lowers it further) | 4.44 mL/min <= 5 mL/min | Within known science | VDS-CAL-001 D2 (4.39 mL/min) |
| S8 | The capillary flow is laminar, so the Poiseuille law applies | Physics | Fluid mechanics | Reynolds number Re = rho v d / mu below 2,000 at the highest flow | 273 (Re) <= 2000 (Re) | Within known science | VDS-CAL-001 D1 |
| S9 | At the 1 m, 20 C setting the drip supplies at least half of the 2.5 L a day that Sphere gives as the survival need for drinking | Biology | Human physiology | Sphere Handbook, water supply standard 1: survival needs 2.5 to 3 litres per day (drinking and food); 88 mL/h is 2.1 L/day. The drip is a bridge until extrication, not full hydration | 1.7 L/day >= 1.25 L/day | Within known science | VDS-CAL-001 D4 |
| S10 | The air path loses less than the blower can overcome at 20 L/min | Physics | Fluid mechanics | Sum of Darcy-Weisbach pipe losses and minor losses over the filter, meter, 2.5 m hose, barbs, rod bore and outlets; blower shut-off 0.9 kPa | 0.376 kPa <= 0.9 kPa | Within known science | VDS-CAL-001 E1 |
| S11 | With every outlet blocked the pressure at the tip stays below 1 kPa above ambient | Physics | Fluid mechanics | Blower shut-off pressure is the only stop (a centrifugal blower cannot exceed its shut-off head), and it rises with the square of speed, so the blower runs from the converter's regulated output with a fixed speed cap and not straight from the pack (12.8 to 14.4 V would lift 0.9 kPa to about 1.1 to 1.3 kPa); 0.9 kPa is a datasheet figure to confirm when bought (fix F5, independent review) | 0.9 kPa <= 1 kPa | Plausible, to confirm at TRL 3 | VDS-CAL-001 E5 |
| S12 | A 20 mm letter 1 m from the camera spans enough pixels to read | Physics | Optics | Pinhole geometry: 1920 pixels across a 90 degree view give 0.96 px/mm at 1 m, 19.2 px per 20 mm letter against 10 needed. This counts sensor pixels only; lens blur, compression and an analogue link can cost 30 to 50 per cent, which still leaves about 10 px (independent review) | 19.2 px at the sensor, about 10 px after losses | Plausible, to confirm at TRL 3 | VDS-CAL-001 C2 (19.2 px); chart test at TRL 4 |
| S13 | In moderate dust (extinction 0.5 per m, visibility about 8 m) the light after 2 m is far above the camera's minimum illumination; in dust so dense that visibility is 1 m nothing is seen, as with any camera | Physics | Optics | Inverse-square illuminance from 60 lm in a 120 degree beam, Beer-Lambert extinction over the 2 m round trip: 7.0 lx at 0.5 per m, 0.0064 lx at 4 per m against a 0.01 lx minimum. The first version called 0.5 per m heavy dust (independent review) | 7.0 lx at 0.5 per m; 0.0064 lx at 4 per m | Plausible, to confirm at TRL 3 | VDS-CAL-001 C6, C7; dust box at TRL 4 |
| S14 | After the fix (housing black anodised, emissivity 0.85; LEDs dimmed so the head dissipates 0.8 W by default) the tip housing stays at or below 48 C, the 10 minute touch limit for bare metal, at 35 C ambient | Physics | Thermodynamics and heat transfer | Same convection and radiation model; at 45 C ambient it reaches 54 C, so above 35 C ambient the tip is kept off the survivor (steered aside, as for giving water) and the LEDs are kept at the lowest useful setting; camera power at the dimmed setting is a datasheet figure to confirm when bought | 44.4 C <= 48 C | Plausible, to confirm at TRL 3 | VDS-DDR-006 F1; VDS-CAL-001 K1 to K5 |
| S15 | One pack runs video and light for at least 4 h at -10 C | Physics | Thermodynamics and heat transfer | Energy balance: 76.8 Wh x 0.9 usable x 0.70 of capacity at -10 C (assumed) over an 11.1 W load (camera at full power 3 W, monitor 7 W, converter 90 %; the dimmed camera, about 0.8 W, makes the run longer) | 4.36 h >= 4 h | Plausible, to confirm at TRL 3 | VDS-CAL-001 F4--10 (4.35 h) |
| S16 | Aluminium tube with stainless pins, wire and screws and a brass air barb survives a wet shift in a collapsed building | Chemistry | Electrochemistry and batteries | Galvanic series: 6061 aluminium is anodic to stainless steel and brass, so a wet crevice corrodes the aluminium; anodising insulates, the wet time is one shift and the kit is rinsed and dried after use | No rate can be stated at first order; the pins and screws sit in anodised or nylon-tipped holes | Plausible, to confirm at TRL 3 |  |
| S17 | A LiFePO4 pack delivers its rated energy at -10 C and is charged only above 0 C | Chemistry | Electrochemistry and batteries | LiFePO4 cells discharge at low temperature with reduced capacity (70 % assumed) and must not be charged below freezing; the exact limits are on the pack datasheet, to confirm when bought | Charging indoors away from the kit is already a stop (build plan S2, S8) | Plausible, to confirm at TRL 3 |  |
| S18 | A bite valve passes water only when bitten, with 19.6 kPa of water head behind it | Biology | Human physiology | Water pressure rho g h = 19.6 kPa at 2 m; a silicone slit bite valve stays closed until bitten at a cracking pressure that must exceed it (supplier figure, not yet known) | Cracking pressure and the survivor's ability to bite and sip are to confirm at TRL 4 with the medical lead | Plausible, to confirm at TRL 3 |  |
| S19 | The assembled probe is 4.54 m long | Mathematics | Units and dimensional analysis | Four 1,050 mm sections plus a 313 mm head plus the tail cap | claimed 4538 mm, estimate 4.54e+03 mm (ratio 1.00) | Within known science | VDS-CAL-001 A3 |
| S20 | The setup time of 2.2 min is the sum of its steps | Mathematics | Units and dimensional analysis | Sum of the timed steps (estimates, to time in drills) | in 2.2 min, out 2.2 min | Within known science | VDS-CAL-001 H6 |
| S21 | The head fits a standard 51 mm core hole | Engineering and technology | Standards practice | Geometry: largest diameter on the probe 48 mm against a 51 mm core hole, 1.5 mm a side | 48 mm <= 51 mm | Within known science | VDS-CAL-001 A1, A2 |
| S22 | The kit costs less than the value-engineering target | Engineering and technology | Standards practice | Sum of bom/bom.csv against budget_usd 2,000 (a control target, not a limit) | 1780 USD <= 2000 USD | Within known science | VDS-CAL-001 I2 |
| SB1 | Option B (after the fix): the 10 mm glass-fibre rod reaches 4 m only where the void floor or debris carries it; free reach in air is capped at 1 m | Physics | Strength of materials | Cantilever droop at only 1 m is 93 mm (E 40 GPa assumed, I = 491 mm4), growing with L^3: a flexible rod cannot hold a head in free air beyond about 1 m. Fix: B is claimed only where the void floor or debris carries the rod, free reach capped at 1 m | Floor-supported reach plausible, to test; the first claim (4 m in free air) failed and was restated | Plausible, to confirm at TRL 3 | VDS-OPT-001; VDS-DDR-006 F2 |
| SB2 | Option B: winding the rod on a 640 mm hub keeps the bending strain at about 1.5 per cent | Physics | Strength of materials | Elastic strain of a rod bent on a drum, e = d / (2R + d) = 1.54 per cent, about 600 MPa at 40 GPa; that is a large share of the strength of pultruded glass-fibre rod and glass composites creep under sustained load, so a larger hub or the supplier's allowable strain is needed (independent review) | 1.54 per cent against an unknown allowable | Plausible, to confirm at TRL 3 | VDS-OPT-001 |
| SC1 | Option C: each tripod leg carries the 150 N hanging load with a factor of 10 against buckling | Physics | Strength of materials | Euler buckling of a 32 x 2 mm aluminium tube, 1.8 m, pinned ends; load shared by three legs and taken as 150 N per leg (conservative) | 1500 N <= 4477 N | Within known science | VDS-OPT-001 |
| SC2 | Option C: the sonde hangs vertical and steady on its rope and the lines hang clear in a vertical hole | Physics | Mechanics and statics | A body hanging from an eye above its centre of mass hangs upright; it spins freely on the rope, so the picture rotates and the bite valve swings; steering is none | Works only down a vertical hole; side entry is not possible | Plausible, to confirm at TRL 3 |  |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails**. Every "Plausible" row names what would settle it: S1 (rod with couplers fitted), S2 (rest the tip on debris beyond 2 m), S5 (wire breaking load, 250 N assumed), S11 (blower shut-off pressure and supply), S12 and S13 (a chart test in a dust box), S14 (camera power at the dimmed setting), S15 (cold capacity of the pack), S16 (galvanic attack in a wet shift), S17 (pack datasheet), S18 (bite valve cracking pressure), SB1, SB2 and SC2 (options B and C, not carried forward).

## Fix history

Under the standing instruction of 2026-10-23, a failed row is fixed in the same session when the fix keeps the working principle. Details are in VDS-DDR-006.

1. **S14, heat in the camera tip (fix F1, and F4 for the criterion).** First version: the camera and its 12 LEDs dissipate 3 W in a sealed 33 x 71 mm aluminium housing, bead-blasted (emissivity 0.3). Natural convection and radiation put the surface at 85 C at 45 C ambient (VDS-CAL-001 K2). The first pass compared this with 55 C, the 10 s touch threshold for bare metal; the reviewer pointed out that a trapped survivor cannot pull away, so the 10 minute threshold of 48 C is the right one. Fix: the tip housing is black anodised (emissivity 0.85) and the LEDs are dimmed by default so the head dissipates 0.8 W. Result 44.4 C at 35 C ambient and 30 C at 20 C (K4, K5), inside 48 C; at 45 C ambient the housing reaches 53.9 C (K3), so above 35 C the tip is kept off the survivor, steered aside as when offering water. The light margin is about 700-fold in moderate dust (S13).
2. **S7, capillary margin (F3).** The reviewer showed that a capillary bore 5 per cent oversize gives 5.46 mL/min at 2 m and 40 C with the 600 mm capillary, over the 5 mL/min ceiling, because flow goes with the fourth power of the bore. Fix: the capillary is 750 mm long (BOM line 11), and the worst case, 2 m, 40 C and a bore 5 per cent oversize, is 4.4 mL/min. The drill card keeps the rule that the bottle is at most 1 m above the tip, measured vertically.
3. **S2, droop at 2 m.** The first version took the hole lip as a clamp (16.8 mm). The lip is a pivot and the span behind it also bends: 37 to 39 mm. The claim is restated (plausible, with the tip rested on debris beyond about 2 m).
4. **S11, blocked-tip pressure (F5).** The shut-off pressure rises with the square of speed, so a blower run straight from a 12.8 to 14.4 V pack could reach 1.1 to 1.3 kPa. Fix: the blower runs from the converter's regulated output with a fixed speed cap so the shut-off stays at or under 0.8 kPa; PR-007 becomes "to verify at TRL 4".
5. **SB1, option B reach in free air (F2).** First claim: the 10 mm glass-fibre rod carries a 0.5 kg head 4 m out. A cantilever of that rod droops about 93 mm at only 1 m and grows with the cube of length, so the claim failed in air. Restated: option B reaches 4 m only where the void floor or debris carries the rod, and its free reach is capped at 1 m.

## Fields not relevant

- Biology: S9 and S18 only. No living material is in the probe itself; the survivor's physiology sets the water ceiling and the bite valve rule.
- Chemistry beyond S16 and S17: no reactive process; the materials are aluminium, stainless steel, silicone, PTFE, polyurethane and polypropylene in dry or briefly wet use.
- Thermodynamic cycles, combustion and radiation hazards: none in the concept.

## Concept options

- **Option A, rigid sectioned rod with steerable tip (design of record):** 22 rows, 0 failing, 11 plausible.
- **Option B, reel-fed flexible push cable:** SB1 failed as first claimed and was restated; SB2 (reel bending strain 1.5 per cent) is plausible, not proven. Carried with its reach limited to floor-supported voids.
- **Option C, tripod and winch lowered sonde:** SC1 (tripod legs, factor 10 in buckling) within; SC2 plausible. Carried; it works only down a vertical hole.

## Independent review

One reviewer (headless `claude -p --model claude-opus-5-5`, because this session had no subagent tool, per the brief) saw only this check, its script and results, VDS-CAL-001, its script and results, and VDS-PRS-001. It tried to refute the headline results and every "Within known science" row, recomputing with python. It agreed with the arithmetic of most rows (buckling 940 N, drip 4.5 mL/min at the nominal bore, Re 295, 2.1 L a day, 4,543 mm, 48 mm) and disagreed with these, each handled as shown:

| Reviewer finding | Verdict change | What changed |
| --- | --- | --- |
| Drip ceiling has no margin: a bore 5 per cent oversize gives 5.46 mL/min; a probe pointed down puts the tip below the bottle | S7 kept Within after the fix | Capillary 750 mm, worst case 4.4 mL/min (F3); the 1 m rule is measured vertically on the drill card |
| Tip touch criterion wrong (10 s, not 10 min) | S14 restated | 48 C at 35 C ambient, 44.4 C (F4, F1) |
| Blocked-tip pressure can pass 1 kPa on the pack's voltage range | PR-007 to "to verify at TRL 4" | Regulated supply with a speed cap (F5) |
| Wire factor ambiguous: drum "18 mm" (radius or diameter) | S5 stays Plausible | The drum is 18 mm radius (36 mm across); text and formula now say so; the lever is 50 mm |
| Dust case: 0.5 per m is light haze, not heavy dust | S13 to Plausible | Moderate dust named; 4 per m case added (0.006 lx); LEDs raised briefly in thick dust |
| Droop at 2 m too low: the lip is a pivot | S2 to Plausible, 37 to 39 mm | Back span included; tip rested on debris beyond about 2 m |
| Reach 4.13 m unsupported has a factor of 1.4 at a button hole | PR-002 note | PR-002 says the tip rests on debris beyond about 2 m |
| S1 buckling is an ideal upper bound; S12 counts sensor pixels; SB2 stress about 600 MPa | S1, S12, SB2 to Plausible | Text states the limits |
| Camera power 3 W in the battery budget, 0.8 W in the heat fix | S15 text | The battery budget uses full power; the dimmed head draws less |
| K1 said 76 cm2 (82 computed); no K rows in results.csv; S10 said a 7 m hose (2.5 m in the model); PR-008 4.4 h against 4.3 h | Traceability | K rows added to results.csv; hose 2.5 m; PR-008 says 4.35 h |

Not accepted as a change: the check reuses the sizing script's assumptions and reads `results.csv`, so it is not fully independent of the calculation note; S4 and B16 treat the same pins in two ways (one conservative); the hole-alignment caveat for a rigid 313 mm head is a TRL 4 test with a bent 51 mm core. The reviewer's other suggestions (a thermistor cut-back, a passive relief valve, a thicker first section, 0.8 mm wire) were not adopted: they add parts or change the design, and the cheaper fixes above meet the claims; they are noted for Amish in VDS-DDR-006.

## Sources

- Roark's formulas for stress and strain (Euler column buckling, cantilever deflection) and Incropera's heat transfer text (Churchill-Chu correlation for a horizontal cylinder in natural convection): standard textbook relations, not opened for this session.
- Hagen-Poiseuille law for laminar flow in a tube, and standard water viscosity tables.
- Sphere Association. Water supply standard 1: access and water quantity. Survival needs 2.5 to 3 litres per day for drinking and food. https://sphereprototype.conted.ox.ac.uk/standards/watersupply/accessAndWaterQuantity.html (checked 2026-10-24; a prototype copy of the Sphere Handbook, to replace with the current edition).
- IEEE Product Safety Technical Committee. Accessible hot surfaces and burn hazards (table of burn thresholds for touched uncoated metal from the BS EN 13202 contact-temperature data: 65 C for 1 s, 55 C for 10 s, 48 C for 600 s). https://ewh.ieee.org/r4/chicago/pstc/content/Accessible-hot-surfaces-and-burn-hazards.pdf (checked 2026-10-24).
- Material data (6061-T6 modulus 69 GPa and yield 240 MPa; PA12 yield about 45 MPa; E-glass rod about 40 GPa) are handbook values assumed in VDS-CAL-001 and to confirm from suppliers.
