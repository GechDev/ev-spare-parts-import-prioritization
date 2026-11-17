# Source Registry & Provenance Log (`reports/source_log.md`)

**Assignment Requirement:** Slide 6 & 10 ("Record every source URL and collection date. Use at least two sources where possible.")

---

## 1. Master Portal Registry

| Source ID | Platform / Entity | Canonical Base URL | Source Category | Geographic Scope | Role in Analysis | Caveats & Methodological Boundaries |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-VIS-01** | **Adey Market** | `https://adey-market.com/categories/cars?type=cars_electric` | Classified Search Engine | Ethiopia (Addis Ababa) | EV model visibility & dealer marketing volume | **Classified proxy only.** Does not represent vehicle registrations, sales, or total fleet size. |
| **SRC-VIS-02** | **Gezat Electric** | `https://ev.gezat.et/` | EV Distributor Showcase | Ethiopia (Addis Ababa) | Distributor model offerings & physical showroom presence | Represents distributor stocking intent; single-distributor observation. |
| **SRC-CAT-01** | **CQSW Auto Parts** | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | Specialist Parts Supplier | China (Global Export) | BYD Seagull OEM part numbers and component schematics | Specialist export catalog; cross-referenced with Landin Parts. |
| **SRC-CAT-02** | **Landin BYD Parts** | `https://www.landinparts.com/byd/` | Specialist Parts Supplier | China (Global Export) | BYD Seagull OEM part numbers, pricing snapshots (CNY) | Single-supplier retail point observations. Excludes freight, insurance, and tariffs. |
| **SRC-CAT-03** | **Toyota Spare Parts** | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X` | OEM / Aftermarket Portal | Global (Europe / Global) | Toyota bZ4X OEM part numbers, diagrams, fitment trees | Structured global Toyota EPC; prices in USD/EUR. |
| **SRC-CAT-04** | **Exist.ae** | `https://exist.ae/catalog/cars/volkswagen/id-4` | Regional Auto Parts Hub | UAE (Dubai / Middle East) | VW ID.4 parts, pricing (AED), stock availability | Regional retail hub prices; represents Dubai-to-Djibouti regional supply corridor. |
| **SRC-REG-01** | **NHTSA Recalls API** | `https://api.nhtsa.gov/recalls/recallsByVehicle` | Regulatory Safety Agency | USA | Safety recalls, campaign numbers, defect consequences | **US-market regulatory data.** Applicable to global platforms (bZ4X, ID.4) as engineering baselines, but not Chinese domestic models (Seagull). |
| **SRC-REG-02** | **NHTSA Complaints API** | `https://api.nhtsa.gov/complaints/complaintsByVehicle` | Regulatory Safety Agency | USA | Consumer failure complaints, mileage at failure | Engineering wear indicators for chassis, braking, and HVAC systems. |

---

## 2. Field-Level Observation Registry (All 30 Vehicle-Part Combinations)

*All 30 empirical catalog observations collected on November 18, 2026, preserved in `data/raw/parts_catalog_evidence_raw.csv`:*

