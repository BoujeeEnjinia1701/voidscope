---
doc_id: VDS-DDR-006
title: VoidScope STEM check fixes
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
  change: "Two STEM check failures recorded: tip heat (F1) and option B free reach (F2), decided under the standing instruction of 2026-10-23"
---

# 0006: STEM check fixes (kit 1.9.1 upgrade)

- **Date:** 2026-10-24
- **Status:** F1 and F2 decided under Amish's standing instruction of 2026-10-23 (a failed STEM row is fixed in the same session when the fix keeps the working principle, pitch and scope). Not individually approved by Amish.

## Context

VDS-STM-001 screened 26 claims. Two failed in the first pass (F1, F2) and the independent review found three more (F3 to F5, and a corrected criterion for F1). Nothing the check proposed had been declined by Amish (`docs/REVIEW.md` and VDS-DDR-001 to VDS-DDR-005 checked).

## F1: heat in the camera tip (S14)

- **Failure.** The camera and 12 LEDs dissipate 3 W in a sealed 33 x 71 mm bead-blasted aluminium housing. Natural convection and radiation put the surface at 85 C at 45 C ambient (VDS-CAL-001 K2). The first pass used 55 C (10 s touch of bare metal); the review corrected the criterion to 48 C (10 minute touch, a survivor cannot pull away; F4).
- **Options.** (a) Black anodise the housing (emissivity 0.85) and dim the LEDs by default so the head dissipates 0.8 W; (b) a heat-sink fin on the tip (rejected: it would break the 48 mm envelope and snag rubble); (c) lower the ambient requirement (rejected: changes the scope).
- **Decision.** (a). Result 44.4 C at 35 C ambient and 30 C at 20 C (K5, K4), inside 48 C; 53.9 C at 45 C (K3), where the tip is kept off the survivor. The light margin is about 700-fold in moderate dust, so dimming costs little in the picture (S13); in thick dust the operator raises the LEDs briefly.
- **Consequences.** BOM line 32 notes "black anodised"; anodising is to quote and no price was changed. The build plan (v0.4) adds the finish step; new requirement PR-014. The camera's real power at the dimmed setting is to confirm when bought (VDS-DEC-001 item 15). The tip housing is drawn in the model unchanged (finish only).

## F2: option B free-air reach (SB1)

- **Failure.** A 10 mm glass-fibre rod droops about 93 mm at 1 m carrying a 0.5 kg head and far more beyond.
- **Decision.** Option B is claimed only where the void floor or debris carries the rod; free reach is capped at 1 m. This keeps B's principle and lowers its score for the 4 m reach (UR-002).
- **Consequences.** VDS-OPT-001 scores B 2 of 5 on reach.

## F3: capillary margin (S7)

- **Failure.** Flow goes with the fourth power of the bore. A 0.5 mm capillary 5 per cent oversize passes 5.46 mL/min at 2 m and 40 C, over the 5 mL/min ceiling.
- **Options.** (a) Capillary 750 mm instead of 600 mm; (b) a tighter bore tolerance only (rejected: the margin stays near zero); (c) an inline flow limiter (not adopted: an extra part).
- **Decision.** (a). Worst case 4.4 mL/min; ceiling at 1 m and 20 C 1.2 mL/min, about 71 mL an hour. BOM line 11 and the build plan say 750 mm; the price is unchanged (a longer length of the same tube). The drill card keeps "bottle at most 1 m above the tip", measured vertically.

## F5: blocked-tip pressure (S11)

- **Failure.** Shut-off pressure rises with speed squared; on a 12.8 to 14.4 V pack a blower rated 0.9 kPa could reach about 1.1 to 1.3 kPa.
- **Decision.** The blower runs from the converter's regulated output with a fixed speed cap so shut-off is at or under 0.8 kPa. The control modules already carry a blower controller; no part is added. PR-007 becomes "to verify at TRL 4" until the datasheet and a blocked-tip measurement agree.

## Reviewer suggestions not adopted, for Amish

A thermistor cut-back on the tip, a passive relief valve at about 0.8 kPa, a thicker-walled first rod section and a 0.8 mm steering wire were suggested. Each adds a part or changes the design, and the fixes above meet the claims, so they are left as options. The relief valve is the most useful if the blower's shut-off pressure is not confirmed at the speed cap.

## Consequences overall

Working principle, pitch and scope of option A are unchanged; no design dimension changed.
