---
doc_id: VDS-REQ-001
title: VoidScope requirements
project: VoidScope
doc_type: Requirements
version: "0.4"
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
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: "R11 restated by Amish (decision 3A) as seeing around a 45-degree bend from a straight hole, with a test-box verification; met on paper by the steerable camera tip (VDS-DDR-003); status of R1, R2, R4, R8 and R9 updated from VDS-CAL-001 v0.2"
---

# VoidScope requirements

Eleven of the twelve requirements are met on paper by the constructable design with its steerable camera tip: eight by calculation and three by design, all to be confirmed by test at TRL 4. R9 (setup in 3 minutes) is estimated at 2.2 minutes but can only be settled by timed drills. R11 was restated on 2026-10-03 by Amish, who chose option A for it ("3A", in his reply "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"): instead of following a channel with two 45° bends, the probe goes in straight and its camera tip, steered from the handle, looks around a 45° bend. The rigid rod, the air path through its bore and the water tube to the bite valve are unchanged.

*Table 1. Requirements and status at TRL 3 (tags in brackets refer to VDS-CAL-001).*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Probe passes a standard core hole | Outer diameter of tip and rod at or below 50 mm | Pass the assembled probe through a 51 mm test ring along its full length | Met with the tip locked straight: 48 mm at the head and tip, 47 mm at the grip [A1]. The handle-end fittings (the tail cap's air barb and now the steering control) are wider and stay outside the hole |
| R2 | Reach into a void along a straight path | Working length of at least 4 m (13 ft) | Measure assembled length from the grip to the tip | Met: 4,203 mm from the grip; 4,131 mm can go in before the steering control reaches the hole [A4g, A4] |
| R3 | See in darkness and dust | Read a 20 mm high letter at 1 m in a dark, dusty test box | Test box with a set dust load and no ambient light | Met on paper: 19 pixels per letter against 10 needed; 7 lx left after 2 m of dusty air [C2, C6]; dust load to test |
| R4 | Survive rubble handling | Head survives 20 drops of 1 m onto concrete and 1 m water immersion for 30 minutes | Drop and immersion tests followed by a video check | By design: IP68 camera in an aluminium tip housing, sheathed bending section, nose with 2.85 mm minimum wall [G2]; to test, with the tip straight and bent |
| R5 | Controlled water delivery | Drip from 0 up to a ceiling of no more than 5 mL/min at any allowed height up to 40 °C; no flow when the clamp is closed or the valve is not bitten | Timed collection at the tip at set heights and temperatures | Met: ceiling 1.5 mL/min at 1 m and 20 °C, 4.5 mL/min at 2 m and 40 °C [D1, D2] |
| R6 | Air delivery to the void | At least 20 L/min of filtered air at the tip; never more than 1 kPa above ambient, even with the tip blocked | Flow meter and manometer at the tip, open and blocked | Met: 44 L/min at full speed, 0.9 kPa at shut-off [E3, E5] |
| R7 | Shift-long battery life | At least 4 h of continuous video and light at 20 °C and at -10 °C | Run-down test at 20 °C and at -10 °C | Met: 6.2 h and 4.3 h on one pack [F4] |
| R8 | Cost against the value-engineering target | Full kit parts cost against the USD 2,000 target | Costed bill of materials from named suppliers | USD 1,780, USD 220 under the target [I2, I4] |
| R9 | Quick to deploy | Two trained people assemble and start searching within 3 minutes | Timed drills with a USAR partner | Estimate 2.2 min [H6]; only a timed drill can settle it |
| R10 | Hygienic water path | Water path parts replaceable in under 5 minutes without tools | Timed replacement against a cleaning procedure | By design: single-use water set, about 4 min [D8]; to time |
| R11 | See around a 45-degree bend from a straight hole (restated 2026-10-03, Amish, decision 3A) | With the probe pushed straight through a 51 mm hole, steer the camera to look down a passage that turns 45° to either side and read what is there | Test box: a 51 mm hole into a straight passage 300 mm wide that turns 45° 0.5 m beyond the hole. Push the probe straight in, steer the tip from the handle and read 20 mm letters 1 m down the turned passage on the monitor; repeat to the other side; straighten the tip and withdraw it through the hole | Met on paper: the tip bends up to 90° each way [J3]; bent 45° it needs 83 mm to the side [J6] and a 20 mm letter at 1 m gets 19 pixels [C2] |
| R12 | Talk with the survivor | Two-way voice between the operator and a person at the tip | Speech test in a rubble box | By design: tip speaker as speaker and microphone, push-to-talk headset |

## Assumptions

- Local crews can open or find gaps of about 50 mm into most voids of interest.
- A rigid, sectioned rod is good enough for a first version, with a camera tip that bends in one plane; turning the rod chooses the plane. Following a bent channel with the rod itself is not required (R11 as restated).
- A slow gravity drip through a bite valve is an acceptable way to give water when a medical lead directs it; the medical lead's acceptance is a TRL 4 item.
- Commodity sealed pipe-inspection camera heads meet the image, light and sealing targets.

> **Safety:** These requirements describe rescue equipment that delivers water and air to a trapped person and carries a lithium battery. The steerable tip must be locked straight before it goes into or comes out of a hole. Meeting them on paper does not make the design safe to use. VoidScope is an open engineering reference, not certified rescue equipment and not a medical device; see VDS-PRC-001, Safety.
