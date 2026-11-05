---
doc_id: VDS-RSK-001
title: VoidScope risk register and hazard analysis
project: VoidScope
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): project risks, preliminary hazard analysis and first-pass design FMEA for option A"
---

# VoidScope risk register and hazard analysis

The top project risks are a missing medical lead to review the water and air lines (R2) and a drip margin of only 12 per cent (R4); the top design FMEA items are F8 bite valve (RPN 60), F5 bending links and pins (RPN 48), F7 capillary and clamp (RPN 40). Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 means the fault is caught before use, 5 means it cannot be seen.

> **Safety:** VoidScope is rescue equipment that may supply water and air to a trapped person and carries a lithium battery. Nothing here shows that it is safe to use. It is an open engineering reference, not certified rescue equipment and not a medical device.

## Project risk register

*Table 1. Project risks.*

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Camera, blower or battery parts differ from the modelled sizes and ratings | Bought parts are single-source and not yet quoted | Redesign of the tip bore, plate layout or lid stack; cost rises | 3 | 3 | Design lead | Confirm each item in VDS-DEC-001 'To confirm' before buying; keep the camera bore a parameter |
| R2 | No co-design partner or medical lead reviews the water and air lines | Neither named candidate has been contacted | Water line cannot move past TRL 3 safely | 3 | 5 | Project lead | Approach the first candidate (VDS-PRB-001); no drill with a person at the tip before review |
| R3 | Tip heat limit missed with the real camera | Camera power at the dimmed setting is not known (STM S14) | Tip too hot to touch at 45 C ambient | 3 | 3 | Design lead | Choose a camera with a dimmer and a datasheet power; thermocouple test at TRL 4 (PR-014) |
| R4 | Drip ceiling margin eroded by a different capillary or bottle height | Margin to 5 mL/min is 12 per cent at 2 m and 40 C with an oversize bore (STM S7) | Water flows faster than intended | 2 | 5 | Design lead | Measure flow at TRL 4; keep the 1 m rule on the drill card |
| R5 | Open design is mistaken for certified equipment | Public hardware files on a rescue topic | Misuse by an untrained team | 3 | 5 | Project lead | Status statement in every document and the README (PR-019); release gate before any public step |
| R6 | Patent in articulating camera tips or combined probes | The patent screen is preliminary (VDS-PRC-001) | Release delayed or design changed | 2 | 3 | Project lead | Focused CPC search before public release; not legal advice |
| R7 | Printed PA12 links fail in drops or bend cycles | New weak point of the tip (STM S6) | Tip stuck or lost in a void | 3 | 3 | Design lead | Drop and cycle tests at TRL 4; spare sheath and links in the kit |
| R8 | Outside lathe work unavailable locally | Nose, collar, tail cap and tip housing need a lathe | Build delayed or a printed fallback needed | 2 | 2 | Builder | Printed or milled fallbacks noted in VDS-DEC-001 value engineering |
| R9 | Cold or heat outside the assumed battery range | Capacity at -10 C taken as 70 per cent (STM S15, S17) | Run time under 4 h | 2 | 3 | Electrical lead | Run-down tests at TRL 4; carry the second pack |

## Preliminary hazard analysis

*Table 2. Hazards (stops S1 to S9 are in the build plan, section 6).*

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Aspiration of water | Survivor drowsy, injured or lying badly; flow too fast; wrong bottle height | Choking, chest infection, death | 5 | 2 | Medical lead directs every use; conscious person who can drink only; gravity drip only; capillary ceiling 5 mL/min sized for 2 m and 40 C; bite valve opens only when bitten; never connect a pump or pressure source (build plan S5, S7, drill card 5a) | Medium; depends on the drill and the medical lead; to review at TRL 4 |
| H2 | Over-pressure or dust in the void from the air line | Blocked outlets; blower too strong; dusty rubble | Barotrauma or choking on stirred dust | 4 | 2 | Blower chosen by its shut-off pressure, 0.9 kPa, run from the regulated converter with a speed cap (fix F5); filter on the intake; flow meter; start at the lowest setting and watch the picture (S4) | Low to medium; shut-off pressure to confirm from the datasheet and measure at a blocked tip |
| H3 | Hot tip touches a survivor | Camera and LEDs dissipate heat in a sealed housing | Contact burn | 3 | 2 | Black anodised housing; LEDs dimmed by default; 44 C at 35 C ambient and 54 C at 45 C (STM S14, fixes F1 and F4); above 35 C the tip is kept off the survivor and steered aside when offering water | Medium; at the limit and to measure |
| H4 | Lithium battery fire or venting | Short circuit, damage, charging below 0 C, wrong charger | Fire, burns, smoke in a rescue area | 4 | 2 | LiFePO4 chemistry; packs with built-in protection; fuse; matching charger; charge away from the kit on a non-combustible surface, never below 0 C (S2, S3, S8) | Low |
| H5 | Collapse or rubble shift during use | Probe used as a lever; operator on unstable debris | Injury to operator or survivor | 5 | 2 | Operator stays outside the void; probe never a lever; the team's structural safety procedures (S6) | Medium; outside the design's control |
| H6 | Sharp edges and rebar | Cut tube ends, rebar, broken glass | Cuts to the operator; probe or sheath torn | 2 | 3 | Edges broken; gloves; the sheath is a spare part | Low |
| H7 | Steered tip bent when withdrawn | Wires are not self-locking; tip left bent in the hole | Tip stuck, wire or link damage, probe stuck | 3 | 3 | Lock straight before in or out (S9); the hole edge straightens a bent tip; wire factor 3 | Low to medium |
| H8 | Lathe, tube cutting and printing during the build | Rotating work, chips, hot nozzle | Injury to the builder | 3 | 2 | Build plan stop S1; guards and eye protection | Low |
| H9 | Contaminated water path | Reused tube, valve or bottle | Infection of a weakened survivor | 4 | 2 | Single-use water set; cleaning kit and procedure; replace in under 5 minutes (PR-011) | Low to medium |
| H10 | Cable or hose snagged on rubble | Lines run outside the void | Probe pulled, camera lost | 2 | 3 | Lines inside the rod and guide tube; hose and cable in an umbilical sleeve | Low |

