---
doc_id: VDS-REG-001
title: VoidScope regulatory and standards register
project: VoidScope
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First issue (kit 1.9.1 upgrade): nine entries, cited with the date checked; classification and certification routes are to assess"
---

# VoidScope regulatory and standards register

Which standards and regulations might apply to VoidScope, where, and what is needed. VoidScope is published as an open engineering reference for a paper concept; nothing here is a claim of compliance, and anything marked "to assess" needs a qualified reviewer before any product claim. Not legal advice. Method: STANDARDS section 23.

> **Safety:** VoidScope is rescue equipment that may supply water and air to a trapped person and carries a lithium battery. This document is an open engineering reference, not certified rescue equipment, not a medical device and not legal advice.

*Table 1. Regulatory and standards register.*

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | Ingress of dust and water into enclosures | The camera head is bought as IP68 and the surface unit case has a lid; the IP rating of the tip housing, sheath and case is a design aim (PR-004) | Design lead | To assess (the bought camera's own rating is a supplier claim) |
| G2 | UN Manual of Tests and Criteria, section 38.3 (lithium battery tests for transport) | International (UN, adopted into air, sea and road rules) | Tests a lithium cell or pack must pass before it is shipped | The two LiFePO4 packs are bought; the supplier should hold the 38.3 report | Design lead | Applies to the bought packs; supplier evidence to request |
| G3 | Cell and pack safety standard for the LiFePO4 pack and its charger | International and market-specific | Safe design of the cells, protection circuit and charger | Packs have built-in protection and a matching charger (build plan stops S2, S3, S8) | Electrical lead | To assess (no standard number chosen) |
| G4 | Regulation (EC) No 1935/2004, materials and articles intended to come into contact with food | European Union | Safety of materials touching food and drink | The bottle, tube, capillary and bite valve touch drinking water; food-grade materials are required by the problem statement constraints | Design lead | Applies as a guide for material choice; to assess for a product |
| G5 | Regulation (EU) 2017/745, medical devices | European Union | Definition and classification of medical devices | The probe delivers water and air to a person; whether that makes it a device is not settled. It is published as a research and educational prototype, not a medical device | Regulatory consultant | To assess (classification with a qualified reviewer) |
| G6 | INSARAG Guidelines | International (UN advisory group) | Methodology for classified urban search and rescue teams and their equipment | A search camera is a technical search tool in a classified team's kit; the guidelines do not certify products | Co-design partner | Does not certify; to assess for team use |
| G7 | NFPA 1670, operations and training for technical search and rescue incidents | United States | Training and operational levels for technical rescue (including structural collapse) | Sets the context for the drill card and procedure, not the design of the probe | Co-design partner | To assess for the procedure and drills |
| G8 | EMC and electrical safety rules for the market of sale | Market-specific | Interference and electrical safety of the monitor, blower and modules | Low-voltage (12.8 V) equipment with a bought monitor and blower | Electrical lead | To assess |
| G9 | Export and import rules for batteries and cameras | Market-specific | Shipping of lithium packs and image sensors | Relevant only if kits are shipped; the design is published, not sold | Project lead | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later. No standard has been identified for the 15 kg carried-load target (PR-016) or the 55 C touch limit (PR-014 uses the burn-threshold figures in VDS-STM-001 Sources, not a product standard).

## Sources

All checked 2026-10-24.

- IEC. IEC 60529:1989+AMD1:1999+AMD2:2013 Degrees of protection provided by enclosures (IP Code). https://webstore.iec.ch/en/publication/2447
- TUV SUD. Lithium battery testing under UN/DOT 38.3 (white paper on the UN Manual of Tests and Criteria section 38.3). https://www.tuvsud.com/en-us/resource-centre/white-papers/lithium-battery-testing
- European Parliament and Council. Regulation (EC) No 1935/2004 on materials and articles intended to come into contact with food. https://eur-lex.europa.eu/eli/reg/2004/1935/oj/eng
- European Parliament and Council. Regulation (EU) 2017/745 on medical devices. https://eur-lex.europa.eu/eli/reg/2017/745/oj (address by the standard ELI pattern; the page was not opened this session)
- INSARAG (International Search and Rescue Advisory Group). INSARAG Guidelines. https://insarag.org
- NFPA. NFPA 1670, Standard on Operations and Training for Technical Search and Rescue Incidents; overview at https://lifesaving.com/issues-safety-rescue/nfpa-1670-standard-for-technical-rescue/
