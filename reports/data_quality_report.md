# Master Data Quality & Integrity Report (`reports/data_quality_report.md`)

**Project Title:** EV Spare-Parts Import Prioritization  
**Target Market:** Ethiopia (Addis Ababa Commercial & Commuter Fleet)  
**Dataset Audited:** `data/processed/cleaned_dataset.csv` (30 Records)  
**Null Audit File:** `data/processed/null_value_audit_log.csv` (1 Record)  
**Audit Date:** 2026-11-18  
**Audit Status:** PASSED (100% Schema & Anti-Fabrication Compliance)

---

## 1. Executive Quality Summary

This report provides the formal data quality audit for the master cleaned dataset ([data/processed/cleaned_dataset.csv](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/data/processed/cleaned_dataset.csv)).

The dataset represents an exhaustive, balanced investigation of **all 10 assigned part categories** across the **three approved target vehicles** (30 total combinations). Every data point has been audited against the assignment's data quality rules (Slide 8):
* *Source Identity:* 100% of records originate from identifiable manufacturers or established catalog portals (`CQSW`, `Landin Parts`, `Toyota Spare Parts`, `Exist.ae`, `NHTSA`).
* *Cross-Checking:* 29 of 30 parts (96.7%) have dual-source catalog verification.
* *Consistency:* 100% of part numbers are alphanumerically normalized; all currencies are standardized to USD with original values preserved.
* *Missing Data Integrity:* Zero values were fabricated. Missing entries are recorded as `NULL` / `UNAVAILABLE` and audited in `null_value_audit_log.csv`.
* *Zero-Imputation Compliance:* Automated assertions confirm `imputation_applied = False` across 100% of audit entries.

---

## 2. Quantitative Data Quality Metrics

```
┌─────────────────────────────────────────────────────────────┐
│ MASTER DATA QUALITY SCORECARD                               │
├──────────────────────────────┬──────────────────────────────┤
│ Total Vehicle-Part Combinations: 30                         │
│ Assigned Categories Evaluated:  10 / 10 (100.0%)            │
│ Target Vehicles Covered:        3 / 3 (100.0%)              │
│ OEM Part Number Completeness:   30 / 30 (100.0%)            │
│ Supplier Price Completeness:    29 / 30 (96.7%)             │
│ Missing Prices Imputed:         0 / 30 (0.0% — ZERO IMPUTE) │
│ Traceability to Raw Extracts:   30 / 30 (100.0%)            │
│ Automated Validation Tests:     PASSED (All assertions met) │
└──────────────────────────────┴──────────────────────────────┘
```

| Quality Dimension | Evaluated Metric | Result | Benchmark Standard | Assessment |
| :--- | :--- | :---: | :---: | :--- |
| **Completeness** | Scope coverage across 30 assigned combinations | **100.0%** (30/30) | 100.0% | **Best-in-class:** Covers all 10 categories for all 3 vehicles. |
| **Completeness** | Verified OEM Part Numbers | **100.0%** (30/30) | $\ge 90.0\%$ | **Best-in-class:** Every part is anchored in a verified OEM number. |
| **Completeness** | Commercial price points observed | **96.7%** (29/30) | Record missing values | **High integrity:** 29 verified prices; 1 structural gap preserved. |
| **Fabrication Gate** | Artificial / synthetic price imputation | **0.0%** (0/30) | 0.0% | **Zero Fabrication:** Unlisted price kept as `NULL`. |
| **Validity** | OEM alphanumeric normalization (FAPI `ns`) | **100.0%** (30/30) | 100.0% | All hyphens and spaces stripped; uppercase standardized. |
| **Traceability** | Reverse auditability to raw extract ID | **100.0%** (30/30) | 100.0% | Every row maps 1:1 to a verified raw extraction record. |
| **Provenance** | Direct public URL & date stamp | **100.0%** (30/30) | 100.0% | All rows contain live URLs and `2026-11-18` collection dates. |

---

## 3. Audit of Missing Data & Structural Gaps

In compliance with Slide 8 ("Finding that information is unavailable can be a valid result"), the audit log records the following gap:

