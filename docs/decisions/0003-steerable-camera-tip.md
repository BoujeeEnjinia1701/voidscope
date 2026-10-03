---
doc_id: VDS-DDR-003
title: VoidScope steerable camera tip (R11)
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
  change: "Amish's requirement decision 3A carried out: cable-steered camera tip, R11 restated, the changes it needed and their results"
---

# 0003: Steerable camera tip (R11)

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish on 2026-10-03, who chose option A on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". Decision 3A is VoidScope's.

## Context

At TRL 3 the constructable design (VDS-DDR-002) met every requirement but R11, "pass a 4 m test channel with two 45° bends". The rigid rod goes straight only, and a flexible lead section had been left to a later version (VDS-DDR-001 D12). Option A, which Amish chose, keeps the rigid rod and instead lets the camera look around a bend: a cable-steered articulating camera tip that bends up to 90° each way, controlled from the handle, with R11 restated as "see around a 45-degree bend from a straight hole" and given a verification method. The rigid rod, the air path through its bore and the water tube to the bite valve stay as they are, and the tip must still pass the 51 mm hole.

## Options considered

The options were put to Amish with the requirement decisions; he chose A. The design choices below were made to carry A out.

*Table 1. How the tip is built: choices made.*

| Question | Options looked at | Chosen | Why |
| --- | --- | --- | --- |
| Bending section | Notched single tube (laser cut); rolling-contact links; pinned hinge links | Five pinned joints: a turned base link, four printed links and a turned tip housing, joined by 2 mm stainless pins | Pinned links can be printed by any SLS service and built with hand tools; a notched tube needs laser cutting and fatigues |
| Bending planes | One plane (two wires); two planes (four wires) | One plane, sideways (left and right of the bite valve) | R11 needs one plane; turning the rod picks the plane; two wires fit beside the existing lines, four would not |
| Where the camera goes | Keep it in the nose; move it to the tip | In a turned tip housing on the last joint, its window 3 mm behind the front edge | A camera behind the bend cannot see around it |
| How the wires reach the handle | Separate cable outside the rod; inside the rod bore | Two 3 mm PTFE-lined steel-coil housings inside the rod, stopping in the collar's front wall at the head end and in the control body at the handle | No loose cable outside; the housings stay threaded with the other lines (tent-pole storage) |
| Handle control | Bought borescope handle; drum and lever | A printed clamp body on section 4 ahead of the grip, with an 18 mm drum on a shaft, a thumb lever and a friction lock | Built from stock and printed parts; the lever sits where the rear hand's thumb reaches |
| Sealing the joints | Bare links; a sheath | A 0.6 mm silicone sheath over the bending section, replaceable, with a spare in the kit | Keeps grit out of the pins; the camera itself is already IP68 |

## Decision

*Table 2. Changes made to the model, the BOM and the calculations.*

