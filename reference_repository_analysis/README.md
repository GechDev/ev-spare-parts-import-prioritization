# Reference Repository Analysis & Code Reuse Governance

## 1. Overview & Academic Mandate

As part of the official assignment brief (Slide 12):
* **Allowed Reuse:** Existing code, database schemas, and analytical concepts from the three reference repositories may be reused when formally cited.
* **Explanation Mandate:** The submission must explicitly explain what was reused, modified, or rejected.
* **Integrity Warning:** Unexplained copied work receives zero marks for reasoning and implementation.
* **Target Market Boundary:** *"The repositories provide structure and examples. They do not provide the target-market answer."*

This directory houses dedicated architectural analyses for each of the three reference repositories located in the workspace parent directory.

---

## 2. Analyzed Repositories

| Repository | Source Origin | Core Tech Stack | Primary Relevance to Assignment |
| :--- | :--- | :--- | :--- |
| **`automotive-part-interchange-database`** | [github.com/3r1nC/automotive-part-interchange-database](https://github.com/3r1nC/automotive-part-interchange-database) | Python, SQLite, Pandas, Streamlit | Normalized 4-tier relational schema (`vehicles`, `parts`, `cross_references`, `fitment`) and SQL query search patterns. |
| **`auto-parts-cross-reference`** | [github.com/fapi-dev/auto-parts-cross-reference](https://github.com/fapi-dev/auto-parts-cross-reference) | SQL (MySQL/PG), Tabular text | Production-grade part number string normalization (`ns` logic), OE vs. aftermarket classification (`tp`), and multi-source confirmation rating (`r`). |
| **`SparePartsInventory`** | [github.com/vivasvana1/SparePartsInventory](https://github.com/vivasvana1/SparePartsInventory) | Python, CPLEX, AnyLogistix, Power BI | ABC-XYZ inventory classification heuristics, holding cost vs. stockout penalty trade-offs, and visual KPI design. |

---

## 3. Strict Boundary: What CANNOT Be Reused as Market Demand

To ensure academic and professional defensibility:
1. **FAPI Sample Cross-References:** Cannot be treated as replacement frequency or local fleet demand. FAPI data contains legacy internal combustion engine (ICE) parts for European and North American vehicles.
2. **`SparePartsInventory` Transaction History:** Cannot be cited as real-world EV maintenance frequencies in Addis Ababa. These logs are synthetic or historical enterprise data from heavy machinery/manufacturing fleets.
3. **Streamlit Sample CSVs:** The sample vehicle applications in `automotive-part-interchange-database` are toy examples for UI testing, not EV fitment data.

See the dedicated markdown files in this directory for detailed technical audits of each repository.
