"""
[CANONICAL / AUTHORITATIVE SENSITIVITY PIPELINE]
Multi-Criteria Decision Analysis (MCDA) Sensitivity Analysis Module.
Stage 5C / Stage 6 Audited Implementation.
Authoritative source for results/rankings/sensitivity_analysis.csv and sensitivity_comparison.png.

Scenarios Evaluated:
1. Baseline (Approved Primary): 25/25/20/20/10
2. Demand-Focused: 40/20/15/15/10 (Prioritizes wear lifecycle and operational failure risk)
3. Evidence-Confidence-Focused: 20/20/20/15/25 (Prioritizes catalog verification rigor & FX risk)
4. Sourcing-Practicality-Focused: 20/20/20/30/10 (Prioritizes unit cost & packaging compactness)
"""

import os
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

# 1. Scenario Weights Definitions
SENSITIVITY_SCENARIOS: Dict[str, Dict[str, float]] = {
    "Baseline": {
        "demand_evidence": 0.25,
        "international_procurement_delay": 0.25,
        "vehicle_compatibility": 0.20,
        "sourcing_practicality": 0.20,
        "evidence_confidence": 0.10,
    },
    "Demand_Focused": {
        "demand_evidence": 0.40,
        "international_procurement_delay": 0.20,
        "vehicle_compatibility": 0.15,
        "sourcing_practicality": 0.15,
        "evidence_confidence": 0.10,
    },
    "Evidence_Focused": {
        "demand_evidence": 0.20,
        "international_procurement_delay": 0.20,
        "vehicle_compatibility": 0.20,
        "sourcing_practicality": 0.15,
        "evidence_confidence": 0.25,
    },
    "Sourcing_Focused": {
        "demand_evidence": 0.20,
        "international_procurement_delay": 0.20,
        "vehicle_compatibility": 0.20,
        "sourcing_practicality": 0.30,
        "evidence_confidence": 0.10,
    },
}

# Verify weights sum to 1.00
for sc_name, sc_weights in SENSITIVITY_SCENARIOS.items():
    weight_sum = sum(sc_weights.values())
    assert abs(weight_sum - 1.0) < 1e-6, f"Scenario '{sc_name}' weights must sum to 1.00 (got {weight_sum})"


def compute_scenario_score(row: pd.Series, weights: Dict[str, float]) -> float:
    """
    Computes unrounded composite priority score (0 - 100) from percentage subscores:
    CPS = w1*S1 + w2*S2 + w3*S3 + w4*S4 + w5*S5
    """
    s1 = float(row["S1_demand_pct"])
    s2 = float(row["S2_procurement_delay_pct"])
    s3 = float(row["S3_compatibility_pct"])
    s4 = float(row["S4_sourcing_pct"])
    s5 = float(row["S5_confidence_pct"])
    
    return (
        weights["demand_evidence"] * s1
        + weights["international_procurement_delay"] * s2
        + weights["vehicle_compatibility"] * s3
        + weights["sourcing_practicality"] * s4
        + weights["evidence_confidence"] * s5
    )


def assign_competition_ranks(df: pd.DataFrame, score_col: str) -> Tuple[List[str], List[int]]:
    """
    Assigns standard competition ranking ("1224" ranking) with 'T-' prefix for ties.
    Returns (rank_strings, rank_numbers).
    """
    sorted_indices = df.sort_values(by=score_col, ascending=False).index.tolist()
    scores = df.loc[sorted_indices, score_col].tolist()
    
    rank_str_map = {}
    rank_num_map = {}
    
    n = len(sorted_indices)
    i = 0
    while i < n:
        val = scores[i]
        ties = []
        j = i
        while j < n and abs(scores[j] - val) < 0.005:
            ties.append(j)
            j += 1
            
        rank_num = i + 1
        rank_str = f"T-{rank_num}" if len(ties) > 1 else str(rank_num)
        
        for k in ties:
            idx = sorted_indices[k]
            rank_str_map[idx] = rank_str
            rank_num_map[idx] = rank_num
            
        i = j
        
    rank_strs = [rank_str_map[idx] for idx in df.index]
    rank_nums = [rank_num_map[idx] for idx in df.index]
    
    return rank_strs, rank_nums


