# Data Cleaning, Normalization & Audit Methodology (`methodology/data_cleaning.md`)

**Document Type:** Formal Data Pipeline & Transformation Documentation  
**Author / Analyst:** GechDev  
**Repository:** `ev-spare-parts-import-prioritization`  
**Input Datasets:** `data/raw/parts_catalog_evidence_raw.csv`, `data/raw/nhtsa_safety_signals_raw.csv`  
**Output Datasets:** `data/processed/cleaned_dataset.csv`, `data/processed/null_value_audit_log.csv`  
**Status:** Executed, Documented & Validated Pipeline

---

## 1. Overview & Pipeline Philosophy

The primary objective of the data cleaning pipeline is to convert raw, heterogeneous catalog extracts into a mathematically consistent, standardized master dataset without losing source provenance or fabricating unverified data.

The pipeline is implemented programmatically in Python (`src/data_cleaning.py`) and executed through Jupyter notebooks (`notebooks/02_parts_cataloguing_and_cleaning.ipynb`). It follows a strict 10-step transformation protocol:

```
[Raw Catalog Ingestion] ──> [Vehicle Standardization] ──> [Category Harmonization]
           │
[Part Number Normalization] ──> [Currency Conversion] ──> [Missing Value Auditing]
           │
[Compatibility Typing] ──> [Defect Signal Merging] ──> [Validation Gate & Export]
```

---

## 2. The 10 Step-by-Step Data Transformations

### Transformation 1: Standardization of Vehicle Names and Identifiers
* **Raw State:** Heterogeneous strings across sources (e.g., `2020 Byd seagull`, `SEAGULL 2023`, `Toyota BZ4X 2023`, `FAW-VW ID.4 Crozz`, `Volkswagen ID.4`).
* **Cleaning Rule:** Standardized into canonical entity codes:
  * `VEH-BYD-SGL` $\rightarrow$ Make: `BYD`, Model: `Seagull`, Variant: `2023-present / FWD (Vitality/Flying)`, Platform: `e-Platform 3.0`.
  * `VEH-TOY-BZ4X` $\rightarrow$ Make: `Toyota`, Model: `bZ4X`, Variant: `2023-present / FWD & AWD (XEAM10)`, Platform: `e-TNGA Platform`.
  * `VEH-VW-ID4` $\rightarrow$ Make: `Volkswagen`, Model: `ID.4`, Variant: `2020-present / RWD & AWD (Pro/Crozz)`, Platform: `MEB Platform`.

### Transformation 2: Standardization of Part Category Names
* **Raw State:** Varying naming conventions (e.g., `Front brake pad`, `Disc brake pad kit`, `Front bumper--upper`, `Head Lamps`, `Outer rearview mirror`).
* **Cleaning Rule:** Mapped strictly into the 10 assigned categories from Slide 5:
  1. `Brake pads` (`CAT-01-BRKPAD`)
  2. `Brake discs` (`CAT-02-BRKDISC`)
  3. `Cabin-air filters` (`CAT-03-CABFILT`)
  4. `Wiper blades` (`CAT-04-WIPER`)
  5. `Headlights` (`CAT-05-HEADLIGHT`)
  6. `Tail lights` (`CAT-06-TAILLIGHT`)
  7. `Side mirrors` (`CAT-07-MIRROR`)
  8. `Bumpers` (`CAT-08-BUMPER`)
  9. `Fenders/body panels` (`CAT-09-FENDER`)
  10. `Shock absorbers` (`CAT-10-SHOCK`)

### Transformation 3: Alphanumeric String Normalization (FAPI `ns` Principle)
* **Raw State:** Inconsistent punctuation across suppliers (e.g., `EQEA-3501500CH`, `EQEA-8403010/70`, `04465-78020`, `1EA-698-151-B`, `1EA.819.669`).
* **Cleaning Rule:** Adapted directly from the FAPI Auto Parts Cross-Reference database schema (`product_list.ns`). All hyphens, slashes, periods, and spaces are removed, and characters are converted to uppercase:
  $$\text{CleanPartNo} = \text{RegExReplace}(\text{RawPartNo}, \, [\wedge A\text{-}Z0\text{-}9], \, \text{""})$$
  * `EQEA-3501500CH` $\rightarrow$ `EQEA3501500CH`
  * `04465-78020` $\rightarrow$ `0446578020`
  * `1EA-698-151-B` $\rightarrow$ `1EA698151B`
* **Preservation:** The original human-readable catalog representation is preserved in `display_oem_part_number`.

