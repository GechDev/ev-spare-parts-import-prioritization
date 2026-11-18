# Citation, Attribution & Code Reuse Log (`reports/citation_and_reuse_log.md`)

**Assignment Requirement:** Slide 12 ("Existing code may be reused when cited. Explain what you reused, changed or rejected. Unexplained copied work receives no reasoning or implementation marks.")  
**Full Implementation Justification Report:** [`reports/reuse_and_implementation_justification_report.md`](file:///c:/Users/Administrator/Desktop/icog/ev-spare-parts-import-prioritization/reports/reuse_and_implementation_justification_report.md)

---

## 1. Summary of Code & Concept Reuse

| Repository Cited | Author / Upstream Origin | Elements Adopted (Reused) | Elements Modified (Adapted) | Elements Rejected (Excluded) |
| :--- | :--- | :--- | :--- | :--- |
| **`automotive-part-interchange-database`** | `github.com/3r1nC/automotive-part-interchange-database` | 4-tier relational schema (`vehicles`, `parts`, `cross_references`, `fitment`) and SQL query search patterns. | Replaced ICE fields (engine, fuel) with EV attributes (battery kWh, platform). Added explicit source URL and retrieval timestamp tracking. | Rejected Streamlit web UI complexity and toy sample data CSVs (legacy combustion cars). |
| **`auto-parts-cross-reference`** | `github.com/fapi-dev/auto-parts-cross-reference` | Part number string normalizer algorithm (`ns` logic), OE vs. aftermarket typology (`tp` flag), and multi-source confirmation rating ($r$). | Adapted normalization from SQL schema to modular Python function (`src/data_cleaning.py`). | **Rejected all 22,550 sample cross-reference rows.** (Mandated by Slide 12 notes: FAPI data is not target-market demand). |
| **`SparePartsInventory`** | `github.com/vivasvana1/SparePartsInventory` | ABC-XYZ inventory classification theory and holding cost vs. stockout penalty trade-off logic. | Simplified complex CPLEX MILP optimization and AnyLogistix simulations into a lightweight, explainable MCDA model. | **Rejected all historical transaction logs and synthetic demand series.** (Cannot be treated as Ethiopian EV demand). |

---

## 2. Detailed Technical Governance

### 2.1 Reused from `automotive-part-interchange-database`
* **Adopted:** We adopted the relational database layout in our schema design. Separating parts from vehicle applications via a junction `fitment` table allows our system to capture platform-shared parts across multiple vehicle trims.
* **Modified:** We added mandatory data provenance columns (`source_name`, `source_url`, `collection_date`, `source_verification_count`) to ensure every row is traceable.
* **Rejected:** We omitted the Streamlit UI and local sample data files because our deliverables focus on reproducible Python pipelines, Jupyter notebooks, and publication-ready figures.

### 2.2 Reused from `auto-parts-cross-reference` (FAPI)
* **Adopted:** We adopted the FAPI alphanumeric normalization rule:
  $$\text{CleanPartNo} = \text{RegExReplace}(\text{RawPartNo}, \, [\wedge A\text{-}Z0\text{-}9], \, \text{""})$$
  This standardizes part numbers across Chinese supplier catalogs (CQSW, Landin) and global databases.
* **Modified:** We embedded this logic directly into `src/data_cleaning.py::normalize_part_number()`.
* **Rejected:** In strict accordance with Slide 12 notes (*"FAPI sample data is for evaluation and is not market-demand evidence"*), none of the 22,550 cross-reference links or part numbers from the sample text files were ingested as demand evidence.

### 2.3 Reused from `SparePartsInventory`
* **Adopted:** We adopted the theoretical framework of ABC-XYZ inventory management. This framework explains why low-cost, high-velocity consumables (brake pads, filters, wipers) outrank expensive, sporadic collision components (bumpers, headlights) for a capital-constrained importer.
* **Modified:** We distilled the inventory trade-offs into our explainable 5-pillar Multi-Criteria Decision Analysis (MCDA) model.
* **Rejected:** All synthetic demand logs, AnyLogistix simulation tables, and IBM CPLEX files were excluded to prevent data fabrication and ensure 100% open-source Python reproducibility.