def run_sensitivity_pipeline(input_csv_path: str, output_csv_path: str) -> pd.DataFrame:
    """
    Runs sensitivity scoring pipeline across all 4 scenarios, calculates competition
    ranks, rank differences, and exports the master sensitivity dataset.
    """
    df = pd.read_csv(input_csv_path)
    
    result_df = df[[
        "record_id", "vehicle_model", "category_id", "part_category",
        "clean_oem_part_number", "price_usd", "operational_criticality",
        "S1_demand_pct", "S2_procurement_delay_pct", "S3_compatibility_pct",
        "S4_sourcing_pct", "S5_confidence_pct"
    ]].copy()
    
    # 1. Compute unrounded scores and competition ranks for each scenario
    for sc_name, sc_weights in SENSITIVITY_SCENARIOS.items():
        raw_col = f"Score_{sc_name}_raw"
        disp_col = f"Score_{sc_name}"
        str_rank_col = f"Rank_{sc_name}_Str"
        num_rank_col = f"Rank_{sc_name}_Num"
        
        result_df[raw_col] = result_df.apply(lambda r: compute_scenario_score(r, sc_weights), axis=1)
        result_df[disp_col] = result_df[raw_col].round(2)
        
        r_strs, r_nums = assign_competition_ranks(result_df, raw_col)
        result_df[str_rank_col] = r_strs
        result_df[num_rank_col] = r_nums
        
    # 2. Compute rank differences relative to Baseline
    for sc_name in ["Demand_Focused", "Evidence_Focused", "Sourcing_Focused"]:
        diff_col = f"Rank_Shift_{sc_name}"
        # Positive shift means improved rank (e.g. from 6 to 4 is +2)
        result_df[diff_col] = result_df["Rank_Baseline_Num"] - result_df[f"Rank_{sc_name}_Num"]
        
    # Sort by Baseline score descending
    result_df = result_df.sort_values(by="Score_Baseline_raw", ascending=False).reset_index(drop=True)
    
    # Export
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    result_df.to_csv(output_csv_path, index=False)
    
    return result_df


def compute_top_n_overlap_summary(df: pd.DataFrame, top_n: int = 5) -> Dict[str, Any]:
    """
    Computes top-N retention, displacement, new appearances, and overlap percentages
    relative to Baseline.
    """
    baseline_top = df[df["Rank_Baseline_Num"] <= top_n]
    baseline_ids = set(baseline_top["record_id"])
    
    summary = {}
    for sc_name in SENSITIVITY_SCENARIOS.keys():
        sc_top = df[df[f"Rank_{sc_name}_Num"] <= top_n]
        sc_ids = set(sc_top["record_id"])
        
        retained = list(baseline_ids.intersection(sc_ids))
        displaced = list(baseline_ids - sc_ids)
        new_items = list(sc_ids - baseline_ids)
        overlap_pct = round((len(retained) / len(baseline_ids)) * 100.0, 1)
        
        summary[sc_name] = {
            "total_top_skus": len(sc_ids),
            "retained_from_baseline": retained,
            "displaced_from_baseline": displaced,
            "newly_appearing": new_items,
            "overlap_pct_vs_baseline": overlap_pct,
        }
        
    return summary


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_path = os.path.join(repo_root, "results", "rankings", "full_ranking.csv")
    out_path = os.path.join(repo_root, "results", "rankings", "sensitivity_analysis.csv")
    
    df_res = run_sensitivity_pipeline(in_path, out_path)
    print(f"[SUCCESS] Exported sensitivity_analysis.csv ({len(df_res)} rows)")
    
    overlap = compute_top_n_overlap_summary(df_res, top_n=5)
    for sc, data in overlap.items():
        print(f"Scenario '{sc}': Overlap = {data['overlap_pct_vs_baseline']}% | Total Top SKUs = {data['total_top_skus']}")