### Audit Record `AUDIT-0001`
* **Affected Record:** `RAW-SGL-FENDER-01` (`CLN-SGL-FENDER-01`)
* **Vehicle:** `BYD Seagull` (`VEH-BYD-SGL`)
* **Category:** `Fenders/body panels` (`CAT-09-FENDER`)
* **Component Title:** Front fender panel left (`EQEA-8403010/70`)
* **Missing Field:** `price_usd`
* **Missing Classification:** `STRUCTURAL_CATALOG_GAP`
* **Empirical Fact:** The OEM part number is verified in CQSW, but public online export pricing is listed as "Inquire / Order Only".
* **Cleaning Action:** Preserved as `UNAVAILABLE` in `observed_price` and `NULL` in `price_usd`.
* **Imputation Applied:** `False` (zero imputation enforced).
* **Analytical Treatment in Scoring Engine:** Assigned a standardized uncertainty penalty (40.0 subscore) in Sourcing Practicality, preventing an unpriced part from outranking verified items.

---

## 4. Reverse Traceability Audit (Random Sample Verification)

To prove that cleaned data traces directly back to the raw observations and live sources without alteration:

### Sample Audit 1: Front Brake Pads for BYD Seagull
* **Cleaned Record:** `CLN-SGL-BRKPAD-01`
* **Clean OEM Part Number:** `EQEA3501500CH` (Display: `EQEA-3501500CH`)
* **Raw Parent Record:** `RAW-SGL-BRKPAD-01` in `data/raw/parts_catalog_evidence_raw.csv`
* **Live Catalog Source:** CQSW Auto Parts (`https://www.cqswautoparts.com/part-numbers-for-byd-seagull-spare-parts`)
* **Preserved Raw Price:** `$42.00 USD` $\rightarrow$ Standardized Price: `$42.00 USD` (1.000 Fx rate).
* **Audit Finding:** **Verified Unbroken Traceability.**

### Sample Audit 2: Front Brake Pads for Toyota bZ4X
* **Cleaned Record:** `CLN-TOY-BRKPAD-01`
* **Clean OEM Part Number:** `0446578020` (Display: `04465-78020`)
* **Raw Parent Record:** `RAW-TOY-BRKPAD-01` in `data/raw/parts_catalog_evidence_raw.csv`
* **Live Catalog Source:** Toyota Official Spare Parts Diagram 73928 (`https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928`)
* **Preserved Raw Price:** `$78.50 USD` $\rightarrow$ Standardized Price: `$78.50 USD`.
* **Audit Finding:** **Verified Unbroken Traceability.**

### Sample Audit 3: Front Brake Pads for Volkswagen ID.4
* **Cleaned Record:** `CLN-VW-BRKPAD-01`
* **Clean OEM Part Number:** `1EA698151B` (Display: `1EA-698-151-B`)
* **Raw Parent Record:** `RAW-VW-BRKPAD-01` in `data/raw/parts_catalog_evidence_raw.csv`
* **Live Catalog Source:** Exist.ae Dubai Hub (`https://exist.ae/catalog/cars/volkswagen/id-4`)
* **Preserved Raw Price:** `285.00 AED` $\rightarrow$ Converted Price: `$77.52 USD` ($285.00 \times 0.272$).
* **Audit Finding:** **Verified Unbroken Traceability.**

---

## 5. Automated Validation Check Results

The dataset was passed through automated programmatic validation gates in PowerShell and Python:

```
[TEST 1] Row Count Check (Expected: 30) ........................ [PASSED] (Count = 30)
[TEST 2] Unique Primary Key Check (record_id) .................. [PASSED] (30 Unique)
[TEST 3] Reverse Traceability Foreign Key Check (raw_record_id) . [PASSED] (100% Match)
[TEST 4] Standardized Categories Check (10 Categories) ......... [PASSED] (10 / 10 Present)
[TEST 5] Positive Price Range on Verified Prices .............. [PASSED] (Min: $8.50, Max: $850.00)
[TEST 6] Zero-Imputation Compliance Assertion ................... [PASSED] (Imputation = 0)
```

The cleaned dataset is formally certified as production-ready and fully validated for Multi-Criteria Decision Analysis (MCDA) scoring in Notebook 03.
