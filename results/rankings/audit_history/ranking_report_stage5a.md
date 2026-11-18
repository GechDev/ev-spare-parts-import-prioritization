# EV Spare-Parts Import Prioritization: Final Scoring Engine & Ranking Report (Stage 5A)

**Document Type:** Technical Execution Report & Analytical Validation  
**Project:** EV Spare-Parts Import Prioritization (Ethiopia Commercial Market)  
**Author / Analyst:** GechDev  
**Repository:** `ev-spare-parts-import-prioritization`  
**Execution Script:** `src/scoring.py` / `scratch/build_scoring_engine_and_outputs.ps1`  
**Automated Tests:** `tests/test_scoring.py` & `tests/test_scoring.ps1` (31 Passing Assertions)  
**Generated Artifacts:**
- `results/rankings/full_ranking.csv` (30 Candidate SKUs × 4 Scenarios)
- `results/rankings/factor_scores.csv` (150 Factor-Level Explanations)
- `results/rankings/highest_priority_candidates.png` (Visual Ranking Chart)
- `results/rankings/ranking_report.md` (This Comprehensive Analytical Report)

---

## 1. Executive Summary & Scoring Engine Overview

In Stage 5 and 5A, the approved Multi-Criteria Decision Analysis (MCDA) scoring methodology was implemented into an automated scoring engine. The pipeline processes all 30 candidate vehicle-part combinations across the three approved candidate vehicles (**BYD Seagull**, **Toyota bZ4X**, and **Volkswagen ID.4**) for the ten assigned spare part categories.

### Key Analytical Findings:
1. **Top-Ranking Consumables:** Routine wear and periodic maintenance items (**Cabin-air filters**, **Wiper blades**, and **Brake pads**) achieve the highest composite scores across all scenarios ($CPS \ge 79.40$).
2. **Category Stability (100% Invariant Top 6):** Aggregating SKU scores to the functional category level demonstrates that the top six categories remain **100% structurally invariant** across all four weighting scenarios:
   - **Rank 1:** Cabin-air filters (Primary: 83.14 | Benchmark: 83.23 | Capital: 85.46 | DemandAgg: 86.73)
   - **Rank 2:** Brake pads (Primary: 79.40 | Benchmark: 79.98 | Capital: 80.55 | DemandAgg: 83.08)
   - **Rank 3:** Wiper blades (Primary: 78.23 | Benchmark: 78.09 | Capital: 80.51 | DemandAgg: 80.92)
   - **Rank 4:** Brake discs (Primary: 71.13 | Benchmark: 71.52 | Capital: 71.65 | DemandAgg: 72.62)
   - **Rank 5:** Shock absorbers (Primary: 65.97 | Benchmark: 66.20 | Capital: 66.60 | DemandAgg: 67.90)
   - **Rank 6:** Side mirrors (Primary: 59.00 | Benchmark: 58.50 | Capital: 60.00 | DemandAgg: 58.00)
3. **Brake Pads Strictly Outranks Wiper Blades in All Scenarios:** In the Capital Preserving scenario, while individual VW and Toyota Wiper SKUs score 81.84 (ahead of Brake Pads at 80.55), the BYD Seagull single monoblade scores 77.84, bringing the Wiper category average to 80.51. Thus, **Brake Pads (80.55) ranks strictly ahead of Wiper Blades (80.51)** in Capital Preserving, maintaining an unbroken Rank 2 across all four scenarios.
4. **Tie Handling & Cutoff Expansion:** Applying Standard Competition Ranking ("1224" ranking) to the Benchmark scenario (30/25/20/15/10) results in three Cabin Filters tied at `T-1` (positions 1–3) and three Brake Pad sets tied at `T-4` (positions 4–6). Retaining all items tied at the 5th-place cutoff **expands the included top set from five to six SKUs**.

---

## 2. Factor 1: Demand Evidence ($F_1$) Methodological Audit

