# Reference Repository Reuse and Implementation Justification Report
## Technical Attribution, Architectural Adaptation, and Decision Boundary Governance

**Document Version:** 1.0.0 (Stage 6 Implementation Review)  
**Execution Date:** November 2026  
**Repository Location:** [`reports/reuse_and_implementation_justification_report.md`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/reports/reuse_and_implementation_justification_report.md)  
**Target Market:** Addis Ababa, Ethiopia (Commercial EV Spare-Parts Importer Pilot: USD 5,000–10,000)  
**Related Documents:**
- Citation and Reuse Log: [`reports/citation_and_reuse_log.md`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/reports/citation_and_reuse_log.md)
- Reference Architectural Audits: [`reference_repository_analysis/`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/reference_repository_analysis/)
- Final Recommendation Report: [`results/recommendation_report.md`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/results/recommendation_report.md)

---

## 1. Executive Summary & Core Governance Principles

This report provides a comprehensive, component-by-component audit of how code, database schemas, and supply-chain theories from the **three reference repositories** were evaluated, adopted, modified, or rejected in this project.

### Core Governance Principles
1. **Academic & Legal Attribution:** All three upstream repositories are licensed under the **MIT License**. Full copyright notices, repository origins, and upstream author attributions are preserved in this repository.
2. **Zero False Originality Claims:** We explicitly distinguish between components reused directly, components adapted with documented modifications, and components developed specifically for this project. No external code is claimed as original work.
3. **The Target-Market Boundary (Slide 12 Compliance):**
   > [!IMPORTANT]
   > **Implementation Support vs. Market Conclusions:**
   > The reference repositories supported **software architecture, relational data modeling, part-number string cleaning, and inventory classification theory**. They did **NOT** provide any empirical Ethiopian market demand data, Addis Ababa vehicle registration counts, EV parts catalog pricing, or local procurement conclusions. All commercial prioritization conclusions are derived strictly from our independent empirical research into the Addis Ababa EV market.

---

## 2. Inventory of Reference Repositories

