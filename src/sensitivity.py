"""
[PROTOTYPE / REFERENCE IMPLEMENTATION]
Sensitivity and Scenario Analysis Module.

NOTE: This is the prototype sensitivity analysis module paired with `src/scoring_engine.py`.
      The CANONICAL and AUTHORITATIVE sensitivity pipeline that generated
      `results/rankings/sensitivity_analysis.csv` and powers `04_sensitivity_analysis.ipynb`
      is `src/sensitivity_analysis.py` (which implements the Stage 5C 4-scenario framework).
      Retained for reference and legacy test compatibility.
"""

from typing import Dict, List
import pandas as pd
from .scoring_engine import rank_parts_dataset
from .config import BASELINE_SCORING_WEIGHTS

# Alternative Strategic Weighting Scenarios
SCENARIO_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Baseline": BASELINE_SCORING_WEIGHTS,
    "Wear_Aggressive": {
        "demand_wear_signal": 0.45,
        "market_scarcity": 0.20,
        "vehicle_compatibility": 0.15,
        "sourcing_practicality": 0.10,
        "evidence_confidence": 0.10,
    },
    "Capital_Preserving": {
        "demand_wear_signal": 0.15,
        "market_scarcity": 0.20,
        "vehicle_compatibility": 0.15,
        "sourcing_practicality": 0.40,  # Prioritize cheap, compact parts to protect cash flow
        "evidence_confidence": 0.10,
    },
    "Compatibility_Focused": {
        "demand_wear_signal": 0.20,
        "market_scarcity": 0.15,
        "vehicle_compatibility": 0.40,  # Prioritize parts shared across platforms
        "sourcing_practicality": 0.15,
        "evidence_confidence": 0.10,
    },
    "Scarcity_Constrained": {
        "demand_wear_signal": 0.20,
        "market_scarcity": 0.45,        # Prioritize parts facing severe local stockouts
        "vehicle_compatibility": 0.15,
        "sourcing_practicality": 0.10,
        "evidence_confidence": 0.10,
    },
}

# Verify all scenarios sum to 1.0
for sc_name, sc_weights in SCENARIO_WEIGHTS.items():
    assert abs(sum(sc_weights.values()) - 1.0) < 1e-6, f"Scenario '{sc_name}' weights must sum to 1.0"


def evaluate_scenario_rankings(
    df: pd.DataFrame,
    scenarios: Dict[str, Dict[str, float]] = SCENARIO_WEIGHTS
) -> pd.DataFrame:
    """
    Runs the scoring engine across all specified scenarios and aggregates
    part ranks into a single comparison DataFrame.
    """
    if df.empty:
        return pd.DataFrame()
        
    master_ranks = pd.DataFrame()
    
    for sc_name, sc_weights in scenarios.items():
        ranked = rank_parts_dataset(df, sc_weights)
        sc_cols = ranked[["part_id", "category_name", "rank", "composite_priority_score"]].copy()
        sc_cols = sc_cols.rename(columns={
            "rank": f"rank_{sc_name}",
            "composite_priority_score": f"score_{sc_name}"
        })
        
        if master_ranks.empty:
            master_ranks = sc_cols
        else:
            master_ranks = master_ranks.merge(sc_cols, on=["part_id", "category_name"], how="left")
            
    return master_ranks


def calculate_top_n_stability(
    scenario_matrix: pd.DataFrame,
    baseline_col: str = "rank_Baseline",
    top_n: int = 5
) -> float:
    """
    Calculates the proportion of baseline Top-N parts that remain in the Top-N
    across all alternative scenarios.
    Returns stability index between 0.0 (unstable) and 1.0 (highly robust).
    """
    if scenario_matrix.empty or baseline_col not in scenario_matrix.columns:
        return 0.0
        
    baseline_top_n = set(scenario_matrix[scenario_matrix[baseline_col] <= top_n]["part_id"])
    rank_cols = [c for c in scenario_matrix.columns if c.startswith("rank_") and c != baseline_col]
    
    if not rank_cols:
        return 1.0
        
    overlaps = []
    for col in rank_cols:
        sc_top_n = set(scenario_matrix[scenario_matrix[col] <= top_n]["part_id"])
        overlap = len(baseline_top_n.intersection(sc_top_n)) / top_n
        overlaps.append(overlap)
        
    return round(sum(overlaps) / len(overlaps), 3)
