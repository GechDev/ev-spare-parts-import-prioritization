"""
Unit tests for data schema integrity and null-audit tracking.
Ensures zero-fabrication compliance and proper column typing.
"""

import pytest
import pandas as pd
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.data_cleaning import generate_null_audit_log


def test_raw_vehicle_visibility_template_headers():
    path = RAW_DATA_DIR / "vehicle_visibility_raw.csv"
    assert path.exists()
    df = pd.read_csv(path)
    expected_cols = ["vehicle_id", "make", "model", "source_portal", "source_url", "collection_date"]
    for col in expected_cols:
        assert col in df.columns


def test_processed_master_dataset_template_headers():
    path = PROCESSED_DATA_DIR / "ev_parts_master_dataset.csv"
    assert path.exists()
    df = pd.read_csv(path)
    expected_cols = [
        "part_id",
        "vehicle_id",
        "category_id",
        "clean_oem_part_number",
        "price_usd_standardized",
        "source_verification_count",
    ]
    for col in expected_cols:
        assert col in df.columns


def test_null_audit_log_zero_imputation():
    dummy_df = pd.DataFrame([
        {
            "record_id": "TEST_001",
            "clean_oem_part_number": "UNAVAILABLE",
            "price_usd_standardized": None,
            "nhtsa_defect_signals": "NULL",
        }
    ])
    
    audit_df = generate_null_audit_log(
        dummy_df,
        record_id_col="record_id",
        critical_cols=["clean_oem_part_number", "price_usd_standardized", "nhtsa_defect_signals"]
    )
    
    assert len(audit_df) == 3
    # Verify that imputation is NEVER applied
    assert (audit_df["imputation_applied"] == False).all()
