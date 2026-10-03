---
doc_id: VDS-REQ-001
title: VoidScope requirements
project: VoidScope
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: "TRL 2: R2 split into reach (R2) and bends (R11); R5 restated as a ceiling with a bite valve; R6 adds the blocked-tip limit; R8 worded as a value-engineering target; R12 two-way voice added; concept status for each"
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: "TRL 3: status from VDS-CAL-001 on the constructable design (VDS-DDR-002)"
---

# VoidScope requirements

Ten of the twelve requirements are met on paper by the constructable design: seven by calculation and three by design, all to be confirmed by test at TRL 4. R9 (setup in 3 minutes) is estimated at 2.1 minutes but can only be settled by timed drills. R11, following a path with two 45° bends, is not met: the rigid rod of the first version goes straight only.

*Table 1. Requirements and status at TRL 3 (tags in brackets refer to VDS-CAL-001).*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Probe passes a standard core hole | Outer diameter of tip and rod at or below 50 mm | Pass the assembled probe through a 51 mm test ring along its full length | Met: 48 mm at the head, 47 mm at the grip [A1] |
| R2 | Reach into a void along a straight path | Working length of at least 4 m (13 ft) | Measure assembled length from the grip to the tip | Met: 4,063 mm [A4] |
| R3 | See in darkness and dust | Read a 20 mm high letter at 1 m in a dark, dusty test box | Test box with a set dust load and no ambient light | Met on paper: 19 pixels per letter against 10 needed; 7 lx left after 2 m of dusty air [C2, C6]; dust load to test |
| R4 | Survive rubble handling | Head survives 20 drops of 1 m onto concrete and 1 m water immersion for 30 minutes | Drop and immersion tests followed by a video check | By design: IP68 camera, aluminium head with 2.85 mm minimum wall [G2]; to test |
| R5 | Controlled water delivery | Drip from 0 up to a ceiling of no more than 5 mL/min at any allowed height up to 40 °C; no flow when the clamp is closed or the valve is not bitten | Timed collection at the tip at set heights and temperatures | Met: ceiling 1.5 mL/min at 1 m and 20 °C, 4.5 mL/min at 2 m and 40 °C [D1, D2] |
| R6 | Air delivery to the void | At least 20 L/min of filtered air at the tip; never more than 1 kPa above ambient, even with the tip blocked | Flow meter and manometer at the tip, open and blocked | Met: 44 L/min at full speed, 0.9 kPa at shut-off [E3, E5] |
| R7 | Shift-long battery life | At least 4 h of continuous video and light at 20 °C and at -10 °C | Run-down test at 20 °C and at -10 °C | Met: 6.2 h and 4.3 h on one pack [F4] |
| R8 | Cost against the value-engineering target | Full kit parts cost against the USD 2,000 target | Costed bill of materials from named suppliers | USD 1,578, USD 422 under the target [I2, I4] |
| R9 | Quick to deploy | Two trained people assemble and start searching within 3 minutes | Timed drills with a USAR partner | Estimate 2.1 min [H5]; only a timed drill can settle it |
| R10 | Hygienic water path | Water path parts replaceable in under 5 minutes without tools | Timed replacement against a cleaning procedure | By design: single-use water set, about 4 min [D8]; to time |
| R11 | Follow a bent path | Pass a 4 m test channel with two 45° bends | Push through the channel | **Not met.** The rigid rod cannot bend [A6]; a flexible lead section is a later version |
| R12 | Talk with the survivor | Two-way voice between the operator and a person at the tip | Speech test in a rubble box | By design: tip speaker as speaker and microphone, push-to-talk headset |

## Assumptions

- Local crews can open or find gaps of about 50 mm into most voids of interest.
- A rigid, sectioned rod is good enough for a first version; articulation and bends come later (R11).
- A slow gravity drip through a bite valve is an acceptable way to give water when a medical lead directs it; the medical lead's acceptance is a TRL 4 item.
- Commodity sealed pipe-inspection camera heads meet the image, light and sealing targets.

> **Safety:** These requirements describe rescue equipment that delivers water and air to a trapped person and carries a lithium battery. Meeting them on paper does not make the design safe to use. VoidScope is an open engineering reference, not certified rescue equipment and not a medical device; see VDS-PRC-001, Safety.
