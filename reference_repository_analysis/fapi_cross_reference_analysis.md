# Architectural Audit: FAPI Auto Parts Cross-Reference

**Source Repository:** `c:\Users\Administrator\Desktop\icog\auto-parts-cross-reference`  
**Upstream GitHub:** `https://github.com/fapi-dev/auto-parts-cross-reference`  
**Inspected Date:** 2026-11-18

---

## 1. Architectural Overview & System Purpose

The **FAPI Auto Parts Cross-Reference** repository contains a production-grade sample of the commercial FAPI cross-reference database. In automotive commerce, a cross-reference represents an equivalence link between two part numbers (OE vs. aftermarket or aftermarket vs. aftermarket) certified as interchangeable direct replacements.

### Key Components Inspected:
* `scheme.sql`: Unified SQL schema supporting MySQL, MariaDB, and PostgreSQL.
* `manufacturer_list.txt`: 1,506 records of automotive brands and parts manufacturers.
* `product_list.txt`: 13,869 part number records with normalized search representations.
* `analog_list.txt`: 22,550 bidirectional cross-reference link records with evidence ratings.

---

## 2. Schema Decomposition (`scheme.sql`)

```sql
CREATE TABLE manufacturer_list (
    i integer NOT NULL,
    ds character varying(255) NOT NULL,
    da character varying(255) NOT NULL
);

CREATE TABLE product_list (
    i bigint NOT NULL,
    mfi integer NOT NULL,
    ns character varying(105) NOT NULL,
    n character varying(255),
    d character varying(255),
    tp integer NOT NULL,
    upd bigint DEFAULT 0 NOT NULL
);

CREATE TABLE analog_list (
    i bigint NOT NULL,
    mfi integer NOT NULL,
    ns character varying(105) NOT NULL,
    pi bigint NOT NULL,
    pai bigint NOT NULL,
    r integer NOT NULL
);
```

### High-Value Industrial Concepts Discovered:
1. **The `ns` (Normalized String) Attribute:**  
   In `product_list` and `analog_list`, `ns` represents an alphanumeric-only representation of the part number. Characters like hyphens (`-`), spaces (` `), slashes (`/`), and dots (`.`) are stripped, and letters are standardized to uppercase.
   * *Example:* `BYD-1029384-A` $\rightarrow$ `BYD1029384A`.
   * *Value for Our Project:* Online catalogs for Chinese EVs (e.g., CQSW vs. Landin) frequently format the same OEM part number with differing hyphens or spacing. Applying this normalization eliminates false-negative search matches.
2. **The `tp` (Type Code) Attribute:**  
   `tp = 1` denotes Original Equipment (OE), while `tp = 2` denotes Aftermarket replacement. This distinction is vital for an importer evaluating profit margins and sourcing availability.
3. **The `r` (Evidence Rating) Attribute:**  
   In `analog_list`, `r` counts the number of independent sources confirming a cross-reference less those disputing it. In our multi-criteria scoring model, this translates directly to the `Evidence Confidence` metric.

---

## 3. Specific Elements to Reuse, Modify, or Reject

### A. Elements to Reuse (Adopt)
* **Part Number Normalization Logic:** We adopt FAPI's `ns` algorithm directly into `src/data_cleaning.py` (`normalize_part_number()`) to sanitize all extracted part numbers.
* **OE vs. Aftermarket Typology:** We adopt the `tp` concept to categorize parts and assess whether cheaper aftermarket alternatives exist for candidate EVs.
* **Evidence Confidence Rating ($r$):** We adopt the rating logic: parts confirmed across multiple independent catalogs receive higher confidence subscores than single-catalog entries.

### B. Elements to Modify (Adapt)
* **Flat File Structure to Pandas/SQLite:** Rather than loading massive delimiter-separated text files into a standalone MySQL/Postgres server, we implement this schema in lightweight SQLite and Pandas within Python for full portability.

### C. Elements to Reject (Do Not Use)
* **The 22,550 Sample Cross-References:**  
  * *Slide 12 Notes Mandate:* *"FAPI sample data is for evaluation and is not market-demand evidence."*
  * *Reason:* The sample part numbers belong to legacy European and North American combustion cars. Using them to model Ethiopian EV replacement demand would be complete fabrication and is strictly excluded.
