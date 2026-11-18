# 7-Minute Individual Presentation Script & Timing Guide

**Target Presentation Length:** 7 minutes (420 seconds) followed by Evaluator Q&A.  
**Tone:** Evidence-based, strategic, academically rigorous, defensible.  
**Approved Baseline Model Weights:** Demand Evidence (25%), International Procurement Delay (25%), Vehicle Compatibility (20%), Sourcing Practicality (20%), Evidence Confidence (10%).

---

### [Minute 0:00 – 1:00] Slide 1: The Importer's Dilemma & Problem Framing
* **Visual Exhibit:** Importer balance sheet graphic comparing high inventory holding costs against customer stockout penalties; map of Ethiopia / Addis Ababa EV transition.
* **Speaker Script:**
  > "Good morning. Imagine you are an automotive spare-parts importer entering Ethiopia’s rapidly electrifying market. Following the government’s 2024 ban on internal combustion vehicle imports, tens of thousands of electric vehicles are entering Addis Ababa. However, official dealership parts support is virtually non-existent.
  >
  > As an independent importer, you face a critical dilemma: you cannot stock every replacement part for every model with limited pilot working capital ($5,000 to $10,000). If you buy expensive, slow-moving body panels, your capital is trapped in dead inventory. If you understock routine maintenance items, vehicle owners face prolonged downtime and you lose customer trust.
  >
  > The purpose of this project is not to guess demand, but to turn fragmented, public online data into a defensible, reproducible, and explainable prioritization of the five highest-priority candidate parts for an initial pilot import."

---

### [Minute 1:00 – 2:00] Slide 2: Target Vehicle Selection & Visibility Proxies
* **Visual Exhibit:** Candidate vehicle comparison matrix showing BYD Seagull, Toyota bZ4X, and VW ID.4 alongside explicit marketplace proxy disclaimer banner.
* **Speaker Script:**
  > "Our first decision was selecting three target vehicles from the candidate pool. We selected the **BYD Seagull**, the **Toyota bZ4X**, and the **Volkswagen ID.4**.
  >
  > These three models cover distinct, vital market segments: the Seagull on BYD's e-Platform 3.0 is the premier high-volume urban commuter in Addis Ababa; the bZ4X carries Toyota’s dominant brand equity in East Africa on the e-TNGA architecture; and the ID.4 represents the surging parallel-import family crossover built on VW’s modular MEB platform.
  >
  > I must emphasize a critical methodological boundary: in our analysis, marketplace listings from Adey Market and distributor entries on Gezat Electric are treated strictly as proxies for commercial visibility and dealer intent. We do not, and must not, present listing counts as vehicle registrations or sales numbers."

---

### [Minute 2:00 – 3:15] Slide 3: The 10 Parts & Evidence Architecture
* **Visual Exhibit:** Schema diagram showing the 10 assigned categories grouped into Fast-Moving Wear, Maintenance, Lighting, Collision, and Suspension; FAPI string normalization exhibit; Null-Audit table snippet.
* **Speaker Script:**
  > "Our second and third decisions were investigating all ten assigned part categories across these three vehicles—totaling 30 SKUs—and building a traceable dataset.
  >
  > We gathered evidence from primary supplier catalogs including Landin Parts, CQSW, Toyota Parts, and Exist.ae, cross-checking fitment across multiple sources wherever possible. To ensure data integrity, we adapted key architectural concepts from our reference repositories: first, we implemented FAPI's alphanumeric string normalization, stripping punctuation so that part numbers from Chinese suppliers match reliably against international catalogs.
  >
  > Second, we enforced a strict zero-fabrication policy: if a price or fitment was unavailable online, we never imputed or guessed it. We preserved it as unavailable and recorded it in a dedicated Null-Audit Log, penalizing the part's evidence confidence rather than creating fake data."

---

### [Minute 3:15 – 4:30] Slide 4: Explainable Multi-Criteria Scoring Model
* **Visual Exhibit:** 5-pillar MCDA formula, bounded $[0, 100]$ scaling equations, and pie chart of approved baseline scoring weights (25/25/20/20/10).
* **Speaker Script:**
  > "For our fourth decision, we designed an explainable Multi-Criteria Decision Analysis model that translates evidence into numbers without black-box assumptions.
  >
  > Every part receives a score from 0 to 100 across five weighted dimensions:
  > - **25% for Demand Evidence (F1):** Prioritizing documented routine wear schedules, environmental degradation, and safety defect signals.
  > - **25% for International Procurement Delay (F2):** Capturing supplier lead-time risk and acute local stockout vulnerability.
  > - **20% for Vehicle Compatibility (F3):** Rewarding parts shared across multiple trims or platform siblings, such as VW’s MEB platform.
  > - **20% for Sourcing Practicality (F4):** Favoring affordable unit costs and compact freight dimensions over bulky body panels.
  > - **10% for Evidence Confidence (F5):** Rewarding dual-source catalog verification and complete price/OEM fitment transparency.
  >
  > This weighting directly reflects supply chain inventory theory: high-turnover consumables protect an early-stage importer's operating cash flow."

---