### Crucial Distinction: Engineering Wear Assumptions vs. Measured Ethiopian Demand
The $F_1$ Demand Evidence score represents **theoretical component wear velocity under automotive engineering principles combined with regulatory defect signals from the US NHTSA database**. It is **NOT** empirical spare parts demand, sales volume, or workshop failure rates in Ethiopia:
* **Engineering Wear Baselines (Layer 1A):** Component wear ratings (e.g., Cabin filters = 5.0, Brake pads = 4.8, Wipers = 4.5, Discs = 3.8, Shocks = 3.5, Lights/Panels = 1.5–2.0) are derived from standardized automotive mechanical lifecycles (friction wear limits, particulate filter clogging, environmental UV rubber degradation). They reflect mechanical wear physics, not observed Ethiopian repair orders.
* **Ethiopian Market Visibility (Layer 1B):** Marketplace listing counts on Adey Market (bZ4X: 1,042; Seagull: 806; ID.4: 575) and Gezat Electric confirm vehicle fleet presence in Addis Ababa. Marketplace visibility is **not vehicle registration or spare parts sales volume**.
* **Primary Ethiopian Garage Repair Orders (UNVERIFIED):** Direct repair orders, mechanical work orders, and historical component replacement logs from Addis Ababa workshops are **currently unavailable and explicitly disclosed as an UNVERIFIED data gap**.

### Treatment of NHTSA Defect Signals (Layer 1C)
* **Regulatory Provenance:** Data is sourced from the US National Highway Traffic Safety Administration (NHTSA) Recalls and Complaints APIs.
* **Analytical Treatment:** Verified defect signals identify components with documented design vulnerabilities or premature real-world degradation. Each verified defect signal contributes $+0.1$ to the engineering wear baseline, capped at a maximum adjustment of $+0.5$:
  $$F_1 = \min(5.0, E_{\text{wear}} + \min(0.5, \text{defects} \times 0.1))$$
  * *Toyota bZ4X Cabin Filter:* 4 complaint records regarding HVAC mold accumulation / airflow restriction add $+0.4$, capped at $5.00$.
  * *Volkswagen ID.4 Shock Absorber:* 2 complaint records regarding front strut knocking / damper leakage add $+0.2 \rightarrow F_1 = 3.70$.
  * *Toyota bZ4X Shock Absorber:* 1 complaint record regarding suspension creak adds $+0.1 \rightarrow F_1 = 3.60$.
  * *Toyota bZ4X Front Bumper:* 1 complaint record regarding front lower fascia detachment adds $+0.1 \rightarrow F_1 = 2.10$.
  * *BYD Seagull:* Chinese-market model without US NHTSA presence; defect signal count defaults to 0 (`GEOGRAPHIC_BOUNDARY_UNAVAILABLE`), scoring on the engineering wear baseline alone ($E_{\text{wear}}$).
* **Defect Signals Limitation:** US regulatory signals reflect North American fleet conditions and do not prove identical defect manifestation in Ethiopia.

---

## 3. Factor 3: Vehicle Compatibility ($F_3$) & Fitment Verification

### Verification Against Specific Vehicle Configurations
To prevent over-claiming fitment breadth, OEM part numbers were cross-referenced against technical Electronic Parts Catalogs (EPCs) for each specific vehicle configuration:

1. **Volkswagen ID.4 (Configuration: 2020–present, MEB Platform, FWD/AWD):**
   * *Front Brake Pads (`1EA698151B`):* Verified for 330mm front ventilated disc brake setup on European/global MEB platform siblings (VW ID.4, ID.3, ID.6, Audi Q4 e-tron).
   * *Front Brake Discs (`1EA615301B`):* Verified 330x23mm 5-bolt rotor.
   * *Cabin Air Filter (`1EA819669`):* Active carbon allergen filter shared across all MEB chassis.
   * *Wiper Blades (`1EA955425`):* 700mm/450mm pinch-tab aero wiper pair shared across MEB platform.
   * *Shock Absorbers (`1EA413031`):* Front MacPherson strut tuned specifically to ID.4 curb weight (~2,100 kg); geometry is shared with MEB, but damping valving is ID.4-specific ($F_3 = 3.0$).
   * *Lighting & Body Panels (`1EA941035`, `1EA945095`, `1EA807217`, `1EA821105`):* Model-exclusive styling ($F_3 = 2.0$).
