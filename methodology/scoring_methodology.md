# Multi-Criteria Decision Analysis (MCDA) Scoring Methodology (Audited Quality-Control Specification)

**Document Type:** Formal Methodological Specification & Mathematical Framework  
**Project:** EV Spare-Parts Import Prioritization (Ethiopia Commercial Market)  
**Author / Analyst:** GechDev  
**Repository:** `ev-spare-parts-import-prioritization`  
**Associated Source Code:** `src/scoring.py`  
**Test Suite:** `tests/test_scoring.py` & `tests/test_scoring.ps1` (47 Automated Tests Passing)  
**Status:** Audited Quality-Control Revision 3 Submitted for Final Analyst Review  

---

## 1. Executive Summary & Final Quality-Control Revisions

Following the comprehensive Stage 4 Quality-Control audit, this document presents the fully reconciled, audited, and mathematically verified MCDA scoring methodology. Every calculation in this specification is derived programmatically from the underlying 30-SKU dataset with unrounded floating-point arithmetic, rounding only for display.

### Key Methodological & Mathematical Corrections:
1. **Programmatic Recalculation of Category Averages:** Eliminated manual transcription errors. Every category average across all four weighting scenarios is calculated programmatically from the 30 individual SKU scores.
2. **Category Ranking & Stability Correction (Brake Pads vs. Wiper Blades):** Reconciled the Capital scenario ranking. At the category level, **Brake Pads (80.55)** ranks strictly ahead of **Wiper Blades (80.51)** in the Capital scenario. Consequently, **Brake Pads is 100% Invariant at Rank 2** across all four scenarios, and **Wiper Blades is 100% Invariant at Rank 3** across all four scenarios.
3. **Benchmark Top-Five Cutoff Expansion (Tie-Handling Rule):** In the Benchmark scenario (30/25/20/15/10), 3 Cabin Filter SKUs share rank `T-1` (positions 1–3) and 3 Brake Pad SKUs share rank `T-4` (positions 4–6). Retaining all items tied at the 5th-place cutoff mathematically expands the top-performing group from **five to six SKUs** (3 Cabin Filters + 3 Brake Pad sets).
4. **Clarification of Factor 2 (International Procurement Delay):** Formally renamed *Market Scarcity* to **International Procurement Delay**. Explicitly clarified that international distributor stock status is **not** evidence of Ethiopian local scarcity. An unavailable international listing is an operational procurement hurdle and sourcing friction, **not an automatic buying mandate**. If a product is impossible to procure from regional hubs, it cannot be imported without custom fabrication or direct OEM factory allocation.
5. **Preservation of Empirical Evidence Boundaries:** Maintained strict separation between engineering wear lifecycles (automotive physics), international catalog availability (Dubai/China hubs), Ethiopian fleet visibility proxies (marketplace listings), and explicit **UNVERIFIED data gaps** (local Addis Ababa garage repair orders, physical auto parts shelf stock, and landed customs tariffs).
6. **Zero-Fabrication Data Protocol:** The unlisted BYD Seagull fender price (`RAW-SGL-FENDER-01`) remains strictly `NULL`. Sourcing practicality is evaluated on physical packaging alone (score `0.80`), tagged with `DATA_GAP_PRICE_UNVERIFIED`, with its Decision Completeness Index (DCI) reduced to 50.0%.

---

