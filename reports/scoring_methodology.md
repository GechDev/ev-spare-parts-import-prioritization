# Prioritization Scoring Methodology (`reports/scoring_methodology.md`)

**Assignment Requirement:** Slide 9 & 11 (25% Rubric Weight — "Create and justify your own scoring formula. You must show how each factor becomes a number, why each weight was chosen, and whether changing the weights changes the ranking.")

---

## 1. Mathematical Formulation of the MCDA Model

To transform fragmented online evidence into a defensible prioritization without black-box assumptions, we implement a **Multi-Criteria Decision Analysis (MCDA)** linear additive model.

For each candidate part $i$, the composite priority score $S_i \in [0, 100]$ is computed as:

$$S_i = \sum_{k=1}^{5} w_k \cdot s_{ik}$$

Subject to:
$$\sum_{k=1}^{5} w_k = 1.0, \quad w_k > 0, \quad s_{ik} \in [0, 100]$$

Where:
* $w_k$: Weight assigned to decision criterion $k$.
* $s_{ik}$: Normalized subscore for part $i$ under criterion $k$.

---

## 2. Approved Decision Criteria & Weight Allocation

The approved **Primary Baseline Model** utilizes the following factor weights:

| Factor | Criterion Name | Weight ($w_k$) | Core Metric / Transformation Base |
| :--- | :--- | :---: | :--- |
| **F1** | **Demand Evidence** | **0.25 (25%)** | Empirical maintenance intervals (wear velocity) + NHTSA safety defect signal bonus. |
| **F2** | **International Procurement Delay** | **0.25 (25%)** | Local aftermarket stockout severity and overseas supplier lead times. |
| **F3** | **Vehicle Compatibility** | **0.20 (20%)** | Cross-model and modular platform interchangeability (e.g., VW MEB, Toyota e-TNGA). |
| **F4** | **Sourcing Practicality** | **0.20 (20%)** | Unit acquisition cost affordability (60%) and freight density / compactness (40%). |
| **F5** | **Evidence Confidence** | **0.10 (10%)** | Dual-source catalog verification count + transparent price & OEM fitment presence. |

---

## 3. Subscore Transformations & Scaling Functions

### Criterion 1: Demand Evidence ($s_{i1}$, Weight $w_1 = 0.25$)
* **Definition:** Captures recurring replacement velocity driven by periodic maintenance schedules, road environmental degradation, and documented safety defects.
* **Economic Rationale:** High-velocity wear items generate rapid inventory turnover, minimizing capital tie-up for an early-stage importer.
* **Mathematical Function:**
  $$s_{i1} = \min\left(100.0, \, \text{BaseWear}(c_i) + \min(10.0, \, 2.0 \times \text{DefectSignals}_i)\right)$$
  Where $\text{BaseWear}(c_i)$ reflects wear velocity: Cabin Filters = 90, Wiper Blades = 85, Brake Pads = 80, Brake Discs = 65, Shock Absorbers = 60, Side Mirrors = 50, Bumpers/Fenders = 40.

### Criterion 2: International Procurement Delay ($s_{i2}$, Weight $w_2 = 0.25$)
* **Definition:** Measures local stockout vulnerability and the lead-time penalty incurred if vehicle owners must source parts individually from abroad.
* **Economic Rationale:** Components with high international delay represent urgent local market demand, enabling premium margins.
* **Scoring Rules:**
  * Acute local stockout (foreign supplier required, 4–8 week transit): $s_{i2} = 95.0$ to $100.0$
  * Moderate lead time (standard distributor channel): $s_{i2} = 75.0$
  * Readily available locally: $s_{i2} = 40.0$

### Criterion 3: Vehicle Compatibility ($s_{i3}$, Weight $w_3 = 0.20$)
* **Definition:** Evaluates modular platform sharing (e.g., VW MEB platform sharing across ID.3/ID.4/ID.6/Audi Q4; BYD e-Platform 3.0 sharing across Dolphin/Atto 3) and trim coverage.
* **Economic Rationale:** Parts compatible across multiple models dramatically reduce dead-inventory obsolescence risk.
* **Scoring Rules:**
  * `Universal` fitment profile: $s_{i3} = 100.0$
  * `Platform_Shared` profile: $s_{i3} = 85.0$
  * `Model_Specific` profile: $s_{i3} = 50.0$

### Criterion 4: Sourcing Practicality ($s_{i4}$, Weight $w_4 = 0.20$)
* **Definition:** Evaluates unit procurement affordability (preserving pilot cash flow) and freight compactness (minimizing air/sea container costs).
* **Economic Rationale:** Bulky, heavy body parts (bumpers, fenders) incur disproportionate freight costs, whereas compact consumables maximize container utilization.
* **Mathematical Function:**
  $$s_{i4} = 0.6 \times (100.0 - \text{BulkFactor}_i) + 0.4 \times \text{AffordabilityScore}(\text{PriceUSD}_i)$$
  If price is unlisted (missing data), a documented penalty is applied to enforce zero fabrication.

### Criterion 5: Evidence Confidence ($s_{i5}$, Weight $w_5 = 0.10$)
* **Definition:** Evaluates empirical verification depth across independent supplier catalogs and databases.
* **Reconciled Rule (Stage 5C):**
  * Fully dual-source verified with explicit price & OEM fitment: $s_{i5} = 4.00$ (normalized to 80.00/100).
  * Single-source unpriced records: penalized to $s_{i5} = 3.00$ (normalized to 60.00/100).

---

## 4. Tie-Handling and Ranking Determinism

When composite scores are identical:
1. Primary sort: Composite priority score (descending).
2. First tie-breaker: Demand Evidence score (F1, descending).
3. Second tie-breaker: Sourcing Practicality score (F4, descending).
4. Stable alphabetical sort by SKU ID to ensure 100% deterministic reproducibility.