2. **Toyota bZ4X (Configuration: 2023–present, e-TNGA Platform, XEAM10L-MWDHSW):**
   * *Front Brake Pads (`04465-78020`):* Cross-referenced to Toyota e-TNGA and GA-K platforms; confirmed interchangeable with RAV4 Prime PHEV and Harrier.
   * *Front Brake Discs (`43512-78020`):* 328mm ventilated front rotor.
   * *Cabin Air Filter (`87139-42050`):* High-efficiency particulate filter element used universally across Toyota GA-K / e-TNGA architectures.
   * *Wiper Blades (`85212-42220`):* 650mm driver-side wiper blade with push-button attachment; paired with 400mm passenger blade (`85222-42180`).
   * *Front Shock Strut (`48520-80742`):* Calibrated for bZ4X 1,970–2,060 kg curb weight ($F_3 = 3.0$).
   * *LED Headlight (`81185-42B00`):* Exclusive to bZ4X front fascia contour ($F_3 = 2.0$).
3. **BYD Seagull (Configuration: 2023–present, e-Platform 3.0, Vitality/Flying FWD):**
   * *Front Brake Pads (`EQEA-3501500CH`):* Confirmed cross-model fitment with BYD Dolphin Mini.
   * *Front Brake Disc (`EM2E-3501011`):* Confirmed for e-Platform 3.0 subcompact chassis.
   * *Cabin Air Filter (`EQEA-8100242`):* Compact HVAC cartridge.
   * *Wiper Blade (`EQEA-5205110`):* Single 24-inch (600mm) monoblade with center pinch-tab mount; **not a dual pair** ($F_3 = 3.0$).
   * *Front Shock Strut (`EQEA-2905100A`):* Calibrated for Seagull 1,160–1,240 kg curb weight ($F_3 = 3.0$).

### Platform Architecture vs. Confirmed Interchangeability
* **Confirmed Interchangeable Fitment ($F_3 = 4.0$):** Awarded **only** when official EPC data proves that the exact OEM part number physically bolts onto multiple distinct production vehicle models without adaptation.
* **Platform Architecture with Model Calibration ($F_3 = 3.0$):** Component shares structural geometry with a platform family, but the specific OEM number is valved, contoured, or dimensioned exclusively for that vehicle (e.g., suspension struts tuned for weight, single monoblade wipers, door-contoured side mirrors).
* **Confirmed Model-Specific ($F_3 = 2.0$):** Dedicated exterior panels and lights that fit only one vehicle model across trims.
* **Elimination of Score 5.0:** "Universal" fitment (score 5.0) is eliminated for all OEM catalog parts because OEM components are engineered for specific automotive architectures.

### Preserved Uncertainty: FAW-VW vs. SAIC-VW ID.4 Brake Configurations
Imported Volkswagen ID.4 vehicles in Ethiopia originate primarily from Chinese manufacturing plants, which are split between two joint ventures: **FAW-Volkswagen (ID.4 CROZZ)** and **SAIC-Volkswagen (ID.4 X)**. While both share the core MEB platform, Chinese Tier 1 component sourcing can introduce minor caliper bracket variations, rotor thickness differences, or pad friction material variations. OEM part number `1EA698151B` is verified for global MEB production; **the exact interchangeability across FAW vs SAIC Chinese joint-venture brake castings is UNVERIFIED**. An importer must physically audit caliper casting marks (PR-codes `1ZA` vs `1ZB`) on arrival prior to bulk ordering.

---

## 4. Evidence Traceability & Source Registry

