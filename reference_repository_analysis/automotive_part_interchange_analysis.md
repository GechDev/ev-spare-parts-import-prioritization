# Architectural Audit: Automotive Part Interchange Database

**Source Repository:** `c:\Users\Administrator\Desktop\icog\automotive-part-interchange-database`  
**Upstream GitHub:** `https://github.com/3r1nC/automotive-part-interchange-database`  
**Inspected Date:** 2026-11-18

---

## 1. Architectural Overview & System Purpose

The **Automotive Part Interchange Database** is a functional prototype demonstrating how original equipment (OE), original equipment manufacturer (OEM), and aftermarket automotive parts can be cross-referenced across diverse vehicle applications.

### Key Components Inspected:
* `database/schema.sql`: Relational schema defining four core entities.
* `src/search_parts.py`: SQL search routines using SQLite parameterized queries and pattern matching.
* `src/import_data.py`: Batch data loading routines converting CSVs into relational SQLite tables.
* `src/app.py`: Streamlit-based web user interface featuring KPI metric cards, vehicle search dropdowns, and interchange tables.
* `data/`: Sample CSV files (`sample_vehicles.csv`, `sample_parts.csv`, `sample_cross_reference.csv`, `sample_fitment.csv`).

---

## 2. Schema Decomposition

The SQLite relational schema (`schema.sql`) implements a clean 4-tier normalized structure:

```sql
CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY,
    year INTEGER,
    make TEXT,
    model TEXT,
    engine TEXT,
    fuel_type TEXT
);

CREATE TABLE parts (
    part_id INTEGER PRIMARY KEY,
    part_type TEXT,
    oe_part_number TEXT,
    oem_brand TEXT,
    description TEXT
);

CREATE TABLE cross_references (
    cross_ref_id INTEGER PRIMARY KEY,
    part_id INTEGER,
    brand TEXT,
    part_number TEXT,
    FOREIGN KEY (part_id) REFERENCES parts(part_id)
);

CREATE TABLE fitment (
    fitment_id INTEGER PRIMARY KEY,
    part_id INTEGER,
    vehicle_id INTEGER,
    fitment_type TEXT,
    FOREIGN KEY (part_id) REFERENCES parts(part_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);
```

### Key Relational Strengths:
1. **Decoupling of Parts and Vehicles:** The many-to-many relationship between parts and vehicles is cleanly resolved through the `fitment` junction table. This is critical for our EV prioritization because parts (such as cabin filters or brake pads) often fit across multiple vehicle trims, model years, or platform siblings.
2. **First-Class Cross-Referencing:** The `cross_references` table allows a single OE part to associate with multiple aftermarket manufacturer part numbers without denormalizing the primary `parts` entity.

---

## 3. Query Logic Analysis (`src/search_parts.py`)

The search routine executes a multi-table `LEFT JOIN`:

```python
def search_by_part_number(part_number):
    query = """
    SELECT
        p.part_type,
        p.oe_part_number,
        p.oem_brand,
        cr.brand AS interchange_brand,
        cr.part_number AS interchange_part_number,
        v.year,
        v.make,
        v.model,
        v.engine,
        f.fitment_type
    FROM parts p
    LEFT JOIN cross_references cr ON p.part_id = cr.part_id
    LEFT JOIN fitment f ON p.part_id = f.part_id
    LEFT JOIN vehicles v ON f.vehicle_id = v.vehicle_id
    WHERE
        p.oe_part_number LIKE ?
        OR cr.part_number LIKE ?;
    """
    search_value = f"%{part_number}%"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (search_value, search_value))
        return cursor.fetchall()
```

* **Reusability Assessment:** Excellent structure for querying multi-vehicle compatibility. In our analysis, parts that join to multiple candidate vehicle models or trims receive higher vehicle compatibility subscores.

---

## 4. Specific Elements to Reuse, Modify, or Reject

### A. Elements to Reuse (Adopt)
* **The 4-Tier Relational Model:** Adapt this exact conceptual schema into our SQLite/Pandas data pipeline to map candidate EV models (`dim_vehicles`), part categories (`dim_part_categories`), catalog entries (`fact_part_catalog`), and cross-model fitment matrices.
* **SQL Parameterized Query Patterns:** Use secure parameter binding when querying SQLite for multi-model fitments.

### B. Elements to Modify (Adapt)
* **Fuel Type & Engine Fields:** In `vehicles`, replace ICE-specific attributes (`engine`, `fuel_type`) with EV-specific parameters (`battery_capacity_kwh`, `powertrain_type`, `drive_configuration` [FWD/RWD/AWD], `platform_architecture`).
* **Source Tracking & Provenance:** The original schema lacks provenance fields. We will augment the schema with mandatory `source_url`, `collection_date`, and `source_verification_count` columns.

### C. Elements to Reject (Do Not Use)
* **Sample Data Files:** The sample CSVs contain toy records for legacy vehicles (e.g., 2018 Honda Civic, 2015 Ford F-150). They have zero relevance to Ethiopian EV parts import and are completely excluded.
* **Streamlit UI Complexity:** While visually appealing, deploying a full Streamlit application is unnecessary for our core analytical deliverables. We focus on transparent Python modules, Jupyter notebooks, and publication-ready figures.
