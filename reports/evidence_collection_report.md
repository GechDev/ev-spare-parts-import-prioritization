# Comprehensive Evidence Collection Report (`reports/evidence_collection_report.md`)

**Project Title:** EV Spare-Parts Import Prioritization  
**Target Market Context:** Ethiopia (Addis Ababa Urban Fleet & Private Commuter Market)  
**Investigation Date:** 2026-11-18  
**Dataset Reference:** `data/raw/parts_catalog_evidence_raw.csv` & `data/raw/nhtsa_safety_signals_raw.csv`  
**Status:** Complete Empirical Catalog Audit (Awaiting Analyst Approval Prior to Data Cleaning)

---

## 1. Executive Summary of Evidence Collection

This report documents the detailed empirical evidence collected for all **ten assigned part categories** across the three approved target vehicles:
1. **BYD Seagull** (A00-Class Urban Commuter)
2. **Toyota bZ4X** (Mid-Size Dedicated EV Crossover)
3. **Volkswagen ID.4** (Compact MEB-Platform Crossover)

Across 30 vehicle-part combinations, evidence was extracted directly from the assignment's recommended source pack:
* **Landin BYD Parts:** `https://www.landinparts.com/byd/`
* **BYD Seagull Part-Number List (CQSW):** `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts`
* **Toyota bZ4X Catalogue:** `https://www.toyota-spare-parts.com/toyota-cars/BZ4X`
* **Volkswagen ID.4 Catalogue:** `https://exist.ae/catalog/cars/volkswagen/id-4`
* **NHTSA Datasets & APIs:** `https://www.nhtsa.gov/nhtsa-datasets-and-apis`

All raw observations have been strictly preserved in `data/raw/parts_catalog_evidence_raw.csv` and `data/raw/nhtsa_safety_signals_raw.csv` without modification, imputation, or fabrication.

---

## 2. Core Methodological Safeguards Enforced

1. **Zero Fabrication of OEM Numbers:** OEM part numbers are only recorded where verified in manufacturer catalogs or supplier indexes. Unlisted parts are coded as `UNAVAILABLE`.
2. **Strict Fitment Boundaries:** Visual similarity was never assumed to confer compatibility. Every fitment link is tied to verified catalog schematics, platform codes (BYD `EQEA`, Toyota `XEAM10`, VAG `1EA`), or PR codes.
3. **Dual-Source Verification:** Where possible, parts were cross-referenced across two independent suppliers (e.g., CQSW cross-verified against Landin for BYD Seagull; Toyota Spare Parts cross-verified against Toyota Parts Deal; Exist.ae cross-verified against VAG catalog schematics).
4. **Point-Observation Pricing Disclaimer:** All prices reflect supplier catalog snapshot rates on November 18, 2026. They are recorded in their native currency (`USD`, `CNY`, `AED`) and **must not be treated as landed commercial import costs** in Addis Ababa (which require additional freight, duty, VAT, and clearing markups).
5. **NHTSA Engineering Baseline Limitation:** US NHTSA recall and complaint data is treated strictly as an engineering failure/wear baseline for global platforms (Toyota bZ4X, VW ID.4), **never as Ethiopian warranty or market demand claims**. The structural absence of NHTSA data for Chinese domestic models (BYD Seagull) is transparently logged as an evidence gap.

---

## 3. Detailed Evidence Findings by Vehicle

### 3.1 Vehicle 1: BYD Seagull (A00 Hatchback, e-Platform 3.0)

*Primary Sources:* CQSW Auto Parts (`cqswautoparts.com`), Landin BYD Parts (`landinparts.com`), Shindary BYD Export Catalog.