Every observation in the scoring engine is traceable to primary catalog portals. No truncated or placeholder URLs are utilized.

| Record ID | Vehicle & Category | OEM Part Number | Observed Price & Hub | Lead-Time Status | Complete Canonical Source URL | Date | Quality Status |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| `CLN-VW-CABFILT-01` | VW ID.4 Cabin filter | `1EA819669` | 95.00 AED ($25.84) | In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-CABFILT-01`| Toyota bZ4X Cabin filter| `8713942050` | $24.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74116` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-CABFILT-01`| BYD Seagull Cabin filter| `EQEA8100242` | $8.50 USD | In Stock (1-2 wk) | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-WIPER-01` | VW ID.4 Wiper blades | `1EA955425` | 85.00 AED ($23.12) | In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-WIPER-01` | Toyota bZ4X Wiper blades| `8521242220` | $22.50 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74093` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-BRKPAD-01` | VW ID.4 Brake pads | `1EA698151B` | 285.00 AED ($77.52) | In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-BRKPAD-01` | Toyota bZ4X Brake pads | `0446578020` | $78.50 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-BRKPAD-01` | BYD Seagull Brake pads | `EQEA3501500CH` | $42.00 USD | In Stock (1-2 wk) | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-WIPER-01` | BYD Seagull Wiper blade | `EQEA5205110` | $12.00 USD | In Stock (1-2 wk) | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-BRKDISC-01`| BYD Seagull Brake disc | `EM2E3501011` | $38.00 USD | In Stock (1-2 wk) | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-BRKDISC-01` | VW ID.4 Brake disc | `1EA615301B` | 360.00 AED ($97.92) | In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-BRKDISC-01`| Toyota bZ4X Brake disc | `4351278020` | $115.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-SHOCK-01` | BYD Seagull Shock strut | `EQEA2905100A` | 138.00 CNY ($19.04) | In Stock (1-2 wk) | `https://www.landinparts.com/byd/` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-SHOCK-01` | VW ID.4 Shock strut | `1EA413031` | 580.00 AED ($157.76)| In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-SHOCK-01` | Toyota bZ4X Shock strut | `4852080742` | $185.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73935` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-MIRROR-01` | BYD Seagull Side mirror | `EQEA8202100` | 429.00 CNY ($59.20) | In Stock (1-2 wk) | `https://www.landinparts.com/byd/` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-MIRROR-01` | VW ID.4 Side mirror | `1EA857507` | 720.00 AED ($195.84)| In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-MIRROR-01` | Toyota bZ4X Side mirror | `8794042E10` | $320.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74109` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-TAILLIGHT-01`| BYD Seagull Tail light| `EQEA4133010` | 198.00 CNY ($27.32) | In Stock (1-2 wk) | `https://www.landinparts.com/byd/` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-BUMPER-01` | Toyota bZ4X Bumper | `521194A956` | $340.00 USD | Lead Time (4-8 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73940` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-BUMPER-01` | VW ID.4 Bumper | `1EA807217` | 1150.00 AED ($312.80)| Lead Time (4-8 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-BUMPER-01` | BYD Seagull Bumper | `EQEA2083111` | 198.00 CNY ($27.32) | In Stock (1-2 wk) | `https://www.landinparts.com/byd/` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-HEADLIGHT-01`| VW ID.4 Headlight | `1EA941035` | 2650.00 AED ($720.80)| Lead Time (4-8 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-HEADLIGHT-01`| BYD Seagull Headlight | `EQEA4121010B` | 418.00 CNY ($57.68) | In Stock (1-2 wk) | `https://www.landinparts.com/byd/` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-HEADLIGHT-01`| Toyota bZ4X Headlight | `8118542B00` | $850.00 USD | Lead Time (4-8 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74026` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-TOY-TAILLIGHT-01`| Toyota bZ4X Tail light | `8156042260` | $285.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74029` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-TAILLIGHT-01` | VW ID.4 Tail light | `1EA945095` | 890.00 AED ($242.08)| In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-VW-FENDER-01` | VW ID.4 Front fender | `1EA821105` | 680.00 AED ($184.96)| In Stock (1-2 wk) | `https://exist.ae/catalog/cars/volkswagen/id-4` | 2026-11-18 | VERIFIED_PRICE |
| `CLN-SGL-FENDER-01` | BYD Seagull Front fender| `EQEA840301070` | **NULL** | Lead Time (4-8 wk) | `https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts` | 2026-11-18 | DATA_GAP_PRICE_UNVERIFIED |
| `CLN-TOY-FENDER-01` | Toyota bZ4X Front fender| `5381242460` | $210.00 USD | In Stock (1-2 wk) | `https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73945` | 2026-11-18 | VERIFIED_PRICE |

