"""
[PROTOTYPE / REFERENCE IMPLEMENTATION]
Multi-Criteria Decision Analysis (MCDA) Scoring Engine.

NOTE: This is the prototype MCDA scoring module with 0-100 min-max scaling.
      The CANONICAL and AUTHORITATIVE scoring pipeline that produced all final CSVs
      (results/rankings/full_ranking.csv, final_top_five.csv, factor_scores.csv)
      is `src/scoring.py` (which implements the Stage 5C audited 5-factor model).
      Retained for reference and legacy test compatibility.
"""

from typing import Dict, Any, Optional
import pandas as pd
from .config import BASELINE_SCORING_WEIGHTS, ASSIGNED_PART_CATEGORIES


def min_max_scale(val: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """Bounded min-max scaler returning values strictly in [0.0, 100.0]."""
    if max_val == min_val:
        return 50.0
    scaled = ((val - min_val) / (max_val - min_val)) * 100.0
    scaled = max(0.0, min(100.0, scaled))
    return 100.0 - scaled if invert else scaled


def compute_demand_wear_subscore(
    category_id: str,
    nhtsa_defect_signals: int = 0
) -> float:
    """
    Subscore 1: Demand & Wear Velocity Signal [0 - 100].
    Based on mechanical wear frequency and documented defect/complaint signals.
    Fast-moving wear items (pads, filters, wipers) score higher than static body panels.
    """
    cat_meta = ASSIGNED_PART_CATEGORIES.get(category_id, {})
    base_wear = cat_meta.get("wear_velocity_rating", 50.0)
    
    # Defect adjustment (up to +10 points if documented failure signals exist)
    defect_bonus = min(10.0, nhtsa_defect_signals * 2.0)
    return min(100.0, base_wear + defect_bonus)


def compute_market_scarcity_subscore(
    availability_flag: str,
    local_distributor_coverage: str = "Poor"
) -> float:
    """
    Subscore 2: Market Scarcity & Lead Time Risk [0 - 100].
    Measures the difficulty and lead time for vehicle owners to obtain the part locally.
    High scarcity / backorders = higher priority to import.
    """
    status_weights = {
        "Unavailable": 95.0,        # Severe local stockout / no catalog inventory
        "Lead_Time_Required": 75.0, # 4-8 weeks international transit
        "In_Stock": 40.0,           # Readily available
    }
    return status_weights.get(availability_flag, 60.0)


def compute_compatibility_subscore(
    fitment_scope: str,
    trims_covered: int = 1
) -> float:
    """
    Subscore 3: Vehicle Compatibility & Platform Sharing [0 - 100].
    Components fitting across multiple models, trims, or platform siblings
    (e.g., VW MEB platform or Toyota e-TNGA) carry lower inventory risk.
    """
    scope_scores = {
        "Universal": 100.0,         # Standardized wiper blades, cabin filter profiles
        "Platform_Shared": 85.0,    # Fits multiple MEB or e-Platform 3.0 models
        "Model_Specific": 50.0,     # Exclusive to one vehicle model
    }
    base = scope_scores.get(fitment_scope, 50.0)
    trim_bonus = min(15.0, (trims_covered - 1) * 5.0)
    return min(100.0, base + trim_bonus)


def compute_sourcing_practicality_subscore(
    category_id: str,
    price_usd: Optional[float]
) -> float:
    """
    Subscore 4: Sourcing Practicality & Capital Efficiency [0 - 100].
    Prioritizes parts with affordable unit purchase price (lower working capital lockup)
    and high shipping compactness (low freight volume).
    """
    cat_meta = ASSIGNED_PART_CATEGORIES.get(category_id, {})
    bulk_penalty = cat_meta.get("bulk_factor", 50.0)  # 0 (compact) to 100 (bulky bumper)
    bulk_score = 100.0 - bulk_penalty
    
    # Capital cost score (cheaper parts score higher for initial importer tranches)
    if price_usd is None or pd.isna(price_usd):
        cost_score = 40.0  # Penalty for unverified pricing
    else:
        # Scale between $10 (inexpensive) and $500 (expensive)
        cost_score = min_max_scale(price_usd, min_val=10.0, max_val=500.0, invert=True)
        
    return 0.6 * bulk_score + 0.4 * cost_score


def compute_evidence_confidence_subscore(
    source_count: int,
    has_oem_part_number: bool,
    has_verified_price: bool
) -> float:
    """
    Subscore 5: Evidence Confidence & Verification Count [0 - 100].
    Adapted from FAPI `r`-rating. Multi-source verified parts score higher.
    Unverified or missing data points receive explicit penalties.
    """
    score = 0.0
    # Source cross-referencing count (up to 40 points)
    score += min(40.0, source_count * 20.0)
    
    # OEM Part Number verification (30 points)
    if has_oem_part_number:
        score += 30.0
        
    # Verified catalog pricing (30 points)
    if has_verified_price:
        score += 30.0
        
    return min(100.0, score)


def calculate_composite_score(
    row: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Calculates all 5 subscores and the composite priority score for a single part record.
    Composite Score = sum(w_k * s_ik)
    """
    if weights is None:
        weights = BASELINE_SCORING_WEIGHTS
        
    # Verify weight normalization
    assert abs(sum(weights.values()) - 1.0) < 1e-6, "Weights must sum to 1.0"
    
    cat_id = row.get("category_id", "")
    price = row.get("price_usd_standardized")
    avail = row.get("availability_flag", "Lead_Time_Required")
    fitment = row.get("fitment_scope", "Model_Specific")
    defects = int(row.get("nhtsa_defect_signals", 0) or 0)
    sources = int(row.get("source_verification_count", 1) or 1)
    has_oem = str(row.get("clean_oem_part_number", "")).upper() not in ["", "UNAVAILABLE", "NONE"]
    has_price = price is not None and not pd.isna(price)
    
    s1 = compute_demand_wear_subscore(cat_id, defects)
    s2 = compute_market_scarcity_subscore(avail)
    s3 = compute_compatibility_subscore(fitment)
    s4 = compute_sourcing_practicality_subscore(cat_id, price)
    s5 = compute_evidence_confidence_subscore(sources, has_oem, has_price)
    
    composite = (
        weights["demand_wear_signal"] * s1
        + weights["market_scarcity"] * s2
        + weights["vehicle_compatibility"] * s3
        + weights["sourcing_practicality"] * s4
        + weights["evidence_confidence"] * s5
    )
    
    return {
        "subscore_demand_wear": round(s1, 2),
        "subscore_market_scarcity": round(s2, 2),
        "subscore_compatibility": round(s3, 2),
        "subscore_sourcing_practicality": round(s4, 2),
        "subscore_evidence_confidence": round(s5, 2),
        "composite_priority_score": round(composite, 2),
    }


def rank_parts_dataset(
    df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Applies the scoring engine to a master dataset and returns ranked records.
    """
    results = []
    for _, row in df.iterrows():
        scores = calculate_composite_score(row.to_dict(), weights)
        merged = {**row.to_dict(), **scores}
        results.append(merged)
        
    ranked_df = pd.DataFrame(results)
    ranked_df = ranked_df.sort_values(by="composite_priority_score", ascending=False).reset_index(drop=True)
    ranked_df["rank"] = ranked_df.index + 1
    return ranked_df
