---
doc_id: VDS-DDR-001
title: VoidScope TRL 2 review decisions
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
  change: "TRL 2 review decisions, decided under Amish's 2026-10-03 pre-approval of the batch and its recommendations"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The TRL 2 populate step (session 2026-10-03, `docs/REVIEW.md`) answered the open questions of VDS-PRB-001 v0.1 and set the key design choices of VDS-PRC-001 v0.2. Under the normal rules each would be recorded as "Proposed, awaiting Amish". Amish pre-approved every recommendation in this batch run, so each item below is recorded as decided, with its options and the reason for the choice. Choices that touch safety take the conservative option and state what evidence would relax them. Partners and regions are recorded as the first candidate to approach, not as agreed. The TRL 2 approval that the TRL 3 step needs is the same instruction.

## Options considered

*Table 1. Options for each item.*

| # | Item | Options | Chosen |
| --- | --- | --- | --- |
| D1 | Where the water and air lines run | Alongside the rod in clips; inside, each in its own tube; inside, with the rod bore as the air duct and the water in a guide tube | Inside, bore as air duct, water tube in a PTFE guide tube |
| D2 | Rod and joints | Telescopic carbon pole; threaded sections; sections with internal couplers and snap buttons | 6061-T6 tube 38.1 x 1.47 mm in four 1,050 mm sections, internal couplers, V-spring snap buttons, lines left threaded through (tent-pole storage) |
| D3 | Head articulation | Articulating head; fixed head aimed by turning the rod | Fixed head, about 90° view, aimed by turning the rod; articulation left for a later version (cost and patent risk) |
| D4 | Camera | Bare board camera in a self-made sealed head; bought sealed pipe-inspection head in a machined nose | Bought IP68 29 mm AHD 1080p head with 12 LEDs, in a turned aluminium nose |
| D5 | Display | Handheld screen on its own cable; monitor in the surface unit lid; phone or tablet over USB | 7 in AHD monitor with recorder in the lid of the surface unit (one battery, one cable; USB does not reach 7 m) |
| D6 | Audio | None; separate microphone and speaker; one speaker used as both, with push-to-talk | One 20 mm IP67 speaker at the tip used as speaker and microphone, push-to-talk headset at the surface (fitted, not optional, because talk is how the crew judges consciousness before water) |
| D7 | Water delivery | Open drip tip with a roller clamp; IV-style drip set; gravity drip with a fixed capillary ceiling, roller clamp and a bite valve | Gravity drip: bottle, strainer, 600 mm x 0.5 mm capillary, roller clamp, priming stopcock, single-use tube, bite valve parked in the nose |
| D8 | Air supply | Hand bellows; diaphragm pump with a relief valve; centrifugal blower with shut-off at or below 1 kPa | 12 V centrifugal blower chosen by its shut-off pressure, intake filter, flow meter, speed knob |
| D9 | Power | AA cells; power-tool packs; 12.8 V LiFePO4 packs | Two 12.8 V 6 Ah LiFePO4 packs with built-in protection, one fitted and one spare |
| D10 | Tethered crawler block | Share the proposed crawler head interface; stay independent | Independent; no shared head interface, so the RedZone tether odometry question does not arise |
| D11 | Co-design partner and region | Any accredited USAR team; a national fire or civil protection training school in an earthquake-prone country | First candidate to approach: the disaster management training school of the Armed Police Force, Nepal; second: Turkey's AFAD training centres. Not contacted; not partners |
| D12 | Requirements | Keep the TRL 1 set; restate | R2 split into reach (R2) and bends (R11); R5 as a ceiling with a bite valve; R6 adds a blocked-tip limit; R8 as a value-engineering target; R12 two-way voice added |
| D13 | Budget, pitch and problem | Change; keep | Kept: `budget_usd` stays at USD 2,000 as a value-engineering target; pitch and problem unchanged |

## Decision

All items D1 to D13 are decided as chosen in Table 1, by Amish under his 2026-10-03 pre-approval.

*Table 2. Safety choices taken on the conservative side, and what would relax them.*

| # | Conservative choice | Evidence that would relax it |
| --- | --- | --- |
| S1 | Drip ceiling sized for a 2 m water height at 40 °C (twice the allowed height), giving 1.5 mL/min at the normal 1 m and 20 °C | Measured flows at the tip with the bought capillary, and the co-design medical lead's view of the rate to offer |
| S2 | Water only through a bite valve, never an open drip tip | A written medical protocol from the co-design partner that allows another mouthpiece |
| S3 | Blower chosen by shut-off pressure (at most 1 kPa), with no relief valve to fail | None needed; a measured blocked-tip pressure at TRL 4 confirms it |
| S4 | Audio fitted as standard, so the crew can judge consciousness before water | The medical lead's view that another check is enough |
| S5 | LiFePO4 packs with built-in protection, charged only away from the kit | None; this is the lowest-risk common lithium chemistry |
| S6 | The probe is never used as a lever or pry bar; the 300 N pull and 200 N push are the design loads | Measured joint and button strength at TRL 4 |

## Consequences

- VDS-PRB-001 v0.2, VDS-PRC-001 v0.2 and VDS-REQ-001 v0.2 carry these decisions; the TRL 3 versions (v0.3) add the constructable design of VDS-DDR-002.
- R11 (bends) is not met by D2 and D3; it is recorded as a requirement not met, not redesigned at TRL 3.
- `project.yaml`: only the TRL fields, `design_state` and the evidence list change. `budget_usd`, the pitch and the problem are unchanged.
- Nothing here authorizes building or testing; TRL 4 is capped.