### [Minute 4:30 – 5:30] Slide 5: Top 5 Provisional Recommendations & Sensitivity Stability
* **Visual Exhibit:** Bar chart of the Top 5 parts with composite scores; sensitivity rank stability heatmap across the 4 alternative weighting scenarios.
* **Speaker Script:**
  > "Executing our scoring model yields our fifth decision: the five highest-priority replacement parts for pilot importation.
  >
  > Under the approved baseline model, the top five individual recommendations are:
  > 1. **BYD Seagull Cabin-Air Filter (Score 81.14, Rank T-1)**
  > 2. **Toyota bZ4X Cabin-Air Filter (Score 81.14, Rank T-1)**
  > 3. **Volkswagen ID.4 Cabin-Air Filter (Score 81.14, Rank T-1)**
  > 4. **Toyota bZ4X Front Wiper Blade Set (Score 77.56, Rank T-4)**
  > 5. **Volkswagen ID.4 Front Aero Wiper Blade Set (Score 77.56, Rank T-4)**
  > *(Front Brake Pads rank T-6 at 77.40, trailing wipers by only 0.16 points; BYD Seagull wipers rank 9th at 73.56 due to model-specific fitment).*
  >
  > Crucially, we satisfied the assignment’s sensitivity testing mandate across four strategic scenarios: Baseline, Demand-Focused, Evidence-Confidence-Focused, and Sourcing-Practicality-Focused. Across all scenarios, cabin filters demonstrate perfect rank resilience (Rank T-1 in all four). In the Demand-Focused scenario, Front Brake Pads surge to 81.08 (Rank T-4), displacing wiper blades and confirming a robust 'Core 8' inventory cluster. Our recommendations are mathematically robust and not an artifact of arbitrary weight tuning."

---

### [Minute 5:30 – 6:30] Slide 6: Evidence Limitations & Unverified Parameters
* **Visual Exhibit:** Audit table highlighting proxy limitations, NHTSA geographic mismatch, single-source price point caveats, and catalog structural gaps.
* **Speaker Script:**
  > "A truly defensible analysis must be honest about what it does not know. Finding information is unavailable is a valid and crucial result.
  >
  > We explicitly disclose our Materiality Hierarchy of limitations:
  > 1. **Absence of Ethiopian Vehicle Registration Census:** Marketplace listings show dealer intent, not on-road fleet density.
  > 2. **Wholesale Landed Cost Gaps:** Catalog prices exclude container ocean shipping, Djibouti corridor port fees, and Ethiopian customs tariffs.
  > 3. **Single-Supplier Price Points:** Several SKUs rely on a single catalog quote.
  > 4. **Geographic Asymmetry in Defect Data:** NHTSA complaints cover US-sold VW and Toyota models, but Chinese domestic EVs like the BYD Seagull lack US NHTSA coverage.
  > 5. **Year and Trim Fitment Variances:** MEB and e-TNGA configurations differ between European and Chinese production batches.
  >
  > For these reasons, our recommendation is, and must remain, strictly provisional."

---

### [Minute 6:30 – 7:00] Slide 7: Operational Roadmap & Low-Risk Execution
* **Visual Exhibit:** 3-phase execution roadmap: Phase 1 ($5k–$10k pilot batch), Phase 2 (mechanic field interviews), Phase 3 (commercial scale-up) alongside the 11-point Pre-Purchase Verification Checklist.
* **Speaker Script:**
  > "To turn this provisional recommendation into commercial reality, we propose a low-risk, three-step execution roadmap backed by an 11-point Pre-Purchase Verification Checklist:
  >
  > First, the client should allocate an initial pilot tranche of only **$5,000 to $10,000** focused strictly on high-turnover consumables—cabin filters and wiper blade sets, with optional brake pad sample units.
  >
  > Second, while this pilot order is in transit, the importer must conduct field interviews with Addis Ababa EV repair shops and verify physical fitment against operating VINs.
  >
  > Third, only after the pilot batch turns over within 60 days should commercial container capital be committed.
  >
  > Thank you. I welcome your questions."

---

### Anticipated Evaluator Q&A Defense (Quick Reference)

* **Q: Why didn't you pick the Changan Benben E-Star?**  
  * *Defense:* "The BYD Seagull demonstrated superior parts catalog traceability in English/international public databases (via Landin and CQSW), whereas Changan catalog data is fragmented, increasing supply chain procurement risk."
* **Q: Why are Cabin-Air Filters ranked #1 above Brake Pads in the Baseline model?**  
  * *Defense:* "Under the Baseline weights (25/25/20/20/10), Cabin Filters achieve 81.14 (Rank T-1) because they combine high wear frequency (F1: 5.0) with low unit cost ($8.50–$25.84) and ultra-compact packaging (F4: 4.91). Front Brake Pads score 77.40 (Rank T-6), trailing wipers (77.56, Rank T-4) by a mere 0.16 points due to higher unit acquisition cost ($42.00–$78.50) and heavier freight bulk. However, under the Demand-Focused scenario (40% demand weight), Brake Pads surge to 81.08 (Rank T-4), displacing wipers, which is why we highlight both in our Core 8 cluster."
* **Q: Why didn't you use FAPI's cross-reference data for Ethiopian demand?**  
  * *Defense:* "FAPI sample data is an evaluation schema and not market demand. FAPI data contains European/US combustion car parts. Using it for Ethiopian EV demand would be data fabrication. We reused FAPI's data schema and string normalization algorithms, not its market conclusions."
* **Q: What if the client wants to import headlights instead of cabin filters?**  
  * *Defense:* "Headlights are Class A-Z items in inventory theory: high unit cost ($350–$620), high freight bulk, and highly volatile collision demand. Committing scarce pilot capital ($5,000–$10,000) to headlights would tie up working capital in 8–15 units with prolonged turnover cycles."
