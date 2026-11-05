---
doc_id: VDS-MKT-001
title: VoidScope market and viability
project: VoidScope
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): three segments, cited benchmarks with the date checked, open route"
---

# VoidScope market and viability

Municipal fire crews, volunteer rescue teams and USAR training schools in earthquake-prone countries pay tens of thousands of dollars for a search camera that carries no water or air, or cannot afford one; an open probe that a workshop can build for about USD 1,780 in parts (a control target of USD 2,000) fills that gap, and the open files let each team repair and adapt it. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

> **Safety:** VoidScope is rescue equipment that may supply water and air to a trapped person and carries a lithium battery. Nothing here shows that it is safe to use. It is an open engineering reference, not certified rescue equipment and not a medical device.

*Table 1. Market segments.*

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Municipal fire and rescue services | Towns in earthquake-prone low and middle income countries with no USAR team nearby | Leader Cam: about USD 17,500 (Emergency Responder Products, as cited in VDS-PRB-001, checked 2026-10-03; the page could not be reopened on 2026-10-24) | 1,780 parts (bom/bom.csv); 1,540 if the builder has a lathe | Fits the same 51 mm core holes at a tenth of the price, and adds water and air delivery |
| Volunteer and community response teams | Community emergency response teams, NGOs, humanitarian organisations | SearchCam 3000: quote only, no price listed (allsafeindustries.com, checked 2026-10-24). Zistos TaskForceHD: no price listed (Firehouse product page, checked 2026-10-24) | 1,780 parts | A kit a team can build, repair and learn on, with a written procedure |
| USAR training schools and trainers | National fire academies, training grounds | Same commercial cameras, price not published | 1,780 parts | Affordable for drills, so a real camera is not risked on a rubble pile |

The competitive pricing evidence is thin: one cited price and two products that do not publish one. A procurement quote for each commercial camera is "to assess" before any price comparison is made in public. Differences that do not depend on price: the commercial cameras are certified or field-proven products; VoidScope is a paper concept at TRL 3 and an open reference, not certified equipment.

## Open route

Builders would be workshops, makerspaces, university engineering departments and NGOs, working from the build plan (VDS-BLD-001), the bill of materials and the drawings under CERN-OHL-S-2.0 (hardware) and MIT (software). The design spreads through the repository, training schools and rescue-sector networks; a co-design partner (VDS-PRB-001) would test it on training rubble first. What keeps it open: the licence, the status statement in every document, and no certification claim. A commercial or certified version would be a separate effort that someone else could take on from the files, which is outside this plan.

## Viability

Technically feasible on paper (VDS-FEA-001). The unit economics are a parts cost, not a business case: no sales, support or certification cost is estimated here and none is planned. Viability depends on a co-design partner, a medical lead's review of the water line and TRL 4 tests, none of which has started.

## Sources

All checked 2026-10-24 unless stated.

- Emergency Responder Products. Leader Cam search camera. https://emergencyresponderproducts.com/products/leader-cam (price of about USD 17,500 as recorded in VDS-PRB-001 on 2026-10-03; not reopened for this note).
- AllSafe Industries. SearchCam 3000 Search and Rescue Camera Kit ("Quote Required"). https://allsafeindustries.com/searchcam-3000-search-rescue-camera-kit.aspx
- Firehouse. Product of the Day: TaskForceHD System for Technical Search Specialists, Zistos Corporation (no price stated). https://www.firehouse.com/rescue/technical-rescue/product/21233264/zistos-corporation-taskforcehd-system-for-technical-search-specialists-from-zistos-corporation
- Leader Group. Leader Cam search camera. https://www.leader-group.company/en/urban-search-and-rescue-equipment-usar/usar-life-locator-detector-and-search-camera/usar-search-cameras/leader-cam-search-camera-color
- Savox Communications. SearchCam 3000 datasheet. https://www.datocms-assets.com/120614/1756472896-savox-searchcam-3000-datasheet-2.pdf
