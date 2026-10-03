---
doc_id: VDS-DEC-001
title: VoidScope design decisions register
project: VoidScope
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval"
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish's requirement decision 3A (steerable camera tip, R11 restated) recorded as made (VDS-DDR-003); one new open decision on bite valve access; four items to confirm when parts are bought; value engineering updated"
---

# VoidScope design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Several decisions below set safety stops: the drip ceiling, the bite valve, the blower's shut-off pressure and the battery chemistry. The open decision on bite valve access touches how a survivor is given water. They were taken on the conservative side (VDS-DDR-001, Table 2). VoidScope is rescue equipment that is not certified and is not a medical device.

## Open decisions

*Table 1. Open decisions.*

| # | What is to be decided | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Bite valve access now that the steerable camera tip extends 140 mm beyond the nose. **Proposed, awaiting Amish.** The valve still sits on top of the nose, as decision 3A asked, so a survivor reaches it past the tip and the bending section, whose top is 2.8 mm below the valve. | A: keep the valve on the nose; to offer water, the operator steers the tip fully to one side (the camera then sits 109 mm to the side and 51 mm ahead of the nose) and the medical lead confirms in drills that a survivor can reach the valve. B: carry the valve on a 60 mm flexible extension of the water tube clipped along the sheath, so it is the foremost part when the tip is steered aside. C: move the valve onto the tip housing, running the water tube through the bending section. | A for the first prototype: no change to the water line, and drills with the co-design medical lead settle it; B if they find the valve hard to reach. C is not recommended: the water tube would flex at every bend and be harder to change and keep clean (R10). | A: none. B: a clip on the sheath and a 60 mm longer water tube; water set change rehearsed again. C: new bore in the links and tip housing | VDS-DDR-003, T9 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The camera head is 29 mm or less across and about 55 mm long, IP68 at 1 m for 30 min, AHD 1080p with about a 90° view and 12 dimmable LEDs, with a pigtail at least 170 mm long | It sets the tip housing bore, R3 and R4; the pigtail must reach back through the tip to its splice in the nose | VDS-DDR-001 D4; VDS-CAL-001 C |
| 2 | The blower's shut-off (maximum static) pressure is 1.0 kPa or less, and its curve gives at least 20 L/min through 0.38 kPa | It is the air pressure safety stop (R6) | VDS-DDR-001 D8, S3; VDS-CAL-001 E |
| 3 | The flow meter's pressure drop is 0.2 kPa or less at 20 L/min and it fits 100 mm tall | A larger drop lowers the full-speed flow; the lid must close | VDS-CAL-001 E; VDS-DDR-002 P11 |
| 4 | The snap button suits 1.47 mm and 2.11 mm walls, its button stands about 1.5 mm proud, and it holds a 300 N pull | It locks every joint | VDS-DDR-002 P2; VDS-CAL-001 B |
| 5 | The two tube sizes telescope with about 0.11 mm a side as bought | The couplers must slide in by hand | VDS-DDR-002 P1 |
| 6 | The capillary bore is 0.5 mm and the measured flow at 1 m and 20 °C is about 1.5 mL/min | It sets the drip ceiling (R5) | VDS-DDR-001 S1; VDS-CAL-001 D |
| 7 | The bite valve is about 11 mm across, fits the 4 mm tube and stays shut under 20 kPa of water head | It is the water safety stop | VDS-DDR-001 S2; VDS-CAL-001 D7 |
| 8 | The speaker is 20 mm across and 4 mm thick, IP67 | It must sit flush in its pocket | VDS-DDR-002 P8 |
| 9 | The hybrid cable is 6 mm or less across, and the case, monitor (28 mm deep) and battery (151 x 65 x 94 mm) match the sizes modelled | They set the grommets, the plate layout and the lid stack | VDS-DDR-002 P10, P11 |
| 10 | The 0.6 mm 7x7 stainless wire rope breaks at 250 N or more | It sets the factor of 3.0 at a 30 N thumb push against the stop | VDS-DDR-003; VDS-CAL-001 J16 |
| 11 | The 3 mm steering housings bend to about 15 mm radius where they turn up into the control body, and their friction is about 0.15 | A stiffer housing needs a taller pad; more friction raises the thumb force | VDS-DDR-003 T5, T8; VDS-CAL-001 J13 |
| 12 | The camera cable's bending stiffness is near 5,000 N·mm² | It sets the thumb force to hold 90° (about 5 N) | VDS-CAL-001 J12 to J14 |
| 13 | The printed links' 2.0 mm pin holes ream cleanly and the lugs hold the pins without rocking | The joints must swing freely but not wobble the camera | VDS-DDR-003 T3 |

## Value engineering

Value-engineering target: USD 2,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,780 (USD 220 under the target). Main cost drivers and savings worth trying:

- The largest lines are the lathe time allowance (USD 240), the monitor with recorder and bracket (USD 175), the cleaning kit and four spare water sets (USD 118), the rod sections (USD 128 for four), the rod carry case (USD 115), the battery packs (USD 110 for two), the surface unit case (USD 110) and the camera head (USD 95).
- Savings worth trying: a builder with a lathe saves USD 240; a soft carry bag in place of the hard rod case saves about USD 80; a single battery pack saves USD 55 but leaves no spare for a full shift at -10 °C; printing the base link and drum in PA12 with the links would save about an hour of lathe time (USD 60) at some cost in wear.
- Making the design constructable added the couplers, buttons and pins, the guide tube, the equipment plate, the brackets and the lathe allowance, about USD 290 in all. The steerable tip (decision 3A) added USD 202: links, pins and sheaths USD 42, base link USD 6, tip housing USD 8, wires and housings USD 38, steering control USD 48 and one more hour of lathe time USD 60.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D13: lines inside with the bore as air duct; 38.1 mm aluminium sections with snap buttons; no articulation; bought IP68 camera head; monitor in the surface unit lid; tip speaker as speaker and microphone; gravity drip with capillary ceiling and bite valve; blower chosen by shut-off pressure; two LiFePO4 packs; independent of the crawler block; requirements restated; budget, pitch and problem kept | Amish: "I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | VDS-DDR-001 |
| 2026-10-03 | Conservative safety choices S1 to S6, each with the evidence that would relax it | Amish, same pre-approval | VDS-DDR-001, Table 2 |
| 2026-10-03 | First co-design candidate to approach: the disaster management training school of the Armed Police Force, Nepal; second: Turkey's AFAD training centres (not contacted, not partners) | Amish, same pre-approval | VDS-DDR-001 D11 |
| 2026-10-03 | Design for construction, changes P1 to P14 | Amish, same pre-approval | VDS-DDR-002 |
| 2026-10-03 | R11 (two 45° bends) recorded as not met in the first version; a flexible lead section is a later version, not TRL 3 work (superseded the same day by decision 3A below) | Amish, same pre-approval | VDS-REQ-001 v0.3; VDS-DDR-001 D12 |
| 2026-10-03 | Appearance model departures from `model.py` (rounded edges, depth bands, labels, cables drawn to the surface unit, rubble context) accepted for renders only | Amish, same pre-approval | `docs/REVIEW.md`, TRL 3 |
| 2026-10-03 | Decision 3A: add a cable-steered articulating camera tip that bends up to 90° each way, controlled from the handle; restate R11 as "see around a 45-degree bend from a straight hole" with a verification method; keep the rigid rod, the air path and the water tube to the bite valve; the tip must still pass the 51 mm hole | Amish: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | VDS-DDR-003; VDS-REQ-001 v0.4 |
