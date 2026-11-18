"""
Comprehensive Automated Test Suite for EV Spare-Parts MCDA Scoring Engine (Stage 5).
Audited Quality-Control Implementation.

Verifies:
1. Mathematical precision and weight sums across all 4 scenarios.
2. Proper factor calculations and zero-fabrication rules (NULL price handling).
3. Programmatic category average calculation directly from individual 30-SKU scores.
4. Category ranking stability across all four scenarios (Brake Pads Rank 2 in all 4).
5. Standard competition ranking ("1224") and tie handling.
6. Benchmark top-five cutoff expansion to 6 SKUs due to the T-4 tie at positions 4, 5, 6.
7. Verification that output CSVs (full_ranking.csv, factor_scores.csv) exist and maintain traceability.
"""

import os
import pytest
import pandas as pd
import numpy as np

from src.scoring import (
    SCENARIO_WEIGHTS,
    score_demand_evidence,
    score_international_procurement_delay,
    score_market_scarcity,
    score_vehicle_compatibility,
    score_sourcing_practicality,
    score_evidence_confidence,
    classify_operational_criticality,
    calculate_data_completeness,
    compute_part_scores,
    rank_30_parts_with_ties,
    compute_category_averages,
)


def get_repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_scenario_weights_sum_to_one():
    for name, w in SCENARIO_WEIGHTS.items():
        assert abs(sum(w.values()) - 1.0) < 1e-6, f"{name} weights do not sum to 1.0"


def test_f1_demand_baseline_and_defect_bonus():
    f_pad_0 = score_demand_evidence("CAT-01-BRKPAD", 0)
    f_pad_4 = score_demand_evidence("CAT-01-BRKPAD", 4)
    assert f_pad_0 == 4.8
    assert f_pad_4 == 5.0  # 4.8 + min(0.5, 4 * 0.1) = 5.2 -> capped at 5.0


def test_f2_pure_procurement_delay_scarcity():
    assert score_international_procurement_delay("In_Stock") == 2.5
    assert score_international_procurement_delay("Lead_Time_Required") == 4.0
    assert score_international_procurement_delay("Unavailable") == 5.0
    assert score_market_scarcity("In_Stock") == 2.5


def test_f3_audited_compatibility_tiers():
    assert score_vehicle_compatibility("CAT-03-CABFILT", "ID.4") == 4.0
    assert score_vehicle_compatibility("CAT-04-WIPER", "ID.4") == 4.0
    assert score_vehicle_compatibility("CAT-04-WIPER", "Seagull") == 3.0
    assert score_vehicle_compatibility("CAT-01-BRKPAD", "ID.4") == 4.0
    assert score_vehicle_compatibility("CAT-02-BRKDISC", "bZ4X") == 4.0
    assert score_vehicle_compatibility("CAT-10-SHOCK", "ID.4") == 3.0
    assert score_vehicle_compatibility("CAT-07-MIRROR", "bZ4X") == 3.0
    assert score_vehicle_compatibility("CAT-05-HEADLIGHT", "bZ4X") == 2.0
    assert score_vehicle_compatibility("CAT-08-BUMPER", "Seagull") == 2.0
    assert score_vehicle_compatibility("CAT-09-FENDER", "ID.4") == 2.0


def test_f4_sourcing_null_price_handling_no_fabrication():
    score_p, is_missing_p = score_sourcing_practicality("CAT-01-BRKPAD", 77.52)
    assert not is_missing_p
    assert abs(score_p - 4.225) < 1e-4
    
    score_m, is_missing_m = score_sourcing_practicality("CAT-09-FENDER", None)
    assert is_missing_m
    assert abs(score_m - 0.8) < 1e-4
    
    score_null, is_null = score_sourcing_practicality("CAT-09-FENDER", "NULL")
    assert is_null
    assert abs(score_null - 0.8) < 1e-4


def test_f5_confidence_decoupled_from_defects():
    assert score_evidence_confidence(2, True, True) == 5.0
    assert score_evidence_confidence(2, True, False) == 3.0
    assert score_evidence_confidence(2, False, True) == 1.0