| # | Before | Now | Why |
| --- | --- | --- | --- |
| T1 | Camera in the nose against a 26 mm lip, clamped by a rubber spacer ring | Camera in a tip housing (33 mm outside, 29.3 mm bore, 66 mm long) held by two nylon-tipped M3 grub screws; the spacer ring is gone | The camera must be ahead of the bend |
| T2 | Nose bore 29.3 mm from 12 to 72 mm, then the lip | Nose bore 29.3 mm right through; two M3 tapped holes near the front for the base link's grub screws | Takes the base link's spigot |
| T3 | Nothing ahead of the nose | Base link (turned, 29.25 mm spigot 14 mm into the nose, 33 mm flange), four printed PA12 links (33 mm outside, 23 mm bore, 10 mm bodies, 5.25 mm gaps), tip housing; ten 2 mm pins; nested lugs top and bottom with their ends rounded about the pins | Each joint closes at 18.1°, so five give 90° each way; the rounded lug ends keep neighbouring links clear at full bend (checked in the model at 90° each way) |
| T4 | No steering | Two 0.6 mm 7x7 stainless wires, 14 mm either side of the camera axis, from crimped anchors in the tip housing, through every link and a slanted hole in the base link, along the nose bore and through the collar's front wall into their housings | Pulling one wire bends the tip toward it |
| T5 | No housings in the rod | Two 3 mm housings in the rod bore 10.5 mm either side and 7.5 mm below the axis, clear of the snap button springs (2.0 mm), the coupler bores (0.95 mm), the cable (6.0 mm) and the guide tube (5.0 mm) | The only place in the bore below the spring strips that clears everything |
| T6 | Collar outlets at 0, 45, 135, 225, 270 and 315° | Lower side outlets moved to 240 and 300°; two 3.2 mm housing stops 2 mm deep in the plenum side of the front wall, 1.2 mm wire holes on through the spigot | The housings pass the outlets where 225 and 315° would have put the holes on top of them; six outlets of the same size, so the air path is unchanged |
| T7 | Section 4 plain behind the coupler | Two 4 mm holes on top of section 4, 332 and 368 mm from its back end | Where the housings leave the rod for the control |
| T8 | Nothing on the rod ahead of the grip | Steering control: printed PA12 clamp body 8 mm ahead of the grip, 18 mm aluminium drum on a 6 mm shaft between two cheeks, 50 mm thumb lever, friction lock knob, M4 clamp screw | 71° of lever gives 90° at the tip; about 5 N at the thumb holds it there |
| T9 | Bite valve ending 2 mm behind the nose front | Unchanged position, 2 mm behind the nose front; the tip now extends 140 mm beyond it | The water line is kept as Amish asked; access to the valve is a new open decision (VDS-DEC-001) |
| T10 | Lathe allowance 3 h (USD 180) | 4 h (USD 240) for the base link, tip housing and drum | Three more turned parts |

R11 is restated in VDS-REQ-001 v0.4: "see around a 45-degree bend from a straight hole", verified in a test box with a 51 mm hole into a 300 mm wide passage that turns 45° 0.5 m beyond the hole, reading 20 mm letters 1 m down the turned passage, to each side, then straightening the tip and withdrawing it.

## Consequences

*Table 3. Results (VDS-CAL-001 v0.2).*

| Requirement | Before | Now |
| --- | --- | --- |
| R11, see around a 45° bend (restated) | Not met (rigid rod, old wording) | Met on paper: 90° each way available, 45° needed; bent 45° the tip needs 83 mm to the side; 19 pixels across a 20 mm letter at 1 m |
| R1, 51 mm core hole | 48 mm | 48 mm with the tip locked straight; every tip part inside the outline in the model |
| R2, reach | 4,063 mm from the grip | 4,131 mm can go in before the steering control reaches the hole (4,203 mm from the grip) |
| R9, setup | 2.1 min | 2.2 min (0.1 min to check the steering) |
| R8, cost | USD 1,578 | USD 1,780: Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,780 (USD 220 under the target) |
| Probe mass | 3.66 kg | 4.18 kg (tip 0.28 kg ahead of the nose; housings, wires and control 0.41 kg) |
| Rod buckling | 1,001 N, 5.0 times a 200 N push | 940 N, 4.7 times (longer probe, heavier line) |
| Handling, 3 m unsupported | 34 N at the grip, 2.55 on yield at a button hole | 32 N at the grip, 2.33 on yield |

The model now runs 180 constructability checks, all passing. The new parts to watch at TRL 4 are the printed lugs (8.7 MPa bearing at a 30 N thumb push against the stop, about a fifth of PA12's strength), the 0.6 mm sheath against sharp rubble, the wire's breaking load (a factor of 3.0 assumed) and the camera cable's real bending stiffness, which sets the thumb force. The wires are not self-locking, so a bent tip straightens against the hole's edge if it is pulled back; the procedure is still to steer straight and lock before going in or out.

New for Amish: with the tip 140 mm ahead of the bite valve, the survivor reaches the valve past the camera tip. Options and a recommendation are in the design decisions register (VDS-DEC-001, open decision 1).
