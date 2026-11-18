"""
Unit tests for the Multi-Criteria Decision Analysis (MCDA) Scoring Engine.
Verifies mathematical bounds, weight integrity, and ranking calculations.
"""

import pytest
import pandas as pd
from src.config import BASELINE_SCORING_WEIGHTS, SCENARIO_WEIGHTS if "SCENARIO_WEIGHTS" in locals() else {}
from src.scoring_engine import (
    min_max_scale,
    compute_demand_wear_subscore,
    compute_market_scarcity_subscore,
    compute_compatibility_subscore,
    compute_sourcing_practicality_subscore,
    compute_evidence_confidence_subscore,
    calculate_composite_score,
)
from src.sensitivity import SCENARIO_WEIGHTS, calculate_top_n_stability


def test_baseline_weights_sum_to_one():
    assert abs(sum(BASELINE_SCORING_WEIGHTS.values()) - 1.0) < 1e-6


def test_scenario_weights_sum_to_one():
    for sc_name, sc_weights in SCENARIO_WEIGHTS.items():
        assert abs(sum(sc_weights.values()) - 1.0) < 1e-6, f"{sc_name} weights do not sum to 1.0"


def test_min_max_scale_bounds():
    assert min_max_scale(50, 0, 100) == 50.0
    assert min_max_scale(-10, 0, 100) == 0.0
    assert min_max_scale(150, 0, 100) == 100.0
    assert min_max_scale(20, 0, 100, invert=True) == 80.0


def test_subscore_bounds():
    s1 = compute_demand_wear_subscore("CAT-01-BRKPAD", nhtsa_defect_signals=5)
    assert 0.0 <= s1 <= 100.0
    
    s2 = compute_market_scarcity_subscore("Unavailable")
    assert 0.0 <= s2 <= 100.0
    
    s3 = compute_compatibility_subscore("Platform_Shared", trims_covered=2)
    assert 0.0 <= s3 <= 100.0
    
    s4 = compute_sourcing_practicality_subscore("CAT-01-BRKPAD", price_usd=45.0)
    assert 0.0 <= s4 <= 100.0
    
    s5 = compute_evidence_confidence_subscore(source_count=2, has_oem_part_number=True, has_verified_price=True)
    assert 0.0 <= s5 <= 100.0


def test_calculate_composite_score_bounds():
    dummy_row = {
        "category_id": "CAT-01-BRKPAD",
        "clean_oem_part_number": "BYD1029384A",
        "price_usd_standardized": 45.0,
        "availability_flag": "Lead_Time_Required",
        "fitment_scope": "Platform_Shared",
        "nhtsa_defect_signals": 1,
        "source_verification_count": 2,
    }
    
    res = calculate_composite_score(dummy_row)
    assert "composite_priority_score" in res
    assert 0.0 <= res["composite_priority_score"] <= 100.0