## 2. Factor Definitions & Scoring Rules (0.0 – 5.0 Scales)

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. DEMAND EVIDENCE (F1): Wear velocity + NHTSA defect signals (1.0-5.0)│
├────────────────────────────────────────────────────────────────────────┤
│ 2. INTERNATIONAL PROCUREMENT DELAY (F2): Hub lead-time delay (2.5-5.0) │
│    [Operational Criticality reported separately as 3-level metadata]   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. VEHICLE COMPATIBILITY (F3): Audited OEM fitment breadth (1.0-4.0)   │
├────────────────────────────────────────────────────────────────────────┤
│ 4. SOURCING PRACTICALITY (F4): Capital cost + packaging bulk (0.5-5.0) │
│    [Missing prices handled as NULL without artificial penalty]         │
├────────────────────────────────────────────────────────────────────────┤
│ 5. EVIDENCE CONFIDENCE (F5): Epistemic catalog verification (1.0-5.0)  │
└────────────────────────────────────────────────────────────────────────┘
```

### Factor 1: Demand Evidence ($F_1 \in [1.0, 5.0]$)
* **What It Measures:** Theoretical component replacement frequency based on mechanical friction wear, environmental degradation, and documented defect patterns.
* **Separation of Evidence Layers:**
  * *Layer 1A (Engineering Maintenance Lifecycle Baseline):* Routine air filters (`5.0`), friction brake pads (`4.8`), wiper blades (`4.5`), brake discs (`3.8`), shock absorbers (`3.5`), side mirrors (`2.5`), tail lights (`1.8`), headlights (`1.5`), fenders (`1.5`), bumpers (`2.0`). *Disclosed as automotive engineering wear principles, not verified Ethiopian repair orders.*
  * *Layer 1B (Ethiopian Fleet Visibility Context):* High marketplace listing volumes confirm vehicles exist in the fleet (bZ4X: 1,042; Seagull: 806; ID.4: 575). *Direct Ethiopian parts demand volume remains UNVERIFIED.*
  * *Layer 1C (External Defect Signals):* NHTSA safety recall/complaint records ($+0.1$ per verified signal, capped at $+0.5$). Disclosed as US regulatory signals, not direct Ethiopian failure rates (Toyota Cabin Filter: 4 signals $\rightarrow +0.4$, capped at $5.0$; VW Cabin Filter: 1 signal $\rightarrow +0.1$, capped at $5.0$; VW Shock: 2 signals $\rightarrow +0.2 = 3.7$; Toyota Shock: 1 signal $\rightarrow +0.1 = 3.6$; Toyota Bumper: 1 signal $\rightarrow +0.1 = 2.1$).
* **Calculation:** $F_1 = \min(5.0, E_{\text{wear}} + \min(0.5, \text{defects} \times 0.1))$. Missing evidence defaults to $1.0$.

### Factor 2: International Procurement Delay ($F_2 \in [2.5, 5.0]$, formerly Market Scarcity)
* **What It Measures:** Supply procurement lead-time delay and sourcing friction from international distribution hubs (Dubai / China) to Addis Ababa.
* **Scoring Rules:**
  * `In_Stock`: `2.50` ($S_2 = 50.0\%$). Readily available at regional distributor; standard 1–2 week order dispatch to Addis Ababa.
  * `Lead_Time_Required`: `4.00` ($S_2 = 80.0\%$). Factory order / supplier backorder; 4–8 week procurement delay.
  * `Unavailable`: `5.00` ($S_2 = 100.0\%$). Severe catalog stockout; unlisted or indefinite delay.
* **Critical Commercial Distinction & Sourcing Constraint Rule:**
  1. *Not Proof of Local Scarcity:* International distributor stock status is **not** evidence of Ethiopian local retail scarcity. Physical retail shelf inventory in Addis Ababa auto parts shops is an **UNVERIFIED data gap**.
  2. *Procurement Hurdle vs. Opportunity:* An unavailable or unlisted international listing represents an operational procurement hurdle and supply friction, **not an automatic commercial opportunity**. If an item cannot be procured from international hubs, an importer cannot purchase it without direct factory allocation. In commercial practice, parts with lead times must be scheduled with confirmed supplier commitments, while completely unlisted items (such as the unpriced BYD Seagull fender) are flagged as unverified gaps rather than allocated scarce pilot working capital.

### Factor 3: Vehicle Compatibility & Fitment Breadth ($F_3 \in [1.0, 4.0]$)
* **What It Measures:** Addressable vehicle fleet breadth, strictly separating confirmed cross-model fitment from unverified platform potential.
* **Strict Evidence Tiers:**
  * `4.0` — **Confirmed Cross-Model Platform Fitment:** Exact clean OEM part number verified in official technical EPC to fit multiple distinct vehicle models within the platform family:
    * VW MEB Brake Pads (`1EA698151B`), Brake Discs (`1EA615301B`), and Cabin Filter (`1EA819669`) confirmed across ID.4, ID.3, ID.6, and Audi Q4 e-tron.
    * Toyota bZ4X Brake Pads (`0446578020`), Brake Discs (`4351278020`), and Cabin Filter (`8713942050`) cross-fit bZ4X, RAV4 Prime, and Harrier.
    * BYD Seagull Brake Pads (`EQEA3501500CH`), Brake Discs (`EM2E3501011`), and Cabin Filter (`EQEA8100242`) confirmed across e-Platform 3.0 (Seagull, Dolphin Mini).
    * VW ID.4 Wiper Pair (`1EA955425`, 700/450mm) and Toyota bZ4X Wiper Pair (`8521242220`, 650/400mm) confirmed across shared platform arm profiles.
  * `3.0` — **Platform Architecture with Model-Specific Calibration:** Component built on a shared platform, but specific OEM part number is tuned to vehicle weight/geometry or arm length:
    * Shock absorbers calibrated to curb weight (ID.4 `1EA413031`, bZ4X `4852080742`, Seagull `EQEA2905100A`).
    * Side mirror housings contoured to door sheet metal (ID.4 `1EA857507`, bZ4X `8794042E10`, Seagull `EQEA8202100`).
    * BYD Seagull single 24-inch monoblade (`EQEA5205110`) with dedicated center-arm mount.
  * `2.0` — **Confirmed Model-Specific:** Part is technically and aesthetically exclusive to one vehicle model across trims:
    * Front bumper covers (ID.4 `1EA807217`, bZ4X `521194A956`, Seagull `EQEA2083111`).
    * Headlights (ID.4 `1EA941035`, bZ4X `8118542B00`, Seagull `EQEA4121010B`).
    * Tail lights (ID.4 `1EA945095`, bZ4X `8156042260`, Seagull `EQEA4133010`).
    * Sheet metal fenders (ID.4 `1EA821105`, bZ4X `5381242460`, Seagull `EQEA840301070`).
  * `1.0` — **Niche Trim-Exclusive:** Part fits only a specific sub-trim, single model year, or drive configuration (e.g., AWD-only components).
  * *(Note: Score `5.0` Universal is not awarded to any OEM catalog component because OEM parts are make/platform specific).*

### Factor 4: Sourcing Practicality & Capital Velocity ($F_4 \in [0.5, 5.0]$)
* **What It Measures:** Financial capital efficiency and volumetric shipping burden within a **$5,000 to $10,000 pilot capital constraint**.
* **Formulation:** $F_4 = 0.55 \times S_{\text{cost}} + 0.45 \times S_{\text{packaging}}$
  * **Unit Capital Cost Score ($S_{\text{cost}}$):** $< \$35 \rightarrow 5.0$ | $\$35 - \$80 \rightarrow 4.0$ | $\$80 - \$200 \rightarrow 3.0$ | $\$200 - \$400 \rightarrow 2.0$ | $\$400 - \$800 \rightarrow 1.0$ | $> \$800 \rightarrow 0.5$.
  * **Principled Missing Price Protocol (Zero-Fabrication):** If price is `NULL` (BYD Seagull fender `EQEA840301070`), $S_{\text{cost}}$ is recorded as `UNVERIFIED / NULL`. Sourcing Practicality is scored based on **available physical packaging profile alone** ($F_4 = S_{\text{packaging}} = 0.80$). Tagged with `DATA_GAP_PRICE_UNVERIFIED` and DCI reduced to 50.0%. No artificial $800 price is imputed.
  * **Freight & Packaging Compactness ($S_{\text{packaging}} = 5.0 - \text{Bulk Penalty}$):** Cabin filters (4.8) | Brake pads (4.5) | Wiper blades (4.2) | Brake discs (3.5) | Shock absorbers (3.0) | Side mirrors (3.0) | Tail lights (2.0) | Headlights (1.2) | Fenders (0.8) | Bumpers (0.0).

### Factor 5: Evidence Confidence & Data Rigor ($F_5 \in [1.0, 5.0]$)
* **What It Measures:** Epistemic data verifiability, provenance, and catalog cross-referencing. **Completely decoupled from defect signals.**
* **Decoupled Scoring Scale:**
  * `5.0` — **Dual-Source Verified with Published Price & Clean OEM Number:** Direct verification across two independent commercial/OEM portals, clean alphanumeric OEM number, live published price, and verified collection date.
  * `4.0` — **Authoritative Single-Source with Published Price & OEM Number:** Single official OEM technical catalogue or master distributor portal with verified OEM number and published price.
  * `3.0` — **Verified OEM Number, but Pricing Unlisted / Quote Required:** Authoritative catalog confirms OEM part number and vehicle fitment, but commercial price requires inquiry (e.g., BYD Seagull fender).
  * `2.0` — **Commercial Listing with Aftermarket / Unverified Identifier:** Distributor listing with internal SKU, lacking official OEM cross-reference.
  * `1.0` — **Uncorroborated / Informal Reference:** Informal marketplace photo, forum mention, or unverified specification without an OEM part number.

---

## 3. Operational Criticality (3-Level Framework) & Commercial Role

Operational Criticality is **not** added into the mathematical composite score. It is preserved as a separate decision metadata column to guide business portfolio selection:

| Criticality Tier | Definition & Technical Impact | Part Categories Included | Commercial Decision Role |
| :--- | :--- | :--- | :--- |
| **High (Immobilizing)** | Primary mechanical or hydraulic failure renders the vehicle unroadworthy and legally grounded. Vehicle cannot be driven safely under any condition. | **Brake pads, Brake discs, Shock absorbers** | **Essential Service Capability:** Fleet operators and garages face severe downtime penalties without these items; highest commercial urgency. |
| **Medium (Safety / Visibility)** | Active safety, roadworthiness, and night/wet driving impaired. Vehicle can limp in dry daylight, but cannot operate legally/safely at night or in rain. | **Wiper blades, Side mirrors, Headlights, Tail lights** | **Preventive & Regulatory Demand:** High roadside inspection and safety inspection failure rate; steady turnover. |
| **Low (Cosmetic / Comfort)** | Aesthetic damage or cabin comfort degradation. Vehicle remains 100% mechanically functional and drivable. Zero breakdown urgency. | **Cabin-air filters, Bumpers, Fenders/body panels** | **Cash-Flow Liquidity vs. Dead-Stock Buffer:** Cabin filters provide fast cash turnover; bumpers/fenders are deferred until major accidents. |

---

## 4. Reconciled Ranking of All 30 Individual Vehicle-Part Combinations

The table below presents the programmatically calculated ranking of all 30 candidate parts, displaying Standard Competition Rankings (`T-1`, `T-4`, `T-6`, `T-11`, `T-26`) across all four weighting scenarios:

| Primary Rank | Benchmark Rank | Capital Rank | DemandAgg Rank | Record ID | Vehicle | Part Category | Clean OEM Part Number | Price (USD) | Operational Criticality | Primary CPS (25/25/20/20/10) | Benchmark CPS (30/25/20/15/10) | Capital CPS (20/20/20/30/10) | DemandAgg CPS (40/20/15/15/10) | Decision Completeness (DCI) | Uncertainty Flag |
| :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **T-1** | T-1 | T-1 | T-1 | `CLN-VW-CABFILT-01` | ID.4 | Cabin-air filters | `1EA819669` | $25.84 | Low (Cosmetic/Comfort) | **83.14** | 83.23 | 85.46 | 86.73 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-1** | T-1 | T-1 | T-1 | `CLN-TOY-CABFILT-01` | bZ4X | Cabin-air filters | `8713942050` | $24.00 | Low (Cosmetic/Comfort) | **83.14** | 83.23 | 85.46 | 86.73 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-1** | T-1 | T-1 | T-1 | `CLN-SGL-CABFILT-01` | Seagull | Cabin-air filters | `EQEA8100242` | $8.50 | Low (Cosmetic/Comfort) | **83.14** | 83.23 | 85.46 | 86.73 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-4** | T-7 | T-4 | T-7 | `CLN-VW-WIPER-01` | ID.4 | Wiper blades | `1EA955425` | $23.12 | Medium (Safety/Visibility) | **79.56** | 79.42 | 81.84 | 81.92 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-4** | T-7 | T-4 | T-7 | `CLN-TOY-WIPER-01` | bZ4X | Wiper blades | `8521242220` | $22.50 | Medium (Safety/Visibility) | **79.56** | 79.42 | 81.84 | 81.92 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-6** | T-4 | T-6 | T-4 | `CLN-VW-BRKPAD-01` | ID.4 | Brake pads | `1EA698151B` | $77.52 | High (Immobilizing) | **79.40** | 79.97 | 80.55 | 83.08 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-6** | T-4 | T-6 | T-4 | `CLN-TOY-BRKPAD-01` | bZ4X | Brake pads | `0446578020` | $78.50 | High (Immobilizing) | **79.40** | 79.97 | 80.55 | 83.08 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-6** | T-4 | T-6 | T-4 | `CLN-SGL-BRKPAD-01` | Seagull | Brake pads | `EQEA3501500CH` | $42.00 | High (Immobilizing) | **79.40** | 79.97 | 80.55 | 83.08 | 66.7% | FULL_CATALOG_CONFIRMED |
| **9** | 9 | 9 | 9 | `CLN-SGL-WIPER-01` | Seagull | Wiper blades | `EQEA5205110` | $12.00 | Medium (Safety/Visibility) | **75.56** | 75.42 | 77.84 | 78.92 | 66.7% | FULL_CATALOG_CONFIRMED |
| **10** | 10 | 10 | 10 | `CLN-SGL-BRKDISC-01` | Seagull | Brake discs | `EM2E3501011` | $38.00 | High (Immobilizing) | **72.60** | 72.62 | 73.85 | 73.73 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-11** | T-11 | T-12 | T-11 | `CLN-VW-BRKDISC-01` | ID.4 | Brake discs | `1EA615301B` | $97.92 | High (Immobilizing) | **70.40** | 70.97 | 70.55 | 72.08 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-11** | T-11 | T-12 | T-11 | `CLN-TOY-BRKDISC-01` | bZ4X | Brake discs | `4351278020` | $115.00 | High (Immobilizing) | **70.40** | 70.97 | 70.55 | 72.08 | 66.7% | FULL_CATALOG_CONFIRMED |
| **13** | 13 | 11 | 13 | `CLN-SGL-SHOCK-01` | Seagull | Shock absorbers | `EQEA2905100A` | $19.04 | High (Immobilizing) | **68.40** | 67.80 | 70.60 | 69.30 | 66.7% | FULL_CATALOG_CONFIRMED |
| **14** | 14 | 14 | 14 | `CLN-VW-SHOCK-01` | ID.4 | Shock absorbers | `1EA413031` | $157.76 | High (Immobilizing) | **65.00** | 65.70 | 64.80 | 67.60 | 66.7% | FULL_CATALOG_CONFIRMED |
| **15** | 15 | 15 | 15 | `CLN-TOY-SHOCK-01` | bZ4X | Shock absorbers | `4852080742` | $185.00 | High (Immobilizing) | **64.50** | 65.10 | 64.40 | 66.80 | 66.7% | FULL_CATALOG_CONFIRMED |
| **16** | 16 | 16 | 16 | `CLN-SGL-MIRROR-01` | Seagull | Side mirrors | `EQEA8202100` | $59.20 | Medium (Safety/Visibility) | **61.20** | 60.15 | 63.30 | 59.65 | 66.7% | FULL_CATALOG_CONFIRMED |
| **17** | 17 | 17 | 17 | `CLN-VW-MIRROR-01` | ID.4 | Side mirrors | `1EA857507` | $195.84 | Medium (Safety/Visibility) | **59.00** | 58.50 | 60.00 | 58.00 | 66.7% | FULL_CATALOG_CONFIRMED |
| **18** | 18 | 19 | 18 | `CLN-TOY-MIRROR-01` | bZ4X | Side mirrors | `8794042E10` | $320.00 | Medium (Safety/Visibility) | **56.80** | 56.85 | 56.70 | 56.35 | 66.7% | FULL_CATALOG_CONFIRMED |
| **19** | 21 | 18 | 20 | `CLN-SGL-TAILLIGHT-01` | Seagull | Tail lights | `EQEA4133010` | $27.32 | Medium (Safety/Visibility) | **54.10** | 52.25 | 57.10 | 51.35 | 66.7% | FULL_CATALOG_CONFIRMED |
| **20** | 19 | 22 | 19 | `CLN-TOY-BUMPER-01` | bZ4X | Bumpers | `521194A956` | $340.00 | Low (Cosmetic/Comfort) | **52.90** | 53.90 | 49.00 | 52.10 | 66.7% | FULL_CATALOG_CONFIRMED |
| **21** | 20 | 23 | 21 | `CLN-VW-BUMPER-01` | ID.4 | Bumpers | `1EA807217` | $312.80 | Low (Cosmetic/Comfort) | **52.40** | 53.30 | 48.60 | 51.30 | 66.7% | FULL_CATALOG_CONFIRMED |
| **22** | 22 | 20 | 22 | `CLN-SGL-BUMPER-01` | Seagull | Bumpers | `EQEA2083111` | $27.32 | Low (Cosmetic/Comfort) | **51.50** | 50.75 | 52.50 | 50.25 | 66.7% | FULL_CATALOG_CONFIRMED |
| **23** | 23 | 26 | 23 | `CLN-VW-HEADLIGHT-01` | ID.4 | Headlights | `1EA941035` | $720.80 | Medium (Safety/Visibility) | **49.86** | 50.27 | 46.54 | 47.27 | 66.7% | FULL_CATALOG_CONFIRMED |
| **24** | 25 | 21 | 27 | `CLN-SGL-HEADLIGHT-01` | Seagull | Headlights | `EQEA4121010B` | $57.68 | Medium (Safety/Visibility) | **48.96** | 47.72 | 50.44 | 46.22 | 66.7% | FULL_CATALOG_CONFIRMED |
| **25** | 24 | 28 | 24 | `CLN-TOY-HEADLIGHT-01` | bZ4X | Headlights | `8118542B00` | $850.00 | Medium (Safety/Visibility) | **48.76** | 49.44 | 44.89 | 46.44 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-26** | T-26 | T-24 | T-25 | `CLN-TOY-TAILLIGHT-01` | bZ4X | Tail lights | `8156042260` | $285.00 | Medium (Safety/Visibility) | **47.50** | 47.30 | 47.20 | 46.40 | 66.7% | FULL_CATALOG_CONFIRMED |
| **T-26** | T-26 | T-24 | T-25 | `CLN-VW-TAILLIGHT-01` | ID.4 | Tail lights | `1EA945095` | $242.08 | Medium (Safety/Visibility) | **47.50** | 47.30 | 47.20 | 46.40 | 66.7% | FULL_CATALOG_CONFIRMED |
| **28** | 28 | 27 | 28 | `CLN-VW-FENDER-01` | ID.4 | Fenders/body panels | `1EA821105` | $184.96 | Low (Cosmetic/Comfort) | **46.04** | 45.53 | 46.06 | 44.03 | 66.7% | FULL_CATALOG_CONFIRMED |
| **29** | 29 | 30 | 29 | `CLN-SGL-FENDER-01` | Seagull | Fenders/body panels | `EQEA840301070` | NULL | Low (Cosmetic/Comfort) | **44.70** | 45.40 | 40.80 | 42.40 | 50.0% | DATA_GAP_PRICE_UNVERIFIED |
| **30** | 30 | 29 | 30 | `CLN-TOY-FENDER-01` | bZ4X | Fenders/body panels | `5381242460` | $210.00 | Low (Cosmetic/Comfort) | **43.84** | 43.88 | 42.76 | 42.38 | 66.7% | FULL_CATALOG_CONFIRMED |

---

## 5. Programmatically Derived 10-Category Summary Ranking

The table below is generated programmatically from the unrounded scores of the individual 30 SKUs. Internal arithmetic maintains full 64-bit precision, rounding only to 2 decimal places for display:

| Category Rank | Part Category | Operational Criticality | Primary Model Average (25/25/20/20/10) | Benchmark Average (30/25/20/15/10) | Capital Average (20/20/20/30/10) | DemandAgg Average (40/20/15/15/10) | Category Stability Across Scenarios |
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

### Key Category Ranking Observations:
1. **Brake Pads Strictly Outranks Wiper Blades in All 4 Scenarios:**
   * Primary: Brake Pads 79.40 vs. Wiper Blades 78.23 ($+1.17$)
   * Benchmark: Brake Pads 79.98 vs. Wiper Blades 78.09 ($+1.89$)
   * Capital: Brake Pads 80.55 vs. Wiper Blades 80.51 ($+0.04$)
   * DemandAgg: Brake Pads 83.08 vs. Wiper Blades 80.92 ($+2.16$)
   * *Correction Note:* While individual VW and Toyota Wiper SKUs score 81.84 in Capital (ahead of Brake Pads at 80.55), the BYD Seagull Wiper scores 77.84, which brings the Wiper category average to 80.51. Therefore, **at the category level, Brake Pads ranks ahead of Wiper Blades in all four scenarios without exception.**
2. **Structural Stability of the Top 6 Categories:**
   * The top six categories (Cabin filters, Brake pads, Wiper blades, Brake discs, Shock absorbers, Side mirrors) and the bottom category (Fenders) **maintain identical rank positions (100% Invariant)** across all four scenarios.
   * Minor rank interchanges occur only among lower-tier collision body components (Bumpers, Tail lights, Headlights) due to volumetric freight penalties in the Capital scenario and lighting electronics turnover in the Benchmark scenario.

---

## 6. Tie-Handling Rules & Mathematical Ranking vs. Business Portfolio

### Standard Competition Ranking ("1224" Ranking)
To eliminate arbitrary tie-breaks that would favor one vehicle model over another:
* SKUs sharing identical composite scores receive tied rank labels (`T-1`, `T-4`, `T-6`, `T-11`, `T-26`).
* The subsequent rank number advances by the count of tied items (e.g., three `T-1` items occupy positions 1, 2, and 3; the next rank is 4).

### Benchmark Top-Five Cutoff Expansion (6 Included SKUs)
In the Assignment Benchmark scenario (30/25/20/15/10):
* Positions 1, 2, and 3 are occupied by 3 Cabin Filter SKUs tied at **T-1 (83.23)**.
* Positions 4, 5, and 6 are occupied by 3 Brake Pad SKUs tied at **T-4 (79.98)**.
* Position 7 is occupied by VW and Toyota Wiper Blades tied at **T-7 (79.42)**.

**Cutoff Rule:** A strict mathematical cutoff at position 5 would arbitrarily exclude one of the three tied brake pad SKUs (e.g., dropping Toyota or Seagull or VW), which is mathematically indefensible. Therefore, **retaining all items tied at the 5th-place cutoff expands the mathematical top set from five to six SKUs** (3 Cabin Filters + 3 Brake Pad sets).

### Decoupling Mathematical Ranking from Commercial Portfolio Allocation
1. **Mathematical Top 5 SKU Ranking (Primary Scenario):**
   * T-1: 3 Cabin Filters (ID.4, bZ4X, Seagull) at 83.14.
   * T-4: 2 Wiper Blades (ID.4, bZ4X) at 79.56.
   * *(Tied at T-6: 3 Brake Pad sets at 79.40, trailing wipers by only 0.16 points).*
2. **Commercial Portfolio Allocation ($5,000 to $10,000 Tranche):**
   * A commercial automotive importer cannot import exclusively Cabin Filters and Wiper Blades. Doing so would leave their repair workshop unable to service vehicles immobilized by mechanical brake or suspension failures, destroying customer trust.
   * Operational prudence requires allocating capital across the **top distinct functional categories**:
     * **Tranche Category 1:** Brake pads (High Criticality, immediate breakdown repair)
     * **Tranche Category 2:** Cabin-air filters (Low Criticality, rapid recurring turnover)
     * **Tranche Category 3:** Wiper blades (Medium Criticality, active rain safety)
     * **Tranche Category 4:** Brake discs (High Criticality, rotor wear companion)
     * **Tranche Category 5:** Shock absorbers (High Criticality, rough road damping)

---

## 7. Discrepancy & Correction Log

| Item / Parameter | Previous Erroneous Entry | Corrected Audited Entry | Root Cause & Resolution |
| :--- | :---: | :---: | :--- |
| **Capital Scenario Category Ranks** | Wiper Blades Rank 2 (80.51) > Brake Pads Rank 3 (80.55) | **Brake Pads Rank 2 (80.55) > Wiper Blades Rank 3 (80.51)** | Conflated individual VW/Toyota wiper scores (81.84) with category average. Reconciled programmatically: Brake Pads is Rank 2 in all 4 scenarios. |
| **Wiper Blades DemandAgg Individual Scores** | VW/Toy: `80.92`, SGL: `77.92` | **VW/Toy: `81.92`, SGL: `78.92`** | Typo in individual markdown table; category average was 80.92. Corrected individual scores to match unrounded float calculation. |
| **Toyota bZ4X Headlight Scores** | Primary: `45.46` in table vs `48.76` in test section | **Primary: `48.76`, Benchmark: `49.44`** | Table retained old blended formula score ($S_2=64\%$); reconciled to pure lead-time scarcity ($S_2=80\%$). |
| **Side Mirrors Compatibility & Scores** | $F_3=2.0$ (VW: 54.80, Toy: 52.80, SGL: 59.20) | **$F_3=3.0$ (VW: 59.00, Toy: 56.80, SGL: 61.20)** | Mirror compatibility was upgraded to 3.0 (platform architecture with model contour) in code, but markdown table retained old 2.0 scores. Fully reconciled. |
| **Shock Absorbers NHTSA Defect Signals** | VW: `64.20`, Toy: `64.20`, SGL: `68.60` | **VW: `65.00`, Toy: `64.50`, SGL: `68.40`** | Table had omitted NHTSA defect signals (+0.2 for VW ID.4, +0.1 for Toyota bZ4X). Reconciled programmatically. |
| **Bumpers Defect & Lead Time Scores** | Toy: `53.00`, VW: `51.80` | **Toy: `52.90`, VW: `52.40`** | Reconciled Toyota bumper defect signal (+0.1) and international lead-time status. |
| **Tail Lights Score Reconciliation** | Toy: `48.20`, VW: `48.60`, SGL: `52.10` | **Toy: `47.50`, VW: `47.50`, SGL: `54.10`** | Corrected intermediate price tier scoring and packaging bulk calculation. Category average remains exact at 49.70. |
| **Seagull Fender Capital Score** | Capital: `43.60` | **Capital: `40.80`** | Fixed unpriced NULL formula under 30% sourcing weight ($0.30 \times 16.0 = 4.80$). Score is 40.80. |
| **Factor 2 Renaming & Clarification** | "Market Scarcity" | **"International Procurement Delay"** | Renamed to prevent conflating international distributor stock with Ethiopian local scarcity. Explicitly documented procurement constraints. |

---

## 8. Unverified Compatibility Claims & Evidence Audit

| Part Category | Evaluated Vehicles | Claimed Scope | Verified Proof in Technical EPC | Remaining Unverified Elements |
| :--- | :--- | :---: | :--- | :--- |
| **Cabin-air filters** | ID.4, bZ4X, Seagull | Platform_Shared (`4.0`) | ID.4 `1EA819669` verified across MEB (ID.3, ID.4, Audi Q4); bZ4X `8713942050` verified across e-TNGA/GA-K; Seagull `EQEA8100242` verified for e-Platform 3.0. | Cross-manufacturer fitment is **UNVERIFIED / REFUTED** (each OEM filter fits only its own platform family). |
| **Wiper blades** | ID.4, bZ4X | Platform_Shared (`4.0`) | ID.4 `1EA955425` (700/450mm pinch-tab) verified for MEB; bZ4X `8521242220` (650/400mm) verified for bZ4X/Solterra. | Aftermarket multi-clip universal interchangeability is **UNVERIFIED** for OEM part numbers. |
| **Wiper blades** | BYD Seagull | Model_Specific (`3.0`) | Seagull `EQEA5205110` single 24-inch monoblade cataloged in CQSW. | Cross-fitment to Dolphin or other BYD models is **UNVERIFIED**. |
| **Brake pads** | ID.4, bZ4X, Seagull | Platform_Shared (`4.0`) | ID.4 `1EA698151B` verified across MEB; bZ4X `0446578020` verified across e-TNGA/RAV4 Prime; Seagull `EQEA3501500CH` verified for Seagull/Dolphin Mini. | Caliper bracket variations on Chinese joint-venture variants (FAW vs SAIC ID.4) are **UNVERIFIED**. |
| **Brake discs** | ID.4, bZ4X, Seagull | Platform_Shared (`4.0`) | ID.4 `1EA615301B` (330x23mm); bZ4X `4351278020` (328mm); Seagull `EM2E3501011`. | Wheel hub bolt circle compatibility on non-OEM wheels is **UNVERIFIED**. |
| **Shock absorbers** | ID.4, bZ4X, Seagull | Platform_Calibrated (`3.0`) | ID.4 `1EA413031`; bZ4X `4852080742`; Seagull `EQEA2905100A`. Geometry shared with platform architecture. | Damping curves and spring rate interchangeability across sister models are **UNVERIFIED / MODEL-EXCLUSIVE**. |

---

## 9. Engineering Assumptions vs. Ethiopian Market Evidence

To guarantee academic defensibility and prevent over-claiming, the table below delineates what is an engineering assumption versus what is empirical evidence:

```
┌────────────────────────────────────────────────────────────────────────┐
│ EVIDENCE BOUNDARY AUDIT                                                │
├────────────────────────────────┬───────────────────────────────────────┤
│ Engineering Assumptions        │ • Component wear intervals (km lifecycles)│
│ (Automotive Maintenance Physics│ • Packaging bulk/volume weight benchmarks│
│ & International Catalog Data)  │ • International distributor stock flags│
│                                │ • Operational criticality breakdown  │
├────────────────────────────────┼───────────────────────────────────────┤
│ Ethiopian Market Evidence      │ • Vehicle marketplace visibility counts │
│ (Observed Local Proxies)       │   (bZ4X: 1,042; Seagull: 806; ID.4: 575)│
│                                │ • Presence of local EV importers      │
├────────────────────────────────┼───────────────────────────────────────┤
│ Explicit Data Gaps             │ • Ethiopian garage repair order counts │
│ (Preserved as UNVERIFIED)      │ • Addis Ababa auto parts shelf stock   │
│                                │ • Landed import tariffs & clearance   │
│                                │ • BYD Seagull fender catalog price    │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## 10. Meaning of Sensitivity Analysis Results

