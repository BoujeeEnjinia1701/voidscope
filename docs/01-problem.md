---
doc_id: VDS-PRB-001
title: VoidScope problem statement
project: VoidScope
doc_type: Problem statement
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
  change: "TRL 2 populate: constraints tied to requirements, first co-design candidate named, open questions answered by the TRL 2 decisions (VDS-DDR-001)"
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: "TRL 3: budget worded as a value-engineering target; safety section added; no change to the problem"
---

# VoidScope problem statement

Local crews reach most collapse survivors first, but they search voids blind and supply survivors by improvisation.

## The problem

Survival after a collapse falls quickly with time. More than 90 per cent of survivors are rescued in the first three days, and most in the first 24 hours by local responders with little equipment ([Gulf News, citing Ilan Kelman, UCL, 2023](https://gulfnews.com/world/mena/why-first-72-hours-are-crucial-for-turkey-syria-quake-rescues-1.1675864021699)). INSARAG medical guidance for entrapped patients recommends starting oral intake where possible, while warning that non-intravenous routes absorb slowly and can cause regurgitation ([INSARAG Medical Working Group, 2023](https://insarag.org/wp-content/uploads/2023/05/Attachment-C2-MWG-The-Medical-Management-of-the-Entrapped-Patient-with-Crush-Syndrome-March-2023.pdf)). Water reaching a survivor early therefore matters, but it has to be given with care.

Commercial search cameras solve the seeing part well. The Leader Cam has a 47 mm head sized for standard 51 mm core holes, 170 degree articulation and two-way audio on a 2.4 m or 3.7 m carbon pole ([Leader](https://www.leader-group.company/en/urban-search-and-rescue-equipment-usar/usar-life-locator-detector-and-search-camera/usar-search-cameras/leader-cam-search-camera-color)); the SearchCam 3000 offers 240 degree articulation and poles up to 4.26 m ([Savox datasheet](https://www.datocms-assets.com/120614/1756472896-savox-searchcam-3000-datasheet-2.pdf)). They cost about $17,500 USD ([Emergency Responder Products](https://emergencyresponderproducts.com/products/leader-cam)) and none of them carries water or air. The gap is a low-cost, open probe that local teams can build, that fits the same core holes, and that turns from a search tool into a supply line once someone is found.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Municipal fire and rescue crews | A camera probe they can afford and repair to search voids before committing to a dig | Urban collapses where no USAR team is nearby in the first hours |
| Volunteer and community emergency response teams | A simple kit that works after short training, with a clear written procedure | Earthquake-prone towns in low and middle income countries |
| Medical lead on a rescue team | A controlled way to give small amounts of water and to ventilate a void while extrication continues | Confined-space medicine alongside the dig |
| USAR trainers | An inexpensive probe for drills and for teaching void search | Training grounds and rubble piles |

## Operating environment

- Collapsed masonry and concrete, with voids reached through gaps or cored holes of about 50 mm (2 in) and larger.
- Dust, water, mud, sharp rebar and broken glass along the probe path.
- Ambient -10 to +45 °C (14 to 113 °F), day and night work, rain.
- No mains power; battery operation for a full shift is needed.
- Unstable structures and aftershocks; the operator stays outside the void.

## Constraints

- Value-engineering target of USD 2,000 in parts for the full kit (a hypothetical control target, not a spending limit; STANDARDS section 18).
- Probe outer diameter at or below 50 mm (target) so it passes a standard 51 mm core hole.
- Commodity parts, hand tools and a basic 3D printer only; hardware under CERN-OHL-S-2.0, software under MIT.
- Water path built from food-grade materials, cleanable and single-use where it touches the survivor.
- Published as an open engineering reference, not as certified rescue or medical equipment.

## Out of scope

- Acoustic, seismic or radar life detection.
- Powered steering or a crawler base in the first version.
- Intravenous fluids, drugs or any medical treatment beyond water and air delivery.
- Certification to any rescue equipment or medical device standard at this TRL.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Leader Cam search camera | Articulating colour camera head (47 mm) on a telescopic carbon pole with two-way audio and LED light | About $17,500 USD; no water or air delivery | [link](https://www.leader-group.company/en/urban-search-and-rescue-equipment-usar/usar-life-locator-detector-and-search-camera/usar-search-cameras/leader-cam-search-camera-color) |
| Savox SearchCam 3000 | Articulating search camera with extension tubes up to 4.26 m, two-way audio and Li-ion power | Closed commercial kit of 18.6 kg in its case; no water or air delivery | [link](https://www.datocms-assets.com/120614/1756472896-savox-searchcam-3000-datasheet-2.pdf) |
| Savox Delsar Life Detector kit | Seismic and acoustic sensors with a control console for locating buried victims | Locates sounds and taps but cannot see into a void or supply the survivor | [link](https://cseis.com/product/savox-delsar-usar-ready-to-deploy-life-detector-kit/) |

## Co-design

An accredited or aspiring USAR team, or a national fire service training academy in an earthquake-prone country, that can test the probe on training rubble and bring a confined-space medicine lead into the design of the water and air lines. The first candidate to approach is the disaster management training school of the Armed Police Force, Nepal, with Turkey's AFAD training centres as the second; neither has been contacted, and neither is a partner (VDS-DDR-001, D11).

Co-design checklist for the first meeting:

- [ ] Confirm the users, the first-hours context and the 51 mm core hole as the common entry size.
- [ ] Ask the medical lead to review the bite valve, the drip ceiling and the rule that water is given only to a conscious person who can drink.
- [ ] Agree a training rubble site and a dust and darkness test box for TRL 4.
- [ ] Confirm the kit can be carried by two people and set up within 3 minutes.

## Questions answered at TRL 2

The open questions of version 0.1 were answered by the TRL 2 decisions of 2026-10-03 (VDS-DDR-001), made under Amish's pre-approval:

- Lines inside or alongside: inside. The rod bore carries the air, and a guide tube inside the rod carries the single-use water tube, so nothing snags on rebar (D1).
- Drip rate and mouthpiece: a gravity drip with a ceiling of 5 mL/min set by a fixed capillary, and a bite valve at the tip so water flows only when the survivor bites and sips (D7). The medical lead's acceptance is a TRL 4 item.
- Articulation: none in the first version; the camera is aimed by turning the rod (D3).
- Tethered crawler block: VoidScope stays independent (D10).
- Trial host: the first candidate to approach is named above.

## Safety

> **Safety:** VoidScope is safety-critical rescue equipment. It is published as an open engineering reference, never as certified rescue equipment, and it is not a medical device. Only trained rescue teams should use it, inside their own incident command and structural safety procedures, and the operator never enters the void. Water can be inhaled by a survivor who is drowsy, injured or lying badly, so water is given only under the direction of the team's medical lead. Air must be clean and at low pressure. The surface unit holds a lithium iron phosphate battery.