| Repository Name | Upstream Author / Entity | Source Location / URL | Upstream License | Core Architectural Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`automotive-part-interchange-database`** | Erin Chapman (`3r1nC`) | [GitHub: `3r1nC/automotive-part-interchange-database`](https://github.com/3r1nC/automotive-part-interchange-database) | MIT License (2026) | 4-tier relational schema and SQLite search queries for cross-referencing automotive parts across vehicles. |
| **`auto-parts-cross-reference`** | FAPI / IISIS (`fapi-dev`) | [GitHub: `fapi-dev/auto-parts-cross-reference`](https://github.com/fapi-dev/auto-parts-cross-reference) | MIT License (Schema/Code) / Custom Evaluation (`DATA-LICENSE.md`) | Production cross-reference schema, alphanumeric string normalizer (`ns`), OE/aftermarket flags (`tp`), and evidence ratings (`r`). |
| **`SparePartsInventory`** | Priyanshu Raj (`vivasvana1`) | [GitHub: `vivasvana1/SparePartsInventory`](https://github.com/vivasvana1/SparePartsInventory) | MIT License (2025) | Intermittent-demand forecasting, ABC-XYZ inventory classification matrices, safety stock, and holding vs. stockout optimization. |

---

## 3. Detailed Component-by-Component Reuse Analysis

### 3.1 Component 1: Alphanumeric Part Number String Normalization (`normalize_part_number`)

* **Original Repository:** `auto-parts-cross-reference` (FAPI)
* **Original File / Component:** `scheme.sql` — the `ns character varying(105)` field definition across `product_list` and `analog_list`.
* **Original Purpose:** In the FAPI commercial database, `ns` (Normalized String) serves as an indexing key that strips all punctuation, whitespace, and case differences to enable high-speed search across international supplier catalogs.
* **How It Was Used in Our Project:**
  Implemented as a core data-cleaning function `normalize_part_number()` in [`src/data_cleaning.py`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/src/data_cleaning.py) and verified via automated unit tests in [`tests/test_part_normalizer.py`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/tests/test_part_normalizer.py).
* **What Was Modified:**
  1. *Language & Runtime Translation:* FAPI defined `ns` as a database column generated via SQL triggers/ETL. We translated the algorithm into a pure Python function using regular expressions:
     $$\text{CleanPartNo} = \text{RegExSub}(r"[\wedge A\text{-}Z0\text{-}9]", \, "", \, \text{InputString}.\text{upper}())$$
  2. *Missing Data & Zero-Imputation Handling:* Added strict checks for missing and null values. If an input is `None`, `NaN`, `"NULL"`, or empty, the function returns `"UNAVAILABLE"` rather than failing or fabricating an empty string, preserving data auditability.
* **Why It Was Useful:**
  Chinese supplier catalogs (CQSW, Landin) and Middle Eastern portals (Exist.ae) frequently format the same OEM part number with inconsistent hyphens, spaces, or dots (e.g., `EQEA-8100242` vs. `EQEA8100242` vs. `EQEA.8100242`). Normalization prevented false-negative search mismatches and duplicate SKU entries.
* **Relevant Limitations:**
  The FAPI `ns` standard does not handle non-Latin characters (e.g., Chinese characters sometimes appended in domestic BYD parts descriptions) and does not capture OEM supersession chains (where an older OEM number is superseded by a newer design revision).

---

### 3.2 Component 2: Relational Fitment & Interchange Data Architecture

* **Original Repository:** `automotive-part-interchange-database`
* **Original File / Component:** `database/schema.sql` — relational tables `vehicles`, `parts`, `cross_references`, and `fitment`.
* **Original Purpose:** To provide a normalized SQLite database structure that separates physical parts from vehicle applications via a junction table (`fitment`), allowing parts to be linked to multiple car models.
* **How It Was Used in Our Project:**
  Adapted into our master dataset design ([`data/processed/cleaned_dataset.csv`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/data/processed/cleaned_dataset.csv) and [`methodology/dataset_design.md`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/methodology/dataset_design.md)) to track candidate vehicle-part combinations.
* **What Was Modified:**
  1. *EV Domain Transformation:* Replaced legacy combustion engine fields (`engine`, `fuel_type`, `displacement`) with EV-specific parameters (`vehicle_platform`, `battery_kwh`, `powertrain_type`, `drive_configuration`).
  2. *Provenance Tracking:* Added mandatory data governance columns (`source_name`, `source_url`, `collection_date`, `uncertainty_flag`, `catalog_completeness_cci`, `decision_completeness_dci`) that were absent from Chapman's schema.
  3. *Tabular Pipeline Integration:* While Chapman implemented a live SQLite database, we structured our pipeline around version-controlled CSV files and Pandas DataFrames to guarantee zero-dependency reproducibility across platforms.
* **Why It Was Useful:**
  Prevented redundant cataloging and enforced vehicle-part decoupling. This allowed the scoring engine to evaluate platform-shared parts (e.g., Toyota e-TNGA components shared with RAV4 Prime, or MEB components shared with Audi Q4 e-tron) without duplicating part definitions.
* **Relevant Limitations:**
  Chapman's schema treats fitment as binary (compatible vs. incompatible). It lacks nuance for regional trim variations, PR-code caliper variations (e.g., FAW vs. SAIC ID.4 brake brackets), or partial fitments.

---

### 3.3 Component 3: Multi-Source Evidence Confirmation Metric ($r$-Rating Adaptation)

* **Original Repository:** `auto-parts-cross-reference` (FAPI)
* **Original File / Component:** `scheme.sql` — the `r integer NOT NULL` attribute in table `analog_list`.
* **Original Purpose:** In FAPI, `r` represents an integer rating reflecting the net number of independent commercial suppliers confirming a cross-reference link minus those disputing it.
* **How It Was Used in Our Project:**
  Adapted into our **Factor 5: Evidence Confidence** ($F_5$) scoring rubric and the **Catalog Completeness Index (CCI)**.
* **What Was Modified:**
  FAPI's raw integer count was expanded into a structured, weighted multi-attribute verification scale evaluated out of 5.0 points:
  $$F_5 = 2.0 \times C_{\text{cat}} + 1.5 \times C_{\text{price}} + 1.5 \times C_{\text{fit}}$$
  where catalog traceability ($C_{\text{cat}}$), verified multi-source pricing ($C_{\text{price}}$), and fitment documentation ($C_{\text{fit}}$) are scored independently. Under our Stage 5B/5C audit, single-source catalog observations are capped at $F_5 = 4.00$, directly reflecting FAPI's principle that multi-source confirmation yields higher reliability.
* **Why It Was Useful:**
  Prevented unverified supplier claims from being treated with equal confidence as rigorously documented OEM catalog records.
* **Relevant Limitations:**
  Our empirical dataset achieved single-source catalog verification across 29 priced records, but lacked secondary independent pricing ($C_{\text{price}} = 0.67$).

---

### 3.4 Component 4: ABC-XYZ Inventory Prioritization & Holding-Cost Theory

* **Original Repository:** `SparePartsInventory`
* **Original File / Component:** `notebooks/03_exploratory_data_analysis.ipynb` & `notebooks/05_inventory_optimization.ipynb`.
* **Original Purpose:** Enterprise supply-chain optimization classifying spare parts by annual dollar consumption (ABC: High/Medium/Low value) and demand volatility (XYZ: Steady/Variable/Erratic), optimizing safety stock against holding costs.
* **How It Was Used in Our Project:**
  Served as the theoretical foundation for our **Factor 4: Sourcing Practicality** ($F_4$), operational criticality classification, and pilot portfolio design.
* **What Was Modified:**
  1. *Mathematical Translation:* Replaced complex continuous-demand stochastic inventory formulas (Croston's method, Poisson replenishment) with a multi-criteria scoring model tailored for a capital-constrained importer with zero historical sales data.
  2. *EV Category Mapping:*
     * *Fast-Moving Consumables (Cabin filters, wiper blades):* Mapped to **Class C-X / B-X** (low unit cost, high turnover velocity, steady wear). Prioritized to maximize inventory turn and protect working capital.
     * *Safety Wearables (Brake pads):* Mapped to **Class B-X** (moderate unit cost, high operational criticality).
     * *Collision / Structural Panels (Bumpers, headlights, fenders):* Mapped to **Class A-Z** (high capital cost, erratic accidental demand, high holding cost, bulky storage).
* **Why It Was Useful:**
  Provided an unshakeable commercial supply-chain rationale for why a USD 5,000–10,000 pilot capital tranche must prioritize low-cost, fast-moving maintenance consumables over high-dollar structural panels.
* **Relevant Limitations:**
  Raj's model assumes established historical demand distributions and known holding cost percentages, which must be treated as commercial hypotheses in an emerging market like Ethiopia.

---

## 4. Useful Architectural Ideas Deliberately Rejected & Justifications

In compliance with the assignment instructions, we evaluated several technical concepts from the reference repositories but **deliberately rejected them**:

### 4.1 Rejection 1: Ingestion of FAPI Sample Cross-Reference Data (`analog_list.txt`)
* **What Was Rejected:** 22,550 cross-reference link records, 13,869 products, and 1,506 manufacturers from `auto-parts-cross-reference`.
* **Why It Was Rejected:**
  1. **Legal Constraint:** FAPI's `DATA-LICENSE.md` explicitly specifies: *"You may not redistribute the sample, publish it elsewhere, or use it in a product or a service. All rights in the data are reserved."* Ingesting this data into our public repository would violate upstream intellectual property rights.
  2. **Irrelevant to Ethiopian EV Market:** The sample data consists of legacy internal combustion engine (ICE) parts for European and American passenger cars (e.g., Renault Clio, Ford Focus, Opel Astra). It contains **zero records for BYD Seagull, Toyota bZ4X, or VW ID.4**.
  3. **Zero-Fabrication Compliance:** Slide 12 notes explicitly mandate: *"FAPI sample data is for evaluation and is not market-demand evidence."* Using FAPI data as a proxy for Addis Ababa demand would constitute academic and professional misconduct.

---

### 4.2 Rejection 2: Streamlit Interactive Web Application (`src/app.py`)
* **What Was Rejected:** The Streamlit dashboard interface from `automotive-part-interchange-database`.
* **Why It Was Rejected:**
  1. **Scope Alignment:** The assignment deliverables mandate reproducible Jupyter notebooks, publication-ready high-resolution static charts (`.png`), and standalone executive Markdown reports, NOT an interactive web server.
  2. **Auditability & Portability:** Streamlit introduces heavy web server dependencies, session state management overhead, and browser rendering variances. A script-based pipeline generating deterministic CSVs and PNGs ensures 100% reproducible execution in headless automated testing environments.

---

### 4.3 Rejection 3: IBM ILOG CPLEX & AnyLogistix Optimization Infrastructure
* **What Was Rejected:** The Mixed-Integer Linear Programming (MILP) optimization models (`.mod`/`.dat`) and AnyLogistix discrete-event supply chain simulation files from `SparePartsInventory`.
* **Why It Was Rejected:**
  1. **Proprietary Licensing Barrier:** IBM CPLEX and AnyLogistix are proprietary enterprise software suites requiring paid commercial licenses. Using them would prevent independent verification and break open-source reproducibility.
  2. **False Precision for Pilot Market:** Mathematical programming models like CPLEX require detailed input parameters: holding cost rates ($H$), fixed order costs ($S$), penalty stockout costs per day ($\pi$), and lead-time probability density functions ($f(L)$). In Addis Ababa's nascent EV market, none of these parameters can be measured with empirical rigor. Forcing arbitrary numbers into an MILP solver creates dangerous "black-box" false precision. Our explainable MCDA scoring model is far more defensible and transparent.

---

### 4.4 Rejection 4: Synthetic Historical Demand Time Series
* **What Was Rejected:** Historical transaction logs and daily demand time-series spreadsheets from `SparePartsInventory`.
* **Why It Was Rejected:**
  * The transaction series in `SparePartsInventory` reflect synthetic industrial machinery parts demand. They have zero relation to Addis Ababa's climate, road conditions, or EV fleet operations. Ingesting synthetic sales logs would corrupt the empirical integrity of our demand scoring ($F_1$).

---

## 5. Summary Matrix of Code Reuse vs. Original Development

| System Component | Upstream Source Cited | Exact Reused Logic | Modifications & Custom Adaptations | Original Implementation (GechDev) |
| :--- | :--- | :--- | :--- | :--- |
| **Part Normalizer** | `auto-parts-cross-reference` | Alphanumeric stripping regex standard (`ns` concept). | Ported from SQL trigger to Python `src/data_cleaning.py`; added strict null handling (`UNAVAILABLE`). | Comprehensive unit test suite (`tests/test_part_normalizer.py`). |
| **Data Schema** | `automotive-part-interchange-database` | 4-tier relational structure separating vehicles, parts, and fitments. | Converted from ICE SQLite schema to EV Pandas/CSV architecture; added provenance and DCI/CCI columns. | Field definitions for EV platform, battery size, and Stage 5C audit flags. |
| **Inventory Logic** | `SparePartsInventory` | ABC-XYZ classification matrix principles and holding vs. stockout trade-offs. | Translated stochastic inventory theory into a 5-pillar Multi-Criteria Decision Analysis (MCDA) model. | The complete MCDA weighting engine, sensitivity pipeline, and tie-breaking algorithms. |
| **Catalog Evidence** | *None (Independent)* | *None (0% Reused)* | *None* | 100% original empirical evidence collected from Toyota, Exist.ae, and CQSW catalogs. |
| **Ethiopian Market Analysis** | *None (Independent)* | *None (0% Reused)* | *None* | 100% original analysis of Addis Ababa vehicle visibility, environmental factors, and pilot risks. |

---

## 6. Target-Market Boundary Declaration

We explicitly certify that:
1. **The reference repositories provided technical scaffolding, software design patterns, and theoretical supply-chain heuristics.**
2. **The reference repositories DID NOT provide any empirical findings regarding the Ethiopian automotive market, Addis Ababa vehicle populations, or EV spare-parts demand.**
3. **All conclusions regarding the final five recommended parts (`CLN-SGL-CABFILT-01`, `CLN-TOY-CABFILT-01`, `CLN-VW-CABFILT-01`, `CLN-TOY-WIPER-01`, `CLN-VW-WIPER-01`) were derived entirely from our independent empirical research and audited scoring model.**

---
*Report certified compliant with Stage 6 academic and intellectual property standards.*