### Transformation 4: Currency Standardization to USD
* **Raw State:** Multi-currency supplier quotes (`USD`, `CNY`, `AED`).
* **Cleaning Rule:** Converted to standardized USD ($) using fixed benchmark rates as of collection date (2026-11-18):
  * `1.00 USD = 1.000 USD` (Base)
  * `1.00 CNY = 0.138 USD` (Chinese Yuan from Landin Parts)
  * `1.00 AED = 0.272 USD` (UAE Dirham from Exist.ae)
  * Formula: $\text{PriceUSD} = \text{Round}(\text{ObservedPrice} \times \text{FxRate}, \, 2)$
* **Example:** VW ID.4 brake pads quoted at `285.00 AED` convert to `285.00 \times 0.272 = $77.52 USD`.

### Transformation 5: Preservation of Original Commercial Values
* **Cleaning Rule:** To ensure commercial audibility, original catalog values (`observed_price` and `observed_currency`) are preserved unaltered in parallel columns alongside `price_usd`.

### Transformation 6: Deduplication & Multi-Source Synthesis
* **Cleaning Rule:** Where multiple sources confirm the same component (e.g., CQSW and Landin both listing BYD Seagull shock absorbers), records are consolidated into a single master SKU rather than duplicate rows. The source verification counter is incremented, and `evidence_confidence` is designated as `High (Dual-Source Verified)`.

### Transformation 7: Explicit Missing Value Encoding (Zero vs. Unavailable)
* **Cleaning Rule:** In accordance with Slide 8 ("Record unavailable values instead of inventing them"):
  * A missing price is **never** coded as `0` or `$0.00`.
  * In `cleaned_dataset.csv`, unlisted prices are set to `NULL` in `price_usd` and `UNAVAILABLE` in `observed_price`.
  * The record is tagged with `price_data_status = UNAVAILABLE_GAP`.
* **Execution:** Exactly one component—the BYD Seagull front fender (`RAW-SGL-FENDER-01`)—had an unlisted public supplier price and was coded as `NULL`.

### Transformation 8: Formal Null-Audit Logging
* **Cleaning Rule:** The pipeline automatically writes missing data events to `data/processed/null_value_audit_log.csv`.
* **Observed Entry:**
  * `audit_id`: `AUDIT-0001`
  * `record_id`: `RAW-SGL-FENDER-01`
  * `vehicle_id`: `VEH-BYD-SGL`
  * `attribute_name`: `price_usd`
  * `missing_category`: `STRUCTURAL_CATALOG_GAP`
  * `imputation_applied`: `False` (zero imputation enforced)
  * `analyst_impact_note`: *"Supplier price unlisted online; penalized in scoring engine under sourcing practicality."*

### Transformation 9: Compatibility Scope & Platform Mapping
* **Cleaning Rule:** Parts are categorized into three distinct compatibility scopes:
  * `Universal`: Cabin filters and wiper blades sharing standardized sizing profiles.
  * `Platform_Shared`: Components fitting multiple models across modular architectures (VAG MEB platform, Toyota e-TNGA / RAV4 Prime, BYD e-Platform 3.0).
  * `Model_Specific`: Components restricted to one specific vehicle body (e.g., bumpers, headlights, sheet metal fenders).

### Transformation 10: Ingestion of Empirical Defect Signals (NHTSA)
* **Cleaning Rule:** Official recalls and consumer failure complaints from the NHTSA API are mapped by vehicle and component group:
  * Toyota bZ4X: 4 recalls, 7 complaints (mapped to bumpers, suspension, and HVAC).
  * VW ID.4: 14 recalls, 5 complaints (mapped to suspension struts and HVAC).
  * BYD Seagull: Set to `0` defect signals and explicitly tagged as `GEOGRAPHIC_BOUNDARY_UNAVAILABLE`.

---

## 3. Data Quality Validation Gates

Prior to exporting the cleaned dataset, the pipeline executes automated programmatic assertions:

```python
# Validation Assertions Enforced in Pipeline:
assert len(cleaned_df) == 30, "Cleaned dataset must contain exactly 30 records (3 vehicles x 10 categories)"
assert cleaned_df["clean_oem_part_number"].notna().all(), "All OEM numbers must be populated or UNAVAILABLE"
assert (cleaned_df[cleaned_df["price_data_status"] == "VERIFIED_PRICE"]["price_usd"].astype(float) > 0).all(), "Verified prices must be positive"
assert (cleaned_df["imputation_applied"] == False).all(), "Imputation must strictly be False across all audit records"
```

All 30 records passed validation successfully with 100% schema compliance.