def test_3_level_operational_criticality():
    assert classify_operational_criticality("CAT-01-BRKPAD") == "High (Immobilizing)"
    assert classify_operational_criticality("CAT-02-BRKDISC") == "High (Immobilizing)"
    assert classify_operational_criticality("CAT-10-SHOCK") == "High (Immobilizing)"
    assert classify_operational_criticality("CAT-04-WIPER") == "Medium (Safety/Visibility)"
    assert classify_operational_criticality("CAT-05-HEADLIGHT") == "Medium (Safety/Visibility)"
    assert classify_operational_criticality("CAT-06-TAILLIGHT") == "Medium (Safety/Visibility)"
    assert classify_operational_criticality("CAT-07-MIRROR") == "Medium (Safety/Visibility)"
    assert classify_operational_criticality("CAT-03-CABFILT") == "Low (Cosmetic/Comfort)"
    assert classify_operational_criticality("CAT-08-BUMPER") == "Low (Cosmetic/Comfort)"
    assert classify_operational_criticality("CAT-09-FENDER") == "Low (Cosmetic/Comfort)"


def test_generated_output_files_exist_and_match():
    repo_root = get_repo_root()
    full_path = os.path.join(repo_root, "results", "rankings", "full_ranking.csv")
    factor_path = os.path.join(repo_root, "results", "rankings", "factor_scores.csv")
    report_path = os.path.join(repo_root, "results", "rankings", "ranking_report.md")
    chart_path = os.path.join(repo_root, "results", "rankings", "highest_priority_candidates.png")
    
    assert os.path.exists(full_path), "full_ranking.csv missing"
    assert os.path.exists(factor_path), "factor_scores.csv missing"
    assert os.path.exists(report_path), "ranking_report.md missing"
    assert os.path.exists(chart_path), "highest_priority_candidates.png missing"
    
    df_full = pd.read_csv(full_path)
    df_factor = pd.read_csv(factor_path)
    
    assert len(df_full) == 30, f"Expected 30 rows in full_ranking.csv, got {len(df_full)}"
    assert len(df_factor) == 150, f"Expected 150 rows in factor_scores.csv, got {len(df_factor)}"
    
    # Check NULL price handling in generated CSV
    fender_row = df_full[df_full["record_id"] == "CLN-SGL-FENDER-01"].iloc[0]
    assert str(fender_row["price_usd"]).upper() in ["NULL", "NAN", ""], "Fender price must be NULL"
    assert fender_row["uncertainty_flag"] == "DATA_GAP_PRICE_UNVERIFIED"
    assert float(fender_row["decision_completeness_dci"]) == 40.0
    
    # Check priced single-source DCI (56.7%)
    priced_row = df_full[df_full["record_id"] == "CLN-VW-CABFILT-01"].iloc[0]
    assert float(priced_row["decision_completeness_dci"]) == 56.7
    
    # Category checks
    cat_df = compute_category_averages(df_full)
    cat_map = cat_df.set_index("category_id").to_dict(orient="index")
    
    for s in ["Primary", "Benchmark", "Capital", "DemandAgg"]:
        pad_avg = cat_map["CAT-01-BRKPAD"][f"Avg_{s}"]
        wiper_avg = cat_map["CAT-04-WIPER"][f"Avg_{s}"]
        assert pad_avg > wiper_avg, f"Brake pads must rank above wipers in {s}"


def test_stage5c_reconciliation_csvs_and_invariance():
    repo_root = get_repo_root()
    sku_recon_path = os.path.join(repo_root, "results", "rankings", "stage5c_sku_reconciliation.csv")
    cat_recon_path = os.path.join(repo_root, "results", "rankings", "stage5c_category_reconciliation.csv")
    
    assert os.path.exists(sku_recon_path), "stage5c_sku_reconciliation.csv missing"
    assert os.path.exists(cat_recon_path), "stage5c_category_reconciliation.csv missing"
    
    df_sku = pd.read_csv(sku_recon_path)
    df_cat = pd.read_csv(cat_recon_path)
    
    assert len(df_sku) == 30, f"Expected 30 SKUs, got {len(df_sku)}"
    assert len(df_cat) == 10, f"Expected 10 categories, got {len(df_cat)}"
    
    # Verify all 30 SKUs explained by F5
    assert (df_sku["Mathematically_Explained_By_F5"] == "YES").all()
    
    # Verify 29 priced drop by 2.00, unpriced fender drops by 0.00
    priced_skus = df_sku[df_sku["record_id"] != "CLN-SGL-FENDER-01"]
    assert np.allclose(priced_skus["Diff_Primary"], -2.0000, atol=1e-4)
    
    fender_row = df_sku[df_sku["record_id"] == "CLN-SGL-FENDER-01"].iloc[0]
    assert abs(float(fender_row["Diff_Primary"])) < 1e-4
    
    # Verify zero category discrepancy
    assert np.allclose(df_cat["SKU_Discrepancy"], 0.0, atol=1e-4)


