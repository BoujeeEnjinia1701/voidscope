---
doc_id: VDS-DDR-004
title: VoidScope bite valve access with the steerable tip
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
  change: Amish's decision on register open decision 1 (portfolio decision 46) recorded
---

# 0004: Bite valve access with the steerable tip

- **Date:** 2026-10-03
- **Status:** decided by Amish Chadha, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." For VoidScope this is portfolio decision 46, the recommendation on open decision 1 of VDS-DEC-001 v0.2, taken exactly as worded: "A for the first prototype, B if drills find the valve hard to reach".

## Context

Decision 3A (VDS-DDR-003) added a cable-steered camera tip and kept the water line as it was, so the bite valve still sits in its pocket on top of the nose, 2 mm behind the nose front. The tip now extends 140 mm beyond the valve, and the top of the bending section lies 2.8 mm below it (VDS-DDR-003, T9). A survivor must reach the valve past the steered tip.

## Options considered

*Table 1. Options (no cost or mass stated for any).*

| Option | What it means |
| --- | --- |
| A | Keep the valve on the nose. To offer water the operator steers the tip fully to one side (the camera then sits 109 mm to the side and 51 mm ahead of the nose), and the medical lead confirms in drills that a survivor can reach the valve |
| B | Carry the valve on a 60 mm flexible extension of the water tube clipped along the sheath, so it is the foremost part when the tip is steered aside |
| C | Move the valve onto the tip housing, running the water tube through the bending section |

## Decision

**A for the first prototype; B if the drills find the valve hard to reach.** Nothing in the model, the BOM or the drawings changes. The water line, the capillary ceiling and the bite valve pocket stay as built in VDS-DDR-002 and VDS-DDR-003. The way water is offered changes in the documents:

- To offer water, the operator steers the camera tip fully to one side and locks it, so the bite valve on top of the nose is the foremost part a survivor can reach (build plan safety stop S7, concept VDS-PRC-001).
- A new first check in the build plan (section 5, "Bite valve access") is run in drills with the team's medical lead: a volunteer lying in a mock void reaches, pulls out and bites the valve past the steered tip, with the tip steered to each side.
- If the medical lead finds the valve hard to reach, option B (a 60 mm flexible extension clipped along the sheath) is the fallback. It comes back to Amish with what the drills found, its cost and its effect on the water set change time (R10).

## Consequences

*Table 2. Results.*

| Item | Result |
| --- | --- |
| Requirements | Unchanged: eleven of twelve met on paper, R9 estimated |
| Cost | USD 1,780, unchanged (value-engineering target USD 2,000) |
| Model, drawings, media | Unchanged; no re-render needed |

- With the tip steered fully aside, the camera looks sideways, 109 mm off the nose. It may no longer show the survivor's mouth while they drink, so the operator may have only the voice link to judge coughing or choking. The drills record whether a partly steered tip keeps the survivor in view and still leaves the valve within reach. This is a drill item for the medical lead, not a new decision.
- C stays not recommended: the water tube would flex at every bend and be harder to change and keep clean (R10).

## Safety

> **Safety:** Water can be inhaled by a survivor who is drowsy, injured or lying badly. The risk of aspiration is not reduced by this decision. Water is offered only under the direction of the team's medical lead, only to a conscious person who can speak and drink, only by the gravity drip through the bite valve with the capillary in the line, and never under pressure. The operator steers the tip aside and locks it before water is offered, keeps talking with the survivor while they drink, and shuts the roller clamp at any cough, choking or loss of response. Reaching the valve is confirmed in drills with the medical lead before any use. VoidScope is not certified rescue equipment and is not a medical device.