| Observation ID | Target Vehicle | Category Name | Exact Observed Part Name | Verified OEM Number | Observed Price & Currency | Converted USD | Availability | Source Platform & URL | Verified By Second Source? |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| `RAW-SGL-BRKPAD-01` | BYD Seagull | Brake pads | Front brake pad set | `EQEA-3501500CH` | $42.00 USD | $42.00 | In Stock | [CQSW](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts) | Yes (Landin) |
| `RAW-SGL-BRKDISC-01` | BYD Seagull | Brake discs | Front brake disc rotor | `EM2E-3501011` | $38.00 USD | $38.00 | In Stock | [CQSW](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts) | Yes (Landin) |
| `RAW-SGL-CABFILT-01` | BYD Seagull | Cabin-air filters | A/C air filter element | `EQEA-8100242` | $8.50 USD | $8.50 | In Stock | [Shindary / CQSW](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts) | Yes (Lazada) |
| `RAW-SGL-WIPER-01` | BYD Seagull | Wiper blades | Front wiper blade pad left | `EQEA-5205110` | $12.00 USD | $12.00 | In Stock | [CQSW](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts) | Yes (Landin) |
| `RAW-SGL-HEADLIGHT-01` | BYD Seagull | Headlights | Headlamp assembly left LED | `EQEA-4121010B` | 418.00 CNY | $57.68 | In Stock | [Landin](https://www.landinparts.com/byd/) | Yes (CQSW) |
| `RAW-SGL-TAILLIGHT-01` | BYD Seagull | Tail lights | Tail lamp assembly left | `EQEA-4133010` | 198.00 CNY | $27.32 | In Stock | [Landin](https://www.landinparts.com/byd/) | Yes (CQSW) |
| `RAW-SGL-MIRROR-01` | BYD Seagull | Side mirrors | Rearview side mirror left | `EQEA-8202100` | 429.00 CNY | $59.20 | In Stock | [Landin](https://www.landinparts.com/byd/) | Yes (CQSW) |
| `RAW-SGL-BUMPER-01` | BYD Seagull | Bumpers | Front bumper cover upper | `EQEA-2083111` | 198.00 CNY | $27.32 | In Stock | [Landin](https://www.landinparts.com/byd/) | Yes (CQSW) |
| `RAW-SGL-FENDER-01` | BYD Seagull | Fenders/body panels | Front fender panel left | `EQEA-8403010/70` | UNAVAILABLE | NULL | Order Only | [CQSW](https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts) | Yes (Landin) |
| `RAW-SGL-SHOCK-01` | BYD Seagull | Shock absorbers | Front shock absorber left | `EQEA-2905100A` | 138.00 CNY | $19.04 | In Stock | [Landin](https://www.landinparts.com/byd/) | Yes (CQSW) |
| `RAW-TOY-BRKPAD-01` | Toyota bZ4X | Brake pads | Disc brake pad kit front | `04465-78020` | $78.50 USD | $78.50 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Toyota Parts Deal) |
| `RAW-TOY-BRKDISC-01` | Toyota bZ4X | Brake discs | Front axle brake rotor | `43512-78020` | $115.00 USD | $115.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Autoparts-24) |
| `RAW-TOY-CABFILT-01` | Toyota bZ4X | Cabin-air filters | Clean air pollen filter | `87139-42050` | $24.00 USD | $24.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Longo Toyota) |
| `RAW-TOY-WIPER-01` | Toyota bZ4X | Wiper blades | Front wiper blade right | `85212-42220` | $22.50 USD | $22.50 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Brighton Toyota) |
| `RAW-TOY-HEADLIGHT-01` | Toyota bZ4X | Headlights | Headlamp assembly left LED | `81185-42B00` | $850.00 USD | $850.00 | Lead Time | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (OEM Parts Online) |
| `RAW-TOY-TAILLIGHT-01` | Toyota bZ4X | Tail lights | Tail lamp assembly left | `81560-42260` | $285.00 USD | $285.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Toyota Parts Deal) |
| `RAW-TOY-MIRROR-01` | Toyota bZ4X | Side mirrors | Outer mirror left power | `87940-42E10` | $320.00 USD | $320.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Toyota Parts Deal) |
| `RAW-TOY-BUMPER-01` | Toyota bZ4X | Bumpers | Front bumper cover fascia | `52119-4A956` | $340.00 USD | $340.00 | Lead Time | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (American Toyota) |
| `RAW-TOY-FENDER-01` | Toyota bZ4X | Fenders/body panels | Front fender panel left | `53812-42460` | $210.00 USD | $210.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (Toyota Parts Deal) |
| `RAW-TOY-SHOCK-01` | Toyota bZ4X | Shock absorbers | Front strut left | `48520-80742` | $185.00 USD | $185.00 | In Stock | [Toyota Spare Parts](https://www.toyota-spare-parts.com/toyota-cars/BZ4X) | Yes (OEM Parts Online) |
| `RAW-VW-BRKPAD-01` | VW ID.4 | Brake pads | Front brake pad set | `1EA-698-151-B` | 285.00 AED | $77.52 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (Super-Parts) |
| `RAW-VW-BRKDISC-01` | VW ID.4 | Brake discs | Front brake rotor 330x23 | `1EA-615-301-B` | 360.00 AED | $97.92 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (AHW Shop) |
| `RAW-VW-CABFILT-01` | VW ID.4 | Cabin-air filters | Active carbon pollen filter | `1EA-819-669` | 95.00 AED | $25.84 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (Spareto) |
| `RAW-VW-WIPER-01` | VW ID.4 | Wiper blades | Front aero wiper set | `1EA-955-425` | 85.00 AED | $23.12 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-HEADLIGHT-01` | VW ID.4 | Headlights | LED headlight assembly left | `1EA-941-035` | 2650.00 AED | $720.80 | Lead Time | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-TAILLIGHT-01` | VW ID.4 | Tail lights | Rear combination lamp left | `1EA-945-095` | 890.00 AED | $242.08 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-MIRROR-01` | VW ID.4 | Side mirrors | Rearview mirror left | `1EA-857-507` | 720.00 AED | $195.84 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-BUMPER-01` | VW ID.4 | Bumpers | Front bumper cover panel | `1EA-807-217` | 1150.00 AED | $312.80 | Lead Time | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-FENDER-01` | VW ID.4 | Fenders/body panels | Front wing fender panel left | `1EA-821-105` | 680.00 AED | $184.96 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (VAG Parts) |
| `RAW-VW-SHOCK-01` | VW ID.4 | Shock absorbers | Front suspension strut left | `1EA-413-031` | 580.00 AED | $157.76 | In Stock | [Exist.ae](https://exist.ae/catalog/cars/volkswagen/id-4) | Yes (BRYMAN Exist.ae) |

---

## 3. Regulatory Safety & Defect Signal Sources (NHTSA API)

| Signal Record ID | Target Vehicle | Endpoint URL | Query Parameters | Collection Date | Verified Recalls | Verified Complaints |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `SIG-TOY-BZ4X-01` | Toyota bZ4X | `https://api.nhtsa.gov/recalls/recallsByVehicle` | `make=toyota&model=bz4x&modelYear=2023` | 2026-11-18 | **4 recalls** (Hub bolts 22V444, HVAC defroster 25V577, Labels 24V548, Camera 25V744) | N/A |
| `SIG-TOY-BZ4X-02` | Toyota bZ4X | `https://api.nhtsa.gov/complaints/complaintsByVehicle` | `make=toyota&model=bz4x&modelYear=2023` | 2026-11-18 | N/A | **7 complaints** (Bumper/undercarriage 11733142, Suspension/tires 11690353, HVAC 11768022) |
| `SIG-VW-ID4-01` | VW ID.4 | `https://api.nhtsa.gov/recalls/recallsByVehicle` | `make=volkswagen&model=id.4&modelYear=2023` | 2026-11-18 | **14 recalls** (Door locks, 12V harness 22V956, Sunshade 23V750, HV battery 25V836/26V028) | N/A |
| `SIG-VW-ID4-02` | VW ID.4 | `https://api.nhtsa.gov/complaints/complaintsByVehicle` | `make=volkswagen&model=id.4&modelYear=2023` | 2026-11-18 | N/A | Front strut knocking, HVAC blower motor restriction |
| `SIG-BYD-SGL-01` | BYD Seagull | `https://api.nhtsa.gov/` | `make=byd&model=seagull` | 2026-11-18 | **0** (`GEOGRAPHIC_BOUNDARY_UNAVAILABLE`) | **0** (`GEOGRAPHIC_BOUNDARY_UNAVAILABLE`) |

---

*Registry verified and updated as of November 18, 2026.*