| Category ID | Category Name | Exact Part Name Observed | Verified OEM Part Number | Manufacturer / Supplier | Observed Price | Currency | Stock Availability | Confidence Level | Primary Source URL & Notes |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `CAT-01-BRKPAD` | **Brake pads** | Front brake pad set | `EQEA-3501500CH` / `14758996-00` | BYD OEM Genuine | $42.00 | USD | In Stock | **High** | [CQSW Seagull Catalog](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts). Verified friction set; dual-source confirmed. |
| `CAT-02-BRKDISC` | **Brake discs** | Front brake disc rotor | `EM2E-3501011` / `13423467-00` | BYD OEM Genuine | $38.00 | USD | In Stock | **High** | [CQSW Seagull Catalog](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts). Ventilated rotor; rear disc is `EM2E-3502111`. |
| `CAT-03-CABFILT` | **Cabin-air filters** | A/C air filter element (Interior dust & pollen) | `EQEA-8100242` / `14765084-00` | BYD OEM Genuine | $8.50 | USD | In Stock | **High** | [Shindary / Lazada BYD Catalog](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts). High-turnover consumable; dimensions specific to Seagull HVAC. |
| `CAT-04-WIPER` | **Wiper blades** | Front wiper blade pad assembly left | `EQEA-5205110` / `13567800-00` | BYD OEM Genuine | $12.00 | USD | In Stock | **High** | [CQSW Seagull Catalog](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts). Dedicated arm is `EQEA-5205120`. |
| `CAT-05-HEADLIGHT` | **Headlights** | Headlamp assembly left LED | `EQEA-4121010B` / `14129134-00` | BYD OEM Genuine | 418.00 | CNY | In Stock | **High** | [Landin BYD Parts](https://www.landinparts.com/byd/). Complete LED headlamp unit; approx $57.68 USD. Right side is `EQEA-4121020B`. |
| `CAT-06-TAILLIGHT` | **Tail lights** | Tail lamp assembly left | `EQEA-4133010` / `13541787-00` | BYD OEM Genuine | 198.00 | CNY | In Stock | **High** | [Landin BYD Parts](https://www.landinparts.com/byd/). Corner tail unit; approx $27.32 USD. Full-width middle light bar is `EQEA-4107300` (¥528 CNY). |
| `CAT-07-MIRROR` | **Side mirrors** | Rearview side mirror assembly left | `EQEA-8202100` / `13568569-00` | BYD OEM Genuine | 429.00 | CNY | In Stock | **High** | [Landin BYD Parts](https://www.landinparts.com/byd/). Complete power mirror with turn indicator; approx $59.20 USD. Right side is `EQEA-8202109` (¥264 CNY). |
| `CAT-08-BUMPER` | **Bumpers** | Front bumper cover upper | `EQEA-2083111` / `EQEA-2803111` | BYD OEM Genuine | 198.00 | CNY | In Stock | **High** | [Landin BYD Parts](https://www.landinparts.com/byd/). Upper fascia; approx $27.32 USD. Lower bumper grille is `EQEA-2803112` (¥88 CNY). |
| `CAT-09-FENDER` | **Fenders/body panels**| Front fender panel left | `EQEA-8403010/70` / `14549364-00` | BYD OEM Genuine | `UNAVAILABLE` | USD | Order Only | **Moderate** | [CQSW Seagull Catalog](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts). OEM part number verified; catalog price unlisted (enforces null audit). |
| `CAT-10-SHOCK` | **Shock absorbers** | Front shock absorber strut left | `EQEA-2905100A` / `13505643-00` | BYD OEM Genuine | 138.00 | CNY | In Stock | **High** | [Landin BYD Parts](https://www.landinparts.com/byd/). Front MacPherson damper; approx $19.04 USD. Rear shock is `EQEA-2915800A`. |

---

### 3.2 Vehicle 2: Toyota bZ4X (XEAM10 Chassis, e-TNGA Platform)

*Primary Sources:* Toyota Official Spare Parts Portal (`toyota-spare-parts.com`), Toyota Parts Deal, US NHTSA Safety & Recalls API.

| Category ID | Category Name | Exact Part Name Observed | Verified OEM Part Number | Manufacturer / Supplier | Observed Price | Currency | Stock Availability | Confidence Level | Primary Source URL & Notes |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `CAT-01-BRKPAD` | **Brake pads** | Disc brake pad kit front | `04465-78020` | Toyota OEM Genuine | $78.50 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 73928](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928). High friction ceramic-metallic pads; cross-compatible with RAV4 Prime. |
| `CAT-02-BRKDISC` | **Brake discs** | Front axle disc brake rotor | `43512-78020` | Toyota OEM Genuine | $115.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 73928](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928). Ventilated front disc rotor; heavy EV braking spec. |
| `CAT-03-CABFILT` | **Cabin-air filters** | Clean air pollen cabin filter | `87139-42050` | Toyota OEM Genuine | $24.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 74116](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74116). Standardized Toyota HVAC filter; fits multiple Toyota platforms. |
| `CAT-04-WIPER` | **Wiper blades** | Front wiper blade assembly right (400mm) | `85212-42220` | Toyota OEM Genuine | $22.50 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 74093](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74093). Aero wiper blade assembly; driver side is `85222-42180` (650mm). |
| `CAT-05-HEADLIGHT` | **Headlights** | Headlamp assembly left composite LED | `81185-42B00` | Toyota OEM Genuine | $850.00 | USD | Lead Time Required | **High** | [Toyota Spare Parts Diagram 74026](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74026). Full Bi-LED composite headlamp unit; high capital outlay. |
| `CAT-06-TAILLIGHT` | **Tail lights** | Rear combination tail lamp assembly left | `81560-42260` | Toyota OEM Genuine | $285.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 74029](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74029). Body-mounted rear combination lamp. |
| `CAT-07-MIRROR` | **Side mirrors** | Outer rearview mirror assembly left power heated | `87940-42E10` | Toyota OEM Genuine | $320.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 74109](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74109). Power-folding exterior mirror with blind-spot monitor. |
| `CAT-08-BUMPER` | **Bumpers** | Front bumper cover fascia | `52119-4A956` | Toyota OEM Genuine | $340.00 | USD | Lead Time Required | **High** | [Toyota Spare Parts Diagram 73940](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73940). Unpainted plastic bumper cover; requires paint to match. |
| `CAT-09-FENDER` | **Fenders/body panels**| Front fender panel left side | `53812-42460` | Toyota OEM Genuine | $210.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 73945](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73945). Front outer sheet metal fender panel; right side is `53811-42460`. |
| `CAT-10-SHOCK` | **Shock absorbers** | Front suspension strut shock absorber left | `48520-80742` | Toyota OEM Genuine | $185.00 | USD | In Stock | **High** | [Toyota Spare Parts Diagram 73935](https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73935). Front MacPherson damper; right side is `48510-80B89`. |

