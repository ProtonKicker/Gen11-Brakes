# Dura-Bar 80-55-06 Ductile Iron — Material Data & CCT/TTT Request

Compiled: 2026-11-08
Source receipt: `misc/Order Confirmation # 10119376.pdf`

---

## 1. Purchase details (for the spec-sheet request)

| Field | Value |
|---|---|
| Sales Order # | **10119376 Rev 0** |
| Date ordered | 13-OCT-2026 |
| Customer No. | 418558 |
| PO Number | CALSOL M.TEO 10 13 2026 |
| Product | RND A/C 80-55-06, 18.000" OD × 0.500" L, saw cut (2 EA) |
| Vendor | Dura-Bar Metal Services (Woodstock, IL) |
| Inside sales rep | Deborah O'Donnell — odonnelld@dura-barms.com |
| Corporate | Dura-Bar — 800-BAR-MILL (227-6455), sales@dura-bar.com |

**Important:** TTT/CCT diagrams are **not published** — they are melt/heat-specific and only issued by Dura-Bar's metallurgy/engineering dept on request (via purchase order number). Requested data would typically include the actual heat's ladle chemistry + transformation info.

## 2. How to file the request

**Ready-to-send email to the inside sales rep (recommended):**

**To:** Deborah O'Donnell <odonnelld@dura-barms.com>
**Subject:** Material data request — Dura-Bar 80-55-06, Sales Order 10119376

```
Hi Deborah,

We purchased Dura-Bar 80-55-06 ductile iron from you under Sales Order #10119376 Rev 0
(PO: CALSOL M.TEO 10 13 2026, Customer No. 418558):

- Product: 80-55-06, 18.000" OD round x 0.500" L, saw cut, 2 EA

For our design work and thermal FEA on parts machined from this bar, we need the
following from the mill:

1. The heat/lot number(s) for the bars on this order, plus the material test
   report / certification (actual ladle chemistry and mechanical properties,
   not just the grade minimums).
2. The CCT (continuous cooling transformation) and TTT (isothermal transformation)
   diagrams for this grade/heat chemistry, if available.
3. Any guidance on microstructure/property changes from annealing this grade
   (we'll be heat-treating the parts).

PDFs or email attachments are fine. Happy to provide more order detail if needed.

Thanks,
Tovi Ding
tovi@berkeley.edu
DMS-UNIV CA Berkeley
```

Preferred: **Ask your inside sales rep directly** (fastest — they can pull the cert/heat data):
- Deborah O'Donnell — odonnelld@dura-barms.com (above PO refs)

Via website form (general request/quote form, distributor side):
- URL: https://www.dura-barms.com/request-a-quote
- Fields: FirstName, LastName, Company, Address, City, StateProvince, ZipPostalCode, Country, Email, Phone, product checkboxes, Comment/Message.
- Note: form is Kentico + reCAPTCHA v3, so it must be submitted in a real browser (cannot be scripted).
- Suggested Comment text (copy-paste):

```
Material spec-sheet / metallurgical data request for Sales Order 10119376 Rev 0
(Customer 418558, PO: CALSOL M.TEO 10 13 2026).

Product: Dura-Bar 80-55-06 ductile iron, 18.000" OD x 0.500" L saw cut, 2 EA.

We need the material test report / certification for this heat, and specifically
the CCT and TTT (isothermal transformation) diagrams for this grade/heat chemistry,
plus the actual heat chemistry. We are evaluating thermal cycling of a brake rotor
machined from this bar and need transformation data for FEA validation.
Thank you.
```

Corporate technical contacts (manufacturer):
- https://www.dura-bar.com/resources/metal-experts/technical-team
- Toll free 800-BAR-MILL, fax 815-338-1549, sales@dura-bar.com

## 3. Chemical composition (published grade minimums, as-cast)

| Element | % |
|---|---|
| Carbon* | 3.50 – 3.90 |
| Silicon* | 2.25 – 3.00 |
| Manganese | 0.15 – 0.35 |
| Sulfur | 0.025 max |
| Phosphorus | 0.05 max |

*Carbon/silicon targets vary by bar size. Mg added as inoculant for nodular graphite; small alloying additions stabilize pearlite. Actual heat chemistry is what the certification will show — that's the value of the request.

## 4. Microstructure

- Nodular graphite Type I & II per ASTM A247.
- Matrix: ferrite + ~5–25% pearlite (partially pearlitic; more pearlite = higher strength/wear than ferritic grade).
- Rim has higher nodule count, mostly ferrite; chill carbides < 5% at 100x.
- As-cast hardness 187–255 BHN.

## 5. Mechanical properties (grade minimums)

| Property | Value |
|---|---|
| Tensile strength (min) | 80,000 psi (552 MPa) |
| Yield strength (min) | 55,000 psi (379 MPa) |
| Elongation (min) | 6% (4% under 1.5" dia) |
| Hardness | 187–255 BHN |

## 6. Heat treatment relevance (why annealing matters here)

From Dura-Bar Heat Treat Guide:
- **Subcritical anneal** (1300–1400°F, furnace cool <650°F): spheroidizes pearlite, softens to 135–180 BHN.
- **Full anneal** (1550–1700°F, 1 hr/in, furnace cool <650°F): converts matrix fully to ferrite, 130–180 BHN — this lowers yield strength vs as-cast, matching the team's observation that annealing dropped FOS.
- As-cast 80-55-06 can also be oil-quench hardened from 1600°F to 50 Rc min (OD).
- Jominy end-quench curves: in the heat treat guide (hardness vs distance for hardenability).

## 7. Files in this folder

- 80-55-06-product-brief.pdf — official grade brief (composition, microstructure, mechanicals)
- ductile-iron-resource-guide.pdf — grade overview + stock lists
- dura-bar-heat-treat-guide.pdf — annealing/heat-treat cycles, Jominy data
- FINDINGS.md — this document

## 8. Sources

- https://www.dura-bar.com/products/ductile-iron/80-55-06
- 80-55-06 Product Brief (dur-bar.com getmedia ca3b3f47...)
- Dura-Bar Heat Treating Guide (dur-bar.com getmedia 5cf7c409...)
- Dura-Bar Ductile Iron Resource Guide (dura-barms.com)
- https://www.dura-barms.com/request-a-quote
- https://www.dura-bar.com/resources/metal-experts/technical-team