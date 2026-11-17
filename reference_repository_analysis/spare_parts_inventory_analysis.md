# Architectural Audit: Spare Parts Inventory System

**Source Repository:** `c:\Users\Administrator\Desktop\icog\SparePartsInventory`  
**Upstream GitHub:** `https://github.com/vivasvana1/SparePartsInventory`  
**Inspected Date:** 2026-11-18

---

## 1. Architectural Overview & System Purpose

The **Spare Parts Inventory** repository is an enterprise-grade solution tackling intermittent-demand forecasting, multi-echelon inventory optimization, and simulation under supply chain uncertainty.

### Key Components Inspected:
* `notebooks/01_data_preparation.ipynb` & `02_data_preparation.ipynb`: Pipeline hygiene, outlier detection, and feature engineering.
* `notebooks/03_exploratory_data_analysis.ipynb`: Demand distribution analysis, ABC-XYZ inventory classification matrices, and volatility clustering.
* `notebooks/04_demand_forecasting.ipynb`: Intermittent demand algorithms tailored for lumpy spare-part consumption (Croston's Method, Syntetos-Boylan Approximation [SBA], Teunter-Syntetos-Babai [TSB]).
* `notebooks/05_inventory_optimization.ipynb`: Safety stock, reorder point (ROP), economic order quantity (EOQ), and service-level trade-off modeling.
* `Optimization_models_CPLEX/`: Mixed-integer linear programming (MILP) models (.mod/.dat) for warehouse capacity and multi-echelon inventory allocation.
* `Power-BI Dashboards/`: Executive KPI dashboards tracking fill rates, ROI indices, lead-time variance, and forecast accuracy.

---

## 2. Theoretical Principles & Supply Chain Heuristics

### 2.1 The ABC-XYZ Inventory Matrix
The repository utilizes a dual-axis classification matrix:
* **ABC Classification (Value / Capital Commitment):**
  * `Class A`: High-value parts (top 70–80% of inventory value, typically 10–20% of SKU count).
  * `Class B`: Moderate-value parts (15–20% of inventory value).
  * `Class C`: Low-value parts (5–10% of inventory value, but 50–70% of SKU count).
* **XYZ Classification (Demand Volatility & Predictability):**
  * `Class X`: Stable, continuous, highly predictable consumption (coefficient of variation $CV < 0.5$).
  * `Class Y`: Variable demand with cyclical or seasonal patterns ($0.5 \le CV \le 1.0$).
  * `Class Z`: Highly erratic, intermittent, lumpy demand ($CV > 1.0$).

### 2.2 Relevance to EV Spare-Parts Prioritization
Applying the ABC-XYZ lens to our 10 assigned EV part categories provides clear strategic rationale:
* **Consumables (Brake pads, cabin filters, wipers):** Classify as **C-X or B-X** (relatively low unit cost, high turnover, steady wear-driven demand). These are ideal initial import candidates because they generate immediate cash flow with minimal capital lockup.
* **Collision / Structural Components (Bumpers, headlights, fenders):** Classify as **A-Z** (high capital cost, bulky shipping volume, unpredictable collision-dependent demand). Stocking these without confirmed buyer commitments creates dangerous dead-capital exposure.

---

## 3. Specific Elements to Reuse, Modify, or Reject

### A. Elements to Reuse (Adopt)
* **ABC-XYZ Prioritization Logic:** We adapt the ABC-XYZ theoretical principles to defend our multi-criteria scoring weights. Prioritizing high-turnover consumables over bulky collision panels aligns directly with commercial inventory optimization theory.
* **Trade-Off Modeling Principles:** The logic balancing stockout costs (vehicle downtime) against holding costs (working capital lockup) directly supports our business-problem justification.
* **Visualization & KPI Presentation:** We adopt clean dashboard layouts (metric cards, heatmaps, and ranking bar charts) for our 7-minute slide deck.

### B. Elements to Modify (Adapt)
* **Simplified Scoring Engine:** While `SparePartsInventory` employs heavyweight IBM ILOG CPLEX optimization solvers and discrete-event AnyLogistix simulations, our assignment requires an explainable, lightweight Multi-Criteria Decision Analysis (MCDA) framework implemented in pure Python/Pandas.

### C. Elements to Reject (Do Not Use)
* **Historical Demand & Transaction Datasets:**  
  * *Reason:* The daily transaction logs and demand time series in `SparePartsInventory` represent synthetic or industrial enterprise data. They have zero empirical validity for the Ethiopian EV vehicle fleet. Using them to simulate demand curves for a BYD Seagull or Changan Benben would violate the assignment's anti-fabrication mandate and receive zero marks.
* **Heavyweight CPLEX/AnyLogistix Infrastructure:** Proprietary software packages requiring commercial licenses are excluded to preserve complete reproducibility on open-source Python tooling.