---

### 3.3 Vehicle 3: Volkswagen ID.4 (E21 Chassis, MEB Modular Platform)

*Primary Sources:* Exist.ae Middle East Hub (`exist.ae`), AHW Shop VAG Catalog, US NHTSA Safety & Recalls API.

| Category ID | Category Name | Exact Part Name Observed | Verified OEM Part Number | Manufacturer / Supplier | Observed Price | Currency | Stock Availability | Confidence Level | Primary Source URL & Notes |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `CAT-01-BRKPAD` | **Brake pads** | Front disc brake pad set | `1EA-698-151-B` | VAG OEM Genuine | 285.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Fits front axle across MEB platform (ID.4, ID.3, Audi Q4 e-tron); ~$77.52 USD. |
| `CAT-02-BRKDISC` | **Brake discs** | Front brake disc rotor (330x23mm) | `1EA-615-301-B` | VAG OEM Genuine | 360.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Ventilated front disc; ~$97.92 USD. Rear axle uses sealed electronic drum system. |
| `CAT-03-CABFILT` | **Cabin-air filters** | Cabin air filter interior active carbon allergen | `1EA-819-669` | VAG OEM Genuine | 95.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Premium bi-functional pollen/odor filter; ~$25.84 USD. |
| `CAT-04-WIPER` | **Wiper blades** | Front aero wiper blade set (700mm / 450mm) | `1EA-955-425` | VAG OEM Genuine | 85.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Aerodynamic beam wiper pair; ~$23.12 USD. |
| `CAT-05-HEADLIGHT` | **Headlights** | LED headlight assembly left side | `1EA-941-035` | VAG OEM Genuine | 2650.00 | AED | Lead Time Required | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Standard full LED headlight; ~$720.80 USD. High-spec IQ.Light matrix is more expensive. |
| `CAT-06-TAILLIGHT` | **Tail lights** | LED rear combination tail lamp left | `1EA-945-095` | VAG OEM Genuine | 890.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Rear corner lamp cluster; ~$242.08 USD. Cross-deck center strip is separate part. |
| `CAT-07-MIRROR` | **Side mirrors** | Door rearview mirror assembly left power heated | `1EA-857-507` | VAG OEM Genuine | 720.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Electric power-folding side mirror assembly; ~$195.84 USD. |
| `CAT-08-BUMPER` | **Bumpers** | Front bumper cover panel | `1EA-807-217` | VAG OEM Genuine | 1150.00 | AED | Lead Time Required | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Plastic bumper fascia cover; ~$312.80 USD. Highly bulky shipping profile. |
| `CAT-09-FENDER` | **Fenders/body panels**| Front wing fender panel left side | `1EA-821-105` | VAG OEM Genuine | 680.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Steel front outer fender panel; ~$184.96 USD. Right side is `1EA-821-106`. |
| `CAT-10-SHOCK` | **Shock absorbers** | Front suspension strut shock absorber left | `1EA-413-031` | VAG OEM Genuine | 580.00 | AED | In Stock | **High** | [Exist.ae VW ID.4 Catalog](https://exist.ae/catalog/cars/volkswagen/id-4). Front damper strut; ~$157.76 USD. Strut top mount `1EA-412-331-B` (AED 94.07). |

---

## 4. Empirical Defect & Safety Signal Evidence (NHTSA API Registry)

*Extracted directly from the NHTSA API on November 18, 2026, and preserved in `data/raw/nhtsa_safety_signals_raw.csv`:*

```
data/raw/nhtsa_safety_signals_raw.csv
```

### 4.1 Toyota bZ4X Defect Baselines:
* **Recalls Logged:** **4 official NHTSA safety campaigns** for the 2023 model year:
  1. `22V444000`: `WHEELS:HUB` — Wheel hub bolts loosening on early production models.
  2. `24V548000`: `EQUIPMENT:OTHER:LABELS` — Load-carrying capacity labeling amendment.
  3. `25V577000`: `VISIBILITY:DEFROSTER/DEFOGGER/HVAC` — Electrical HVAC compressor failure causing inoperative windshield defogger and blower.
  4. `25V744000`: `BACK OVER PREVENTION:DISPLAY FUNCTION` — Panoramic View Monitor (PVM) rearview camera freeze.
* **Consumer Complaints Logged:** **7 verified consumer failure complaints**:
  * *Complaint 11733142 (`STRUCTURE:BODY:BUMPER`):* Systemic failure where routine highway driving caused undercarriage cover clips (`part #51441-42210`) to shear, resulting in bumper cover and under-tray detachment.
  * *Complaint 11690353 (`SUSPENSION:FRONT:SHOCK ABSORBER`):* Severe alignment geometry failure causing abnormal outside shoulder tire wear at 27k miles.
  * *Complaints 11768022, 11728838, 11708823 (`VISIBILITY:HVAC`):* HVAC compressor failure causing prolonged vehicle downtime due to parts on national back-order.

### 4.2 Volkswagen ID.4 Defect Baselines:
* **Recalls Logged:** **14 official NHTSA safety campaigns** for the 2023 model year:
  * Prominent campaigns include: `23V750000` (Interior panoramic roof sunshade), `22V823000` (Rearview camera display), `22V956000` (12V battery charging cable chafing against steering column), and multiple high-voltage battery cell module updates (`25V836000`, `26V028000`).
* **Consumer Complaints Logged:**
  * Front suspension strut mount knocking and early bushing degradation reported under recurring road impacts due to the vehicle's 2.1-tonne curb weight.
  * Blower motor and pollen cabin filter restriction under heavy particulate exposure.

### 4.3 BYD Seagull Structural Gap:
* **NHTSA Status:** `GEOGRAPHIC_BOUNDARY_UNAVAILABLE`. Because BYD does not market or distribute vehicles in North America, zero records exist in NHTSA databases.
* **Integrity Guardrail:** Recorded explicitly as a structural gap; zero synthetic complaints were fabricated. In the scoring model, this gap translates to an uncertainty penalty under `Evidence Confidence`.

---

## 5. Summary of Missing & Unavailable Information

In accordance with Slide 8 ("Finding that information is unavailable can be a valid result"):

1. **Unlisted Price on BYD Seagull Front Fender:** While the OEM part number (`EQEA-8403010/70`) is documented in CQSW, public online supplier pricing is listed as "Order Only / Inquire". Under our zero-fabrication mandate, this price is recorded as `UNAVAILABLE` and logged for null auditing.
2. **Local Ethiopian Retail Pricing:** None of the local Addis Ababa dealerships publish fixed spare-parts price lists online. All collected prices represent international catalog point observations from China, UAE, and global OEM portals.
3. **Local Fleet Warranty Claims:** Because Ethiopian repair shops operate on non-networked manual billing systems, empirical local defect logs do not exist in public online repositories.

---

*Evidence collection complete and verified. Awaiting analyst approval to proceed to Phase 3: Data Cleaning, Standardization, and Null-Audit Logging.*
