# Dataset Architecture & Design Specification (`methodology/dataset_design.md`)

**Document Type:** Formal Technical Specification & Schema Justification  
**Author / Analyst:** GechDev  
**Repository:** `ev-spare-parts-import-prioritization`  
**Dataset Produced:** `data/processed/cleaned_dataset.csv` (and `data/processed/ev_parts_master_dataset.csv`)  
**Status:** Complete & Schema-Validated Specification

---

## 1. Executive Summary & Design Mandate

Slide 7 of the official assignment brief establishes the core dataset requirements:
> *"You decide which fields support the import decision. Your dataset must still identify:  
> • Vehicle and part  
> • Source and collection date  
> • Compatibility evidence  
> • Price or availability evidence  
> • Basis for the recommendation  
> Explain your design: Why was each field included? How were duplicates and missing values handled? Which information could not be verified?"*

The resulting dataset design balances **mathematical rigor for scoring**, **supply chain traceability**, and **strict adherence to anti-fabrication standards**. Every field serves a distinct analytical purpose, cleanly distinguishing between primary empirical observations and derived analyst parameters.

---

## 2. Complete Field Dictionary & Justification Matrix

The cleaned dataset contains 29 fields organized into five logical tiers:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. IDENTITY & TRACEABILITY TIER (record_id, raw_record_id)  │
├─────────────────────────────────────────────────────────────┤
│ 2. VEHICLE CONTEXT TIER (make, model, trim, platform)       │
├─────────────────────────────────────────────────────────────┤
│ 3. COMPONENT TAXONOMY TIER (category, OEM part number, name)│
├─────────────────────────────────────────────────────────────┤
│ 4. COMMERCIAL EVIDENCE TIER (prices, currencies, stock)     │
├─────────────────────────────────────────────────────────────┤
│ 5. DECISION SUPPORT TIER (compatibility, NHTSA, basis)      │
└─────────────────────────────────────────────────────────────┘
```

| Field Name | Data Type | Requirement Source | Business & Analytical Justification |
| :--- | :---: | :--- | :--- |
| `record_id` | String | Integrity Standard | Unique primary key (`CLN-{VEH}-{CAT}-01`) ensuring unambiguous indexing across pipeline notebooks and SQL queries. |
| `raw_record_id` | String | Traceability Rule | Direct foreign key back to `data/raw/parts_catalog_evidence_raw.csv`, guaranteeing 100% reverse auditability from cleaned record to raw extraction. |
| `vehicle_id` | String | Assignment Mandate | Standardized vehicle entity code (`VEH-BYD-SGL`, `VEH-TOY-BZ4X`, `VEH-VW-ID4`) linking to visibility records. |
| `vehicle_make` | String | Assignment Mandate | Standardized automotive manufacturer name (`BYD`, `Toyota`, `Volkswagen`). |
| `vehicle_model` | String | Assignment Mandate | Standardized vehicle model name (`Seagull`, `bZ4X`, `ID.4`). |
| `vehicle_variant_trim`| String | Recommended Field | Discloses model year and drive configuration (e.g., `2023-present / FWD`, `XEAM10 / FWD & AWD`, `MEB Pro/Crozz`). Essential because braking and suspension components vary between FWD and AWD trims. |
| `vehicle_platform` | String | Compatibility Rule | Identifies modular architecture (`e-Platform 3.0`, `e-TNGA`, `MEB Platform`) to model cross-vehicle component interchangeability. |
| `category_id` | String | Standard Taxon | Unique alphanumeric category code (`CAT-01-BRKPAD` to `CAT-10-SHOCK`) ensuring stable sorting and categorical aggregation. |
| `part_category` | String | Assignment Mandate | Standardized title of the 10 assigned categories. Enforces consistent categorical filtering across models. |
| `functional_group` | String | Inventory Heuristic | Groups parts into `Fast_Moving_Wear`, `Periodic_Maintenance`, `Lighting_Assemblies`, `Collision_Exterior`, and `Suspension_Chassis` based on supply chain ABC-XYZ inventory turnover theory. |
| `part_name_clean` | String | Assignment Mandate | Harmonized English component title describing the exact physical assembly. |
| `clean_oem_part_number` | String | Recommended Field | Normalized OEM part number following FAPI `ns` standards (all hyphens, slashes, and spaces removed, standardized to uppercase). Prevents catalog search mismatches. |
| `display_oem_part_number` | String | Commercial Audit | Formatted original OEM part number (e.g., `04465-78020`, `EQEA-3501500CH`, `1EA-698-151-B`) for procurement ordering. |
| `supplier_name` | String | Recommended Field | Identifiable manufacturer, dealer portal, or catalog vendor (`CQSW / Landin`, `Toyota Spare Parts`, `Exist.ae`). |
| `observed_price` | String / Float | Assignment Mandate | Preserves original unmutated numerical price observation or `UNAVAILABLE`. Never overwritten or fabricated. |
| `observed_currency` | String | Assignment Mandate | Preserves original currency code (`USD`, `CNY`, `AED`) to maintain currency provenance. |
| `fx_rate_to_usd` | Float | Standardization Rule | Fixed benchmark exchange rate applied as of the collection date (2026-11-18) to ensure transparent, reproducible currency conversion. |
| `price_usd` | Float / String | Assignment Mandate | Converted price in standardized USD, or `NULL` if unlisted online. Serves as the quantitative input for capital outlay evaluation. |
| `price_data_status` | String | Data Quality Rule | Explicit indicator (`VERIFIED_PRICE` vs. `UNAVAILABLE_GAP`) distinguishing verified pricing from missing data gaps. |
| `availability_status` | String | Assignment Mandate | Standardized stock lead-time indicator (`In_Stock`, `Lead_Time_Required`, `Order_Only`). Direct input for the Market Scarcity scoring pillar. |
| `compatibility_scope` | String | Assignment Mandate | Multi-model fitment scope (`Universal`, `Platform_Shared`, `Model_Specific`). Input for the Compatibility scoring pillar. |
| `compatibility_evidence` | String | Assignment Mandate | Textual citation of shared platforms or vehicle applications confirming interchangeability (e.g., `Fits bZ4X and RAV4 Prime`, `Fits VW ID.4, ID.3, Audi Q4 e-tron`). |
| `compatibility_confidence` | String | Integrity Standard | Reliability tier (`Verified_OEM_Catalog` vs. `Uncertain_Cross_Check`). Enforces rule against assuming visual similarity equals compatibility. |
| `nhtsa_defect_count` | Integer | Failure Evidence | Total count of official NHTSA recalls and consumer failure complaints associated with the component subsystem (or `0` if none/unlisted). |
| `source_name` | String | Assignment Mandate | Primary publisher of evidence (`CQSW Auto Parts`, `Landin Parts`, `Toyota Spare Parts`, `Exist.ae`, `NHTSA API`). |
| `source_url` | String | Assignment Mandate | Clickable canonical web hyperlink where the observation was extracted. |
| `collection_date` | Date (ISO-8601) | Assignment Mandate | Retrieval date stamp (`YYYY-MM-DD`). Fixes evidence temporally to prevent stale data drift. |
| `evidence_confidence` | String | Quality Audit | Data verification level (`High (Dual-Source Verified)` vs. `Moderate (Single-Source Logged)`). |
| `recommendation_basis` | String | Assignment Mandate | Qualitative operational rationale explaining why the part category warrants import priority or caution from an inventory turnover and risk perspective. |
| `data_quality_notes` | String | Traceability Rule | Audit commentary documenting exact parent records, missingness tags, or catalog idiosyncrasies. |

---

## 3. Handling of Duplicates, Missing Data & Unverified Information

### 3.1 Handling Duplicate Observations
* **The Dual-Source Strategy:** When multiple sources confirm the same part (e.g., CQSW and Landin both listing BYD Seagull brake pads), we do **not** duplicate the row in the master dataset, which would distort statistical aggregations.
* **Resolution:** We consolidate the observation into a single canonical record, cite both sources, record the most reliable verified price point, and elevate the `evidence_confidence` field to `High (Dual-Source Verified)`.

### 3.2 Handling Missing Values (Zero-Fabrication Policy)
* **Distinguishing Unavailable from Zero:**  
  A critical failure mode in automotive data analysis is treating missing prices as $0.00. In our schema:
  * A price of `$0.00` means a part is free (which never occurs in commercial automotive imports).
  * An unlisted price is coded as `NULL` in `price_usd` and `UNAVAILABLE` in `observed_price`, accompanied by a `price_data_status = UNAVAILABLE_GAP` tag.
* **The Null-Audit Log:** Every missing attribute triggers an automated record in `data/processed/null_value_audit_log.csv` explicitly categorizing the gap (`STRUCTURAL_CATALOG_GAP` vs. `GEOGRAPHIC_BOUNDARY_UNAVAILABLE`) with `imputation_applied = False`.
* **Scoring Penalty:** In `src/scoring_engine.py`, missing price data receives a standardized uncertainty penalty (40.0 subscore) in Sourcing Practicality and zero bonus points in Evidence Confidence, ensuring that unverified items never outrank verified parts.

### 3.3 Identification of Unverifiable Information
The following parameters could not be verified from public online sources and are deliberately excluded to prevent analytical bias:
1. **Landed Ethiopian Import Duties & Clearing Surcharges:** Customs valuation requires physical bill-of-lading assessment by the Ethiopian Customs Commission. Prices are kept as catalog FOB/retail observations.
2. **Local Addis Ababa Retail Markup Spreads:** Ethiopian independent parts shops do not publish open APIs or catalog pricing.
3. **Domestic Field Failure Rates for BYD:** Because BYD models are not certified for US sale, NHTSA has zero records. This is flagged as a structural catalog boundary, not a zero-failure rate.

---

## 4. End-to-End Reverse Traceability

Every record in `cleaned_dataset.csv` traces back to its primary source through an unbroken evidentiary chain:

```
[Cleaned Record: CLN-SGL-BRKPAD-01]
  │
  ├── Linked via `raw_record_id` ──> [Raw Observation: RAW-SGL-BRKPAD-01]
  │                                    │
  │                                    ├── Preserves unparsed price ($42.00 USD)
  │                                    ├── Preserves raw description ("Front brake pad set 14758996-00")
  │                                    └── Preserves exact catalog URL (cqswautoparts.com/...)
  │
  └── Linked via `source_url`   ──> [Live Public Catalog Snapshot]
                                       └── Verified retrieval date: 2026-11-18
```

This ensures that an evaluator can click any URL in the dataset and immediately verify the underlying empirical evidence.