## Design FMEA (first pass, P3)

*Table 3. Failure modes of option A. RPN = severity x occurrence x detection.*

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Rod sections | Carry the push and bending loads | Buckles or bends | Probe unusable; tip lost in the void | Push above 940 N; a stuck probe pulled hard | 4 | 2 | 3 | 24 | Handbook limits; load test at TRL 4; never use as a lever |
| F2 | Snap button and coupler | Lock the sections | Button fails to engage or shears | Sections separate in the void | Wrong wall thickness; weak button | 5 | 2 | 3 | 30 | Pins shear 6 MPa against 139 MPa; confirm button strength at 300 N (VDS-DEC-001 item 4) |
| F3 | Camera head | See in dark and dust | Sealing fails or the window fogs | No picture | IP68 is a supplier claim | 4 | 3 | 3 | 36 | Immersion and drop tests (PR-004) |
| F4 | Tip housing | Hold the camera and shed its heat | Overheats at 45 C ambient | Burn risk; camera shuts down | 3 W in a sealed 33 mm housing | 4 | 3 | 3 | 36 | Black anodise and dimmed LEDs (fixes F1, F4); thermocouple test (PR-014) |
| F5 | Bending links and pins | Bend the tip 90 degrees | Link cracks or a pin walks out | Tip stuck bent or lost | Printed PA12; 2 mm pins | 4 | 3 | 4 | 48 | Drop and cycle tests; grub screws and sheath retain pins (STM S6) |
| F6 | Steering wire | Pull the tip round | Wire breaks at the thumb stop | Tip loose; cannot steer | Thumb force above 30 N; assumed breaking load wrong | 3 | 2 | 3 | 18 | Factor 3 on an assumed 250 N; confirm the rope (item 10) |
| F7 | Capillary and clamp | Cap the water drip at 5 mL/min | Bore oversize or partly clogged | Flow too fast or too low | Tolerance; debris in the water | 5 | 2 | 4 | 40 | Flow measured at 1 m and 20 C before each use; strainer; bore confirmed when bought (item 6) |
| F8 | Bite valve | Pass water only when bitten | Leaks under head or sticks shut | Water dribbles on a survivor, or none arrives | Cracking pressure below 19.6 kPa | 5 | 3 | 4 | 60 | Check the cracking pressure and the bite in drills with the medical lead (S2, item 7) |
| F9 | Blower | Move 20 L/min at 0.9 kPa at most | Shut-off pressure above the datasheet | Over-pressure in the void | Wrong or substituted part | 5 | 2 | 4 | 40 | Select by shut-off pressure; measure at a blocked tip before use (S4) |
| F10 | Intake filter | Give clean air | Clogged or bypassed | Dusty air or low flow | Heavy dust | 3 | 3 | 2 | 18 | The flow meter shows low flow; spare filter |
| F11 | Battery pack | Power for a shift | Capacity lost in cold; cell fault | Run time under 4 h, or fire | Cold; damage; wrong charger | 4 | 3 | 3 | 36 | Second pack; protection circuit; charge rules (STM S15, S17) |
| F12 | Camera cable | Carry picture and voice | Crushed or pulled at the tail cap | No picture | Snag on rubble | 3 | 3 | 3 | 27 | Grommets and strain relief at the tail cap; spare cable |
| F13 | Monitor and lid | Show the picture | Glare or a cracked screen | Picture unreadable | Sun; a drop | 3 | 2 | 2 | 12 | Lid clearance 19 mm by model; screen shade |
| F14 | Water guide tube | Carry the water tube inside the rod | Kinks or tangles with the cable | Water set cannot be changed | Bore too tight for the lines | 3 | 2 | 3 | 18 | PTFE guide; change procedure in the build plan |

Items with severity 5 (F2, F7, F8, F9) get a TRL 4 test whatever their RPN. Options B and C are not analysed to FMEA depth; their main hazards are recorded in VDS-OPT-001.
