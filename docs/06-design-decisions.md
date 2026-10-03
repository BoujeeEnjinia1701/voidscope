---
doc_id: VDS-DEC-001
title: VoidScope design decisions register
project: VoidScope
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval"
---

# VoidScope design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Several decisions below set safety stops: the drip ceiling, the bite valve, the blower's shut-off pressure and the battery chemistry. They were taken on the conservative side (VDS-DDR-001, Table 2). VoidScope is rescue equipment that is not certified and is not a medical device.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The camera head is 29 mm or less across and about 55 mm long, IP68 at 1 m for 30 min, AHD 1080p with about a 90° view and 12 dimmable LEDs | It sets the nose bore, R3 and R4 | VDS-DDR-001 D4; VDS-CAL-001 C |
| 2 | The blower's shut-off (maximum static) pressure is 1.0 kPa or less, and its curve gives at least 20 L/min through 0.38 kPa | It is the air pressure safety stop (R6) | VDS-DDR-001 D8, S3; VDS-CAL-001 E |
| 3 | The flow meter's pressure drop is 0.2 kPa or less at 20 L/min and it fits 100 mm tall | A larger drop lowers the full-speed flow; the lid must close | VDS-CAL-001 E; VDS-DDR-002 P11 |
| 4 | The snap button suits 1.47 mm and 2.11 mm walls, its button stands about 1.5 mm proud, and it holds a 300 N pull | It locks every joint | VDS-DDR-002 P2; VDS-CAL-001 B |
| 5 | The two tube sizes telescope with about 0.11 mm a side as bought | The couplers must slide in by hand | VDS-DDR-002 P1 |
| 6 | The capillary bore is 0.5 mm and the measured flow at 1 m and 20 °C is about 1.5 mL/min | It sets the drip ceiling (R5) | VDS-DDR-001 S1; VDS-CAL-001 D |
| 7 | The bite valve is about 11 mm across, fits the 4 mm tube and stays shut under 20 kPa of water head | It is the water safety stop | VDS-DDR-001 S2; VDS-CAL-001 D7 |
| 8 | The speaker is 20 mm across and 4 mm thick, IP67 | It must sit flush in its pocket | VDS-DDR-002 P8 |
| 9 | The hybrid cable is 6 mm or less across, and the case, monitor (28 mm deep) and battery (151 x 65 x 94 mm) match the sizes modelled | They set the grommets, the plate layout and the lid stack | VDS-DDR-002 P10, P11 |

## Value engineering

Value-engineering target: USD 2,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,578 (USD 422 under the target). Main cost drivers and savings worth trying:

- The largest lines are the lathe time allowance (USD 180), the monitor with recorder and bracket (USD 175), the cleaning kit and four spare water sets (USD 118), the rod sections (USD 128 for four), the rod carry case (USD 115), the battery packs (USD 110 for two), the surface unit case (USD 110) and the camera head (USD 95).
- Savings worth trying: a builder with a lathe saves USD 180; a soft carry bag in place of the hard rod case saves about USD 80; a single battery pack saves USD 55 but leaves no spare for a full shift at -10 °C.
- Making the design constructable added the couplers, buttons and pins, the guide tube, the equipment plate, the brackets and the lathe allowance, about USD 290 in all.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D13: lines inside with the bore as air duct; 38.1 mm aluminium sections with snap buttons; no articulation; bought IP68 camera head; monitor in the surface unit lid; tip speaker as speaker and microphone; gravity drip with capillary ceiling and bite valve; blower chosen by shut-off pressure; two LiFePO4 packs; independent of the crawler block; requirements restated; budget, pitch and problem kept | Amish: "I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | VDS-DDR-001 |
| 2026-10-03 | Conservative safety choices S1 to S6, each with the evidence that would relax it | Amish, same pre-approval | VDS-DDR-001, Table 2 |
| 2026-10-03 | First co-design candidate to approach: the disaster management training school of the Armed Police Force, Nepal; second: Turkey's AFAD training centres (not contacted, not partners) | Amish, same pre-approval | VDS-DDR-001 D11 |
| 2026-10-03 | Design for construction, changes P1 to P14 | Amish, same pre-approval | VDS-DDR-002 |
| 2026-10-03 | R11 (two 45° bends) recorded as not met in the first version; a flexible lead section is a later version, not TRL 3 work | Amish, same pre-approval | VDS-REQ-001 v0.3; VDS-DDR-001 D12 |
| 2026-10-03 | Appearance model departures from `model.py` (rounded edges, depth bands, labels, cables drawn to the surface unit, rubble context) accepted for renders only | Amish, same pre-approval | `docs/REVIEW.md`, TRL 3 |
