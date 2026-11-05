---
doc_id: VDS-PLN-001
title: VoidScope project plan
project: VoidScope
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade)"
---

# VoidScope project plan

VoidScope is at stage P3 (paper proof of concept, TRL 3) with the design of record, option A, modelled at D3; the next gate is Amish's decision on the concept choice (VDS-DDR-005) and the portfolio's lift of the TRL 3 cap, which opens P4. Method: STANDARDS sections 19 and 23.

> **Safety:** VoidScope is rescue equipment that may supply water and air to a trapped person and carries a lithium battery. Nothing here shows that it is safe to use. It is an open engineering reference, not certified rescue equipment and not a medical device.

## Workstreams

*Table 1. Workstreams.*

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| STEM check and calculations | Design lead | VDS-STM-001, VDS-CAL-001 (sections A to K) | Done at P3; reviewed by an independent reviewer |
| Concept options | Design lead | VDS-OPT-001, VDS-DDR-005 (A, B, C modelled at D3) | Done; choice awaiting Amish |
| Requirements | Design lead | VDS-URS-001, VDS-PRS-001, VDS-RTM-001 (generated) | Done |
| CAD at D3 | Design lead | `cad/src/model.py`, STEP, STL, drawing VDS-DWG-001, `cad/fidelity.json` | Done |
| Build plan and bill of materials | Builder | VDS-BLD-001, `bom/bom.csv` (34 lines, USD 1,780) | Done on paper |
| Regulatory, feasibility, risk, market | Project lead | VDS-REG-001, VDS-FEA-001, VDS-RSK-001, VDS-MKT-001 | First issue; REG items to assess |
| Co-design | Project lead | A partner and a medical lead | Not started (candidates named, not contacted) |
| Prototype build and tests | Builder and partner | Not planned beyond TRL 3 | On hold under the portfolio cap |

## Resources needed

*Table 2. Resources. Planned work beyond TRL 3 is listed for planning only and is not started.*

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead | Decisions, document upkeep | To estimate | Not costed |
| Regulatory reviewer | Classification and standards review (REG G1 to G9) | To assess | To assess |
| Medical lead (co-design) | Review of the water and air lines | To assess | To assess |
| Parts for a prototype (P4, on hold) | The bill of materials | Per BOM | 1,780 (control target 2,000) |

## Stage gates

*Table 3. Stages (P4 to P6 on hold while the stage cap is P3).*

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P3 paper proof of concept | STM done, options scored, URS and PRS traced, D3 model passes `cad_check`, build plan and BOM | Reached 2026-10-24 |
| P4 prototype | Amish lifts the cap; co-design partner and medical lead named | On hold |
| P5 and P6 | As STANDARDS section 19; planned only | On hold |

## Next steps and decision requested

1. Amish to decide the concept choice (option A recommended, VDS-DDR-005), the camera tip finish and LED dimming (VDS-DDR-006 F1, decided under the standing instruction) and the other items in VDS-DEC-001.
2. Approach the first co-design candidate (Nepal Armed Police Force training school) so a medical lead can review the water line.
3. Confirm the parts listed in VDS-DEC-001 "To confirm when parts are bought" with supplier data.
4. Run the focused patent search before any public release (VDS-RSK-001 R6).

## References

- Sphere Association. Water supply standard 1: access and water quantity. https://sphereprototype.conted.ox.ac.uk/standards/watersupply/accessAndWaterQuantity.html
- IEEE Product Safety Technical Committee. Accessible hot surfaces and burn hazards. https://ewh.ieee.org/r4/chicago/pstc/content/Accessible-hot-surfaces-and-burn-hazards.pdf
- Kelman, Ilan. Quoted in "Why first 72 hours are crucial for Turkey-Syria quake rescues." Gulf News, 2023. https://gulfnews.com/world/mena/why-first-72-hours-are-crucial-for-turkey-syria-quake-rescues-1.1675864021699
- INSARAG Medical Working Group. The Medical Management of the Entrapped Patient with Crush Syndrome. March 2023. https://insarag.org/wp-content/uploads/2023/05/Attachment-C2-MWG-The-Medical-Management-of-the-Entrapped-Patient-with-Crush-Syndrome-March-2023.pdf
- Leader Group. Leader Cam search camera. https://www.leader-group.company/en/urban-search-and-rescue-equipment-usar/usar-life-locator-detector-and-search-camera/usar-search-cameras/leader-cam-search-camera-color
- Savox Communications. SearchCam 3000 datasheet. https://www.datocms-assets.com/120614/1756472896-savox-searchcam-3000-datasheet-2.pdf
- Emergency Responder Products. Leader Cam. https://emergencyresponderproducts.com/products/leader-cam
- AllSafe Industries. SearchCam 3000 kit (quote only). https://allsafeindustries.com/searchcam-3000-search-rescue-camera-kit.aspx
- IEC. IEC 60529 (IP code). https://webstore.iec.ch/en/publication/2447
- European Parliament and Council. Regulation (EC) No 1935/2004. https://eur-lex.europa.eu/eli/reg/2004/1935/oj/eng
- European Parliament and Council. Regulation (EU) 2017/745. https://eur-lex.europa.eu/eli/reg/2017/745/oj
- INSARAG. Guidelines. https://insarag.org
- NFPA 1670 overview. https://lifesaving.com/issues-safety-rescue/nfpa-1670-standard-for-technical-rescue/
- TUV SUD. Lithium battery testing under UN/DOT 38.3. https://www.tuvsud.com/en-us/resource-centre/white-papers/lithium-battery-testing
