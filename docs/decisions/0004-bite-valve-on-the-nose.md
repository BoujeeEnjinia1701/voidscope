---
doc_id: VDS-DDR-004
title: VoidScope bite valve kept on the nose
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
  change: Amish's round-2 decision 3A on bite valve access recorded
---

# 0004: Bite valve kept on the nose; steer the tip aside to give water

- **Date:** 2026-10-03
- **Status:** decided by Amish, 2026-10-03 (round 2): "i agree with all the 46 recommendations you provided. please proceed." For VoidScope this is decision 3A, the open decision in VDS-DEC-001 v0.2.

## Context

The steerable camera tip (VDS-DDR-003) extends 140 mm beyond the nose. The bite valve stays on top of the nose, 2 mm behind its front, so a survivor reaches it past the tip and the bending section, whose top is 2.8 mm below the valve.

## Options considered

| Option | What it means |
| --- | --- |
| A (chosen) | Keep the valve on the nose. To offer water, the operator steers the tip fully to one side (the camera then sits 109 mm to the side and 51 mm ahead of the nose); the medical lead confirms in drills that a survivor can reach the valve |
| B | Carry the valve on a 60 mm flexible extension of the water tube clipped along the sheath |
| C | Move the valve onto the tip housing, running the water tube through the bending section (not recommended: the tube would flex at every bend and be harder to change and keep clean, R10) |

## Decision

Option A. No design change: the water line, nose and valve are as in VDS-DDR-003. The changes are written ones:

*Table 1. Changes.*

| Item | Was | Now |
| --- | --- | --- |
| Drill card | None | New: build plan section 5a, "steer the tip aside to give water" |
| Items to confirm | 13 | 14: "Confirm in drills with the medical lead" that a survivor can reach the valve past the steered-aside tip |
| Patent screen list | Focused search to cover articulating camera tips (concept note) | Also listed as an item in the review note, to be searched before public release |

## Consequences

| Item | Result |
| --- | --- |
| Requirements | None changed; R5 (water ceiling) and R11 as before |
| Cost and mass | Unchanged. Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,780 (USD 220 under the target). `budget_usd` unchanged |
| Risk | If drills show the valve is hard to reach, option B is the fallback (a clip and a 60 mm longer water tube) |

## Safety

> **Safety:** VoidScope delivers air and, in drills, water to a person who may be trapped; it carries a lithium iron phosphate battery. Water is offered only when the team's medical lead directs it, the person is conscious, can speak and can drink, and the flow is set from closed. The tip is locked straight before it goes into or out of a hole. It is an open engineering reference, not certified rescue equipment and not a medical device.
