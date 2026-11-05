---
doc_id: VDS-DDR-005
title: VoidScope concept selection
project: VoidScope
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Concept options A, B and C scored; option A proposed, awaiting Amish"
---

# 0005: Concept selection (options A, B and C)

- **Date:** 2026-10-24
- **Status:** Proposed, awaiting Amish. Nothing here is decided.

## Context

Kit 1.9.1 asks for at least two concept options with different working principles, scored against the user requirements (VDS-URS-001) before one is carried forward. The existing design, a rigid sectioned rod with a steerable tip, is option A and is not redesigned. Amish has not declined any option: `docs/REVIEW.md` and the decision records VDS-DDR-001 to VDS-DDR-004 were checked and record only choices made (for example, D3 no articulation at TRL 2, later superseded by decision 3A; the bite valve kept on the nose). The 60 mm valve extension and the valve on the tip housing were options in VDS-DDR-004 that were not chosen; neither is used here.

## Options considered

| Option | Working principle | Weighted score (of 205) |
| --- | --- | --- |
| A | Rigid sectioned rod pushed straight in; steerable tip; bore as air duct | 165 |
| B | Reel-fed glass-fibre push rod that follows the void | 135 |
| C | Tripod and winch lowering a sonde down a vertical hole | 128 |

Scoring and reasons are in VDS-OPT-001 Table 2. All three are modelled at D3 in `cad/src/model.py` and pass `cad/fidelity.json`.

## Decision

Proposed: option A. It leads B by 22 per cent and C by 29 per cent, outside the 10 per cent band, so one option goes forward as a proposal. It is the only option that meets the 4 m horizontal reach (UR-002) and the corner view (UR-011), and its air duct is the rod bore. Suggested grafts, not changes: a reel for the long umbilical (from B) and a tripod guide plate for vertical entry (from C).

`project.yaml` records `concept_chosen: A (proposed)`. If Amish prefers B or C, a redesign is a new instruction.

## Consequences

If A is accepted, nothing changes. If B or C is chosen, PRC, PRS, CAL, the build plan and the BOM are redone for that option.
