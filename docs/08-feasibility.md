---
doc_id: VDS-FEA-001
title: VoidScope feasibility assessment
project: VoidScope
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade)"
---

# VoidScope feasibility assessment

VoidScope option A is feasible on paper as a hand-built open design with commodity parts and one outside lathe job; the weakest points are the bought camera's real power and sealing, the bite valve and the survivor-facing water line, all of which only TRL 4 tests and a medical lead can settle. Method: STANDARDS section 23.

> **Safety:** VoidScope is rescue equipment that may supply water and air to a trapped person and carries a lithium battery. This document is an open engineering reference, not certified rescue equipment, not a medical device and not legal advice.

*Table 1. Feasibility by aspect (option A, the design of record).*

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A 4.5 m rigid rod passes a 51 mm hole, buckles at 940 N and steers its tip 90 degrees each way; all calculations meet their targets on paper | High | Estimates only; wire breaking load, camera power and cable stiffness are assumed | VDS-STM-001, VDS-CAL-001, D3 model (cad/fidelity.json) |
| Materials | 6061-T6 tube, stainless pins and wire, PA12 printed links, silicone sheath, PTFE guide; all commodity | High | Galvanic attack in a wet shift (STM S16); PA12 links are the new weak point (printed, drop-test at TRL 4) | VDS-STM-001 S16, S6 |
| Manufacturing and assembly | Tube cut with hand tools; turned head, tip housing and tail cap need a lathe (outside shop allowance USD 240); links printed in nylon | Medium | The nose and collar need an offset four-jaw set-up; tolerances on the telescoping fit (0.11 mm a side) are tight | VDS-BLD-001, VDS-DDR-002 |
| Power and controls | One 12.8 V 6 Ah LiFePO4 pack gives 6.2 h of video at 20 C and 4.4 h at -10 C; blower speed set by a knob | High | Cold capacity assumed 70 per cent; charging only above 0 C | VDS-CAL-001 F, STM S15, S17 |
| Water and air delivery | Gravity drip capped at 5 mL/min by a capillary; air through the rod bore at 0.9 kPa at most | Medium | The drip ceiling has a 12 per cent margin at 2 m and 40 C with an oversize bore; bite valve cracking pressure unknown; aspiration is a clinical risk | STM S7, S9, S11, S18; RSK H1 |
| Thermal | Tip housing 44 C at 35 C ambient (54 C at 45 C) after the fix (black anodised, LEDs dimmed) | Medium | Near the limit at 45 C ambient; the real camera power is unknown | VDS-STM-001 S14, VDS-DDR-006 F1 |
| Supply of parts | Every BOM line is a catalogue part or stock; the camera head, monitor and blower are the single-source risks | Medium | Prices are first estimates; no supplier has been asked to quote | bom/bom.csv |
| Cost | USD 1,780 against a USD 2,000 value-engineering target | High | Control target, not a limit; B and C probe parts unpriced | bom/bom.csv, VDS-OPT-001 |
| Use and training | Two people, 2.2 min estimated setup; written drill card | Medium | Only timed drills settle it; needs a trained team | VDS-BLD-001 5a |

Ratings: High, Medium, Low. No aspect is rated Low.