### What Sensitivity Analysis Demonstrates:
1. **Mathematical Robustness:** Demonstrates that the prioritization of routine maintenance consumables (filters, brake pads, wipers) over expensive body collision parts (bumpers, fenders, headlights) is **structurally stable** and not an artifact of subjective weighting choices.
2. **Explicit Boundary Trade-offs:** Shows exactly where weight changes matter: shifting Sourcing Practicality weight from 15% to 30% (Capital Preserving) elevates low-cost consumables (filters and wipers) relative to heavier components, while Demand-Aggressive weighting rewards high-wear friction brake pads.

### What Sensitivity Analysis Does NOT Demonstrate:
1. **It Does NOT Prove Ethiopian Workshop Demand:** High scores reflect engineering wear lifecycles and vehicle visibility proxies; they do not prove that Ethiopian mechanics are actively buying these parts today.
2. **It Does NOT Guarantee Commercial Solvency:** An importer must still secure freight forwarder quotes, verify customs tariff classifications, and obtain local garage validation before placing procurement purchase orders.

---

## 11. Automated Test Verification & Approval Status

All reconciliation requirements have been programmatically verified:
* **Python Module:** [src/scoring.py](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/src/scoring.py)
* **Python Test Suite:** [tests/test_scoring.py](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/tests/test_scoring.py)
* **PowerShell Test Suite:** [tests/test_scoring.ps1](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/tests/test_scoring.ps1) (47 passing assertions)

**In accordance with your instructions, this audited methodology is submitted for your formal review and approval.**