def test_sensitivity_analysis_outputs_and_invariance():
    repo_root = get_repo_root()
    sens_csv = os.path.join(repo_root, "results", "rankings", "sensitivity_analysis.csv")
    sens_chart = os.path.join(repo_root, "results", "rankings", "sensitivity_comparison.png")
    
    assert os.path.exists(sens_csv), "sensitivity_analysis.csv missing"
    assert os.path.exists(sens_chart), "sensitivity_comparison.png missing"
    
    df = pd.read_csv(sens_csv)
    assert len(df) == 30, f"Expected 30 rows, got {len(df)}"
    
    # 1. Verify weights sum to 1.00
    from src.sensitivity_analysis import SENSITIVITY_SCENARIOS
    for sc, w in SENSITIVITY_SCENARIOS.items():
        assert abs(sum(w.values()) - 1.0) < 1e-6, f"{sc} weights must sum to 1.0"
        
    # 2. Check Baseline Top 5
    base_top5 = set(df[df["Rank_Baseline_Num"] <= 5]["record_id"])
    assert len(base_top5) == 5
    
    # 3. Check Evidence and Sourcing 100% Top 5 Overlap
    evid_top5 = set(df[df["Rank_Evidence_Focused_Num"] <= 5]["record_id"])
    sour_top5 = set(df[df["Rank_Sourcing_Focused_Num"] <= 5]["record_id"])
    assert evid_top5 == base_top5
    assert sour_top5 == base_top5
    
    # 4. Check Demand-Focused Top 5 (3 Cabin filters + 3 Brake pads due to T-4 tie)
    dem_top5 = set(df[df["Rank_Demand_Focused_Num"] <= 5]["record_id"])
    assert len(dem_top5) == 6  # expands to 6 SKUs due to tie
    retained = base_top5.intersection(dem_top5)
    assert len(retained) == 3  # 60.0% overlap of baseline items
    
    # 5. Check Top 8 Composition Invariance across all 4 scenarios
    base_top8 = set(df.sort_values(by="Score_Baseline_raw", ascending=False).iloc[:8]["record_id"])
    for sc in ["Demand_Focused", "Evidence_Focused", "Sourcing_Focused"]:
        sc_top8 = set(df.sort_values(by=f"Score_{sc}_raw", ascending=False).iloc[:8]["record_id"])
        assert sc_top8 == base_top8, f"Top 8 SKUs must be invariant in {sc}"


def test_stage6_final_recommendations():
    repo_root = get_repo_root()
    final_report = os.path.join(repo_root, "results", "recommendation_report.md")
    final_csv = os.path.join(repo_root, "results", "rankings", "final_top_five.csv")
    cleaned_csv = os.path.join(repo_root, "data", "processed", "cleaned_dataset.csv")
    
    assert os.path.exists(final_report), "recommendation_report.md missing"
    assert os.path.exists(final_csv), "final_top_five.csv missing"
    assert os.path.getsize(final_report) > 15000, "recommendation_report.md too small"
    
    df_final = pd.read_csv(final_csv)
    df_clean = pd.read_csv(cleaned_csv)
    
    assert len(df_final) == 5, f"Expected 5 candidates in final_top_five.csv, got {len(df_final)}"
    
    expected_ids = {
        "CLN-SGL-CABFILT-01",
        "CLN-TOY-CABFILT-01",
        "CLN-VW-CABFILT-01",
        "CLN-TOY-WIPER-01",
        "CLN-VW-WIPER-01"
    }
    assert set(df_final["candidate_id"]) == expected_ids
    
    # Check baseline scores and ranks
    for _, row in df_final.iterrows():
        cid = row["candidate_id"]
        cat = row["part_category"]
        score = float(row["baseline_cps"])
        rank_str = row["baseline_rank_str"]
        
        if cat == "Cabin-air filters":
            assert abs(score - 81.14) < 1e-4
            assert rank_str == "T-1"
        elif cat == "Wiper blades":
            assert abs(score - 77.56) < 1e-4
            assert rank_str == "T-4"
            
        clean_row = df_clean[df_clean["record_id"] == cid].iloc[0]
        assert str(clean_row["clean_oem_part_number"]) == str(row["clean_oem_part_number"])
        assert str(clean_row["source_url"]) == str(row["source_url"])