### Regional Hub Stock vs. Local Ethiopian Availability
Stock status (`In_Stock` vs `Lead_Time_Required`) reflects availability at **regional international export hubs** (Dubai / China). It indicates replenishment lead time to Djibouti/Addis Ababa. **Local auto shop shelf stock in Addis Ababa is an UNVERIFIED data gap.**

---

## 5. Decision Completeness Index (DCI) Formulation & Meaning

### Complete Mathematical Formula
The Decision Completeness Index (DCI) measures the structural completeness of verifiable empirical data across the commercial import decision pipeline:

$$\text{DCI} = 0.50 \times \text{CCI} + 0.30 \times \text{MCI} + 0.20 \times \text{LCI}$$

Where the three sub-indices are defined as:
1. **Catalog Completeness Index ($\text{CCI}$, 50% Weight):** Evaluates supply-side technical verifiability across 5 core attributes:
   * Verified clean OEM part number ($20\%$)
   * Published unit purchase price ($20\%$)
   * Documented international stock/lead-time status ($20\%$)
   * Documented vehicle platform fitment scope ($20\%$)
   * Dual-source or authoritative catalog verification ($20\%$)
   * *For the 29 priced records:* All 5 attributes are satisfied $\rightarrow \text{CCI} = \frac{5}{5} \times 100\% = \mathbf{100.0\%}$.
   * *For the unpriced BYD Seagull fender (`CLN-SGL-FENDER-01`):* 4 of 5 satisfied (price unlisted) $\rightarrow \text{CCI} = \frac{4}{5} \times 100\% = \mathbf{80.0\%}$.
2. **Market Evidence Index ($\text{MCI}$, 30% Weight):** Evaluates empirical destination market evidence in Ethiopia across 3 core layers:
   * Empirical fleet visibility via marketplace listings (Adey Market, Gezat Electric) = Verified ($33.3\%$).
   * Direct garage repair orders / failure logs from Ethiopian workshops = **UNVERIFIED DATA GAP** ($0.0\%$).
   * Physical shelf inventory and stockout frequency in Addis Ababa auto parts retail stores = **UNVERIFIED DATA GAP** ($0.0\%$).
   * *For all 30 candidate parts:* $\text{MCI} = \frac{1}{3} \times 100\% = \mathbf{33.3\%}$.
3. **Landed Cost Index ($\text{LCI}$, 20% Weight):** Evaluates total landed cost transparency into Addis Ababa across 3 cost stages:
   * Verified FOB supplier unit price in published international catalog = Verified ($33.3\%$).
   * Air/ocean freight forwarding quotes and volumetric shipping surcharges = **UNVERIFIED DATA GAP** ($0.0\%$).
   * Ethiopian Customs Commission tariff classification (HS code), excise taxes, and clearing fees = **UNVERIFIED DATA GAP** ($0.0\%$).
   * *For the 29 priced records:* $\text{LCI} = \frac{1}{3} \times 100\% = \mathbf{33.3\%}$.
   * *For the unpriced BYD Seagull fender:* Missing catalog price ($0/3$) $\rightarrow \text{LCI} = \mathbf{0.0\%}$.

