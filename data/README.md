# Data Governance, Schema Architecture & Provenance Guidelines

## 1. Directory Structure

```
data/
├── README.md                                # This document
├── raw/                                     # Raw, unmodified extracts directly from source portals
│   ├── vehicle_visibility_raw.csv           # Marketplace & distributor listings extracts
│   ├── parts_catalog_evidence_raw.csv       # Online parts catalog observations
│   └── nhtsa_safety_signals_raw.csv         # NHTSA complaint & recall API extracts
└── processed/                               # Cleaned, standardized, schema-validated analysis datasets
    ├── ev_parts_master_dataset.csv          # Master harmonized dataset ready for scoring
    └── null_value_audit_log.csv             # Dedicated audit trail of missing/unverified fields
```

---

## 2. Core Data Governance Principles

1. **Separation of Raw and Processed Layers:**
   * Files in `data/raw/` must **never** be manually edited or overwritten once collected. They represent the immutable primary record of extraction.
   * All standardization, type casting, currency conversion, and missing-value logging must occur programmatically via `src/data_cleaning.py`.
2. **Zero Fabrication Policy:**
   * Missing prices, part numbers, compatibility details, or defect counts must **never** be imputed, guessed, or filled with synthetic averages.
   * If a supplier catalog does not list a price for a component, the price column is recorded as `NULL` / empty, and an entry is logged in `null_value_audit_log.csv`.
3. **Traceability Requirements:**
   * Every single row in both raw and processed datasets must contain:
     * `source_name`: The identifiable organization or platform (e.g., `Landin Parts`, `Gezat Electric`, `NHTSA`).
     * `source_url`: The exact hyperlink where the data was retrieved.
     * `collection_date`: The ISO-8601 date stamp (`YYYY-MM-DD`) when the observation was extracted.
4. **Proxy Boundary Enforcement:**
   * Marketplace listing counts from `Adey Market` or distributor listings from `Gezat Electric` are strictly classified as **visibility proxies**. They must **never** be labeled, aggregated, or interpreted as vehicle registrations or sales numbers.

---

## 3. Data Schemas & Field Dictionaries

### 3.1 Raw Vehicle Visibility Schema (`data/raw/vehicle_visibility_raw.csv`)

| Field Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `vehicle_id` | String | Unique candidate vehicle code | `VEH-BYD-SGL` |
| `make` | String | Vehicle manufacturer | `BYD` |
| `model` | String | Vehicle model name | `Seagull` |
| `generation_years` | String | Production year span | `2023-present` |
| `observed_platform` | String | Underlying EV architecture | `e-Platform 3.0` |
| `source_portal` | String | Platform where presence is noted | `Adey Market` |
| `source_url` | String | Direct URL of listing/showcase | `https://adey-market.com/...` |
| `collection_date` | Date | Date observed (`YYYY-MM-DD`) | `2026-11-18` |
| `listing_type` | String | Type of entry | `Marketplace Listing / Distributor Catalog` |
| `notes` | String | Factual observations on listing | `Offered by third-party importer in Addis` |

### 3.2 Raw Parts Catalog Evidence Schema (`data/raw/parts_catalog_evidence_raw.csv`)

| Field Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `raw_record_id` | String | Primary key for extraction record | `RAW-SGL-BRK-01` |
| `vehicle_id` | String | Target candidate vehicle code | `VEH-BYD-SGL` |
| `category_name` | String | One of the 10 assigned categories | `Brake pads` |
| `observed_part_number` | String | Part number exactly as shown | `BYD-1029384-A` |
| `oem_or_aftermarket` | String | Designation in catalog | `OEM Genuine / Aftermarket` |
| `observed_description`| String | Title/description in catalog | `Front Brake Pad Set` |
| `observed_price` | Float | Numeric price as listed | `45.00` |
| `observed_currency` | String | Currency code listed | `USD`, `CNY`, `AED` |
| `availability_status` | String | Stated stock status | `In Stock / Available to Order` |
| `source_name` | String | Catalog name | `Landin Parts` |
| `source_url` | String | Direct product page URL | `https://www.landinparts.com/...` |
| `collection_date` | Date | Date observed (`YYYY-MM-DD`) | `2026-11-18` |

### 3.3 Processed Master Dataset Schema (`data/processed/ev_parts_master_dataset.csv`)

| Field Name | Type | Description & Standards |
| :--- | :--- | :--- |
| `part_id` | String | Standardized identifier (e.g., `PART-SGL-BRKPAD-01`) |
| `vehicle_id` | String | Standardized vehicle code (`VEH-BYD-SGL`, `VEH-TOY-BZ4X`, `VEH-VW-ID4`) |
| `vehicle_make_model` | String | Standardized make and model name |
| `category_id` | String | Standardized category code (`CAT-01-BRKPAD` to `CAT-10-SHOCK`) |
| `category_name` | String | Official category name (one of the 10 assigned categories) |
| `functional_group` | String | `Fast_Moving_Wear`, `Periodic_Maintenance`, `Collision_Exterior`, `Suspension_Chassis` |
| `clean_oem_part_number` | String | Alphanumerically normalized OEM part number (stripping hyphens/spaces) |
| `clean_aftermarket_numbers` | String | Normalized aftermarket equivalents (comma-separated or `UNAVAILABLE`) |
| `part_description` | String | Harmonized standard English description |
| `price_usd_standardized` | Float | Converted price in USD, or `NULL` if unavailable |
| `original_currency` | String | Original currency before conversion |
| `fx_rate_to_usd` | Float | Exchange rate applied during conversion |
| `availability_flag` | String | `In_Stock`, `Lead_Time_Required`, `Unavailable` |
| `fitment_scope` | String | `Model_Specific`, `Platform_Shared`, `Universal` |
| `nhtsa_defect_signals` | Integer | Total complaint/recall records associated with component, or `0` |
| `source_verification_count` | Integer | Count of independent catalog sources confirming fitment ($r \ge 1$) |
| `primary_source_url` | String | Primary URL citation |
| `collection_date` | Date | Verification date (`YYYY-MM-DD`) |

### 3.4 Null-Value Audit Log Schema (`data/processed/null_value_audit_log.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `audit_id` | String | Unique audit event identifier |
| `record_id` | String | Identifier of affected part or vehicle |
| `attribute_name` | String | Field where data was missing (e.g., `price_usd`, `nhtsa_defects`) |
| `missing_category` | String | `STRUCTURAL_CATALOG_GAP`, `GEOGRAPHIC_BOUNDARY_UNAVAILABLE`, `PROPRIETARY_RETAINED` |
| `imputation_applied` | Boolean | Must always be `False` (zero imputation policy) |
| `analyst_impact_note` | String | How this missingness is handled in the scoring engine (uncertainty penalty) |