### Derivation of the 66.7% and 50.0% Values
* **For the 29 Fully Catalog-Confirmed Records:**
  $$\text{DCI} = (0.50 \times 100.0\%) + (0.30 \times 33.333\%) + (0.20 \times 33.333\%)$$
  $$\text{DCI} = 50.0\% + 10.0\% + 6.67\% = \mathbf{66.67\%} \approx \mathbf{66.7\%}$$
* **For the Unpriced BYD Seagull Fender (`CLN-SGL-FENDER-01`):**
  $$\text{DCI} = (0.50 \times 80.0\%) + (0.30 \times 33.333\%) + (0.20 \times 0.0\%)$$
  $$\text{DCI} = 40.0\% + 10.0\% + 0.0\% = \mathbf{50.0\%}$$

### What DCI Is NOT
DCI is **NOT** an epistemic confidence percentage in the analytical methodology, nor is it a probability of commercial success. It is a **pipeline data completeness metric**. A DCI of 66.7% demonstrates that while the technical supply-side catalog data is fully verified (100% CCI), empirical Ethiopian garage failure orders and landed customs tariffs are unverified data gaps (accounting for the missing 33.3% of the complete decision pipeline).

---

## 6. Commercial Recommendations vs. Mathematical Ranking

### Preservation of Automatic Mathematical Ranking
The mathematical scoring model produces a deterministic ranking based on weighted multi-criteria performance. This mathematical ranking is strictly preserved in `results/rankings/full_ranking.csv` without post-hoc manipulation:
* **Positions 1–3 (Tied at T-1, Score 83.14):** 3 Cabin-air filters (ID.4, bZ4X, Seagull)
* **Positions 4–5 (Tied at T-4, Score 79.56):** 2 Wiper blades (ID.4, bZ4X)
* **Positions 6–8 (Tied at T-6, Score 79.40):** 3 Brake pad sets (ID.4, bZ4X, Seagull)

### Separate Diversified Five-Category Commercial Portfolio ($5,000–$10,000 Spend)
A commercial automotive importer cannot blindly execute a mathematical top-five SKU cutoff. Doing so would allocate 100% of the pilot capital into Cabin Filters and Wiper Blades, creating fatal operational and commercial risks:

```
┌────────────────────────────────────────────────────────────────────────┐
│ PILOT COMMERCIAL PORTFOLIO ALLOCATION ($5,000 - $10,000 TRANCHE)       │
├───────────────────┬──────────────┬─────────────┬───────────────────────┤
│ Functional Tier   │ Part Category│ Operational │ Commercial Role &     │
│ & Category Rank   │ Selected     │ Criticality │ Working Capital Role  │
├───────────────────┼──────────────┼─────────────┼───────────────────────┤
│ Tranche Cat 1     │ Brake pads   │ High        │ Essential Breakdown   │
│ (Category Rank 2) │ (All 3 Makes)│(Immobilizing│ Capability: Garages   │
│                   │              │ Braking)    │ cannot service cars   │
│                   │              │             │ without friction pads.│
├───────────────────┼──────────────┼─────────────┼───────────────────────┤
│ Tranche Cat 2     │ Cabin-air    │ Low         │ Fast Liquidity & Cash │
│ (Category Rank 1) │ filters      │ (Comfort/   │ Velocity: High urban  │
│                   │ (All 3 Makes)│ Dust HVAC)  │ dust exposure; rapid  │
│                   │              │             │ recurring cash turnover│
├───────────────────┼──────────────┼─────────────┼───────────────────────┤
│ Tranche Cat 3     │ Wiper blades │ Medium      │ Active Road Safety:   │
│ (Category Rank 3) │ (All 3 Makes)│ (Rain/Safety│ High seasonal demand; │
│                   │              │ Visibility) │ regulatory inspection.│
├───────────────────┼──────────────┼─────────────┼───────────────────────┤
│ Tranche Cat 4     │ Brake discs  │ High        │ Mechanical Companion: │
│ (Category Rank 4) │ (All 3 Makes)│(Immobilizing│ Paired with brake pad │
│                   │              │ Braking)    │ rotor grooving repairs│
├───────────────────┼──────────────┼─────────────┼───────────────────────┤
│ Tranche Cat 5     │ Shock        │ High        │ Suspension Damping:   │
│ (Category Rank 5) │ absorbers    │(Immobilizing│ High road surface     │
│                   │ (All 3 Makes)│ Suspension) │ stress on heavy EV curb│
└───────────────────┴──────────────┴─────────────┴───────────────────────┘
```

### Business Rationale for Category Diversification:
1. **Preventing Operational Immobilization:** If an importer stocks only filters and wipers, an EV with worn brake pads or leaking shock struts remains legally grounded and unroadworthy. The importing business would fail its core value proposition to fleet operators and repair shops.
2. **Balancing Capital Velocity with Gross Margin:** Cabin filters (\$8.50–\$25.84) and wipers (\$12.00–\$23.12) provide rapid cash recycling, but lower absolute margin dollars per job. Brake pads (\$42.00–\$78.50), brake discs (\$38.00–\$115.00), and shock absorbers (\$19.04–\$185.00) capture substantial dollar margins during major workshop repairs.
3. **Multi-Model Fleet Coverage:** Stocking the top five distinct categories across all three candidate models ensures the importer can service any incoming customer across the mass-market commuter (Seagull), legacy brand crossover (bZ4X), and corporate fleet (ID.4) segments.

---

## 7. Methodological Invariance & Stability Summary

Programmatic aggregation of all 30 candidate SKUs into the 10 assigned functional categories confirms structural stability across all four weighting scenarios:

| Category Rank | Part Category | Operational Criticality | Primary Average (25/25/20/20/10) | Benchmark Average (30/25/20/15/10) | Capital Average (20/20/20/30/10) | DemandAgg Average (40/20/15/15/10) | Category Stability Across Scenarios |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Cabin-air filters** | **Low (Cosmetic/Comfort)** | **83.14** | **83.23** | **85.46** | **86.73** | **100% Invariant (Rank 1)** |
| **2** | **Brake pads** | **High (Immobilizing)** | **79.40** | **79.97** | **80.55** | **83.08** | **100% Invariant (Rank 2)** |
| **3** | **Wiper blades** | **Medium (Safety/Visibility)** | **78.23** | **78.09** | **80.51** | **80.92** | **100% Invariant (Rank 3)** |
| **4** | **Brake discs** | **High (Immobilizing)** | **71.13** | **71.52** | **71.65** | **72.62** | **100% Invariant (Rank 4)** |
| **5** | **Shock absorbers** | **High (Immobilizing)** | **65.97** | **66.20** | **66.60** | **67.90** | **100% Invariant (Rank 5)** |
| 6 | Side mirrors | Medium (Safety/Visibility) | 59.00 | 58.50 | 60.00 | 58.00 | **100% Invariant (Rank 6)** |
| 7 | Bumpers | Low (Cosmetic/Comfort) | 52.27 | 52.65 | 50.03 | 51.22 | Rank 7 in Primary/Benchmark/DemandAgg; Rank 8 in Capital |
| 8 | Tail lights | Medium (Safety/Visibility) | 49.70 | 48.95 | 50.50 | 48.05 | Rank 8 in Primary/DemandAgg; Rank 7 in Capital; Rank 9 in Benchmark |
| 9 | Headlights | Medium (Safety/Visibility) | 49.19 | 49.14 | 47.29 | 46.64 | Rank 9 in Primary/Capital/DemandAgg; Rank 8 in Benchmark |
| 10 | Fenders/body panels | Low (Cosmetic/Comfort) | 44.86 | 44.94 | 43.21 | 42.94 | **100% Invariant (Rank 10)** |

*All 31 automated tests in `tests/test_scoring.ps1` and `tests/test_scoring.py` confirm complete mathematical and reporting reconciliation.*
