"""
Data Cleaning, Normalization, and Null-Auditing Module.
Implements FAPI-inspired string normalization, exchange rate standardization,
and explicit zero-imputation audit logging.
"""

import re
from typing import Optional
import pandas as pd
from .config import EXCHANGE_RATES_TO_USD


def normalize_part_number(part_number: Optional[str]) -> str:
    """
    Normalizes automotive part numbers following FAPI `ns` field standards.
    Strips whitespace, hyphens, slashes, periods, and standardizes to uppercase.

    Examples:
        'BYD-1029384-A' -> 'BYD1029384A'
        ' 04465-42200 ' -> '0446542200'
        None -> 'UNAVAILABLE'
    """
    if part_number is None or pd.isna(part_number):
        return "UNAVAILABLE"
    
    clean_str = str(part_number).strip().upper()
    if clean_str in ["", "NAN", "NONE", "NULL", "UNAVAILABLE", "N/A"]:
        return "UNAVAILABLE"
    
    # Strip non-alphanumeric characters
    normalized = re.sub(r"[^A-Z0-9]", "", clean_str)
    return normalized if normalized else "UNAVAILABLE"


def convert_to_usd(amount: Optional[float], currency_code: Optional[str]) -> Optional[float]:
    """
    Converts catalog point observation prices to standardized USD.
    Returns None if price is missing (zero imputation rule).
    """
    if amount is None or pd.isna(amount):
        return None
    
    try:
        numeric_amt = float(amount)
    except (ValueError, TypeError):
        return None
    
    if currency_code is None or pd.isna(currency_code):
        return None
        
    code = str(currency_code).strip().upper()
    rate = EXCHANGE_RATES_TO_USD.get(code)
    if rate is None:
        raise ValueError(f"Unsupported currency code '{code}'. Update EXCHANGE_RATES_TO_USD in config.")
        
    return round(numeric_amt * rate, 2)


def generate_null_audit_log(df: pd.DataFrame, record_id_col: str, critical_cols: list[str]) -> pd.DataFrame:
    """
    Generates a formal audit log of unverified or missing data points.
    Enforces the zero-fabrication mandate by documenting gaps rather than filling them.
    """
    audit_records = []
    
    for idx, row in df.iterrows():
        rec_id = row.get(record_id_col, f"ROW_{idx}")
        for col in critical_cols:
            val = row.get(col)
            if pd.isna(val) or val in [None, "", "UNAVAILABLE", "NULL"]:
                # Categorize the nature of the missingness
                if "nhtsa" in col.lower():
                    cat = "GEOGRAPHIC_BOUNDARY_UNAVAILABLE"
                    impact = "NHTSA US defect records not applicable; confidence penalized."
                elif "price" in col.lower():
                    cat = "STRUCTURAL_CATALOG_GAP"
                    impact = "Public catalog price unlisted; sourcing score penalized."
                elif "aftermarket" in col.lower():
                    cat = "STRUCTURAL_CATALOG_GAP"
                    impact = "No verified aftermarket equivalent; OEM only assumed."
                else:
                    cat = "STRUCTURAL_CATALOG_GAP"
                    impact = "Field unverified in public sources."
                    
                audit_records.append({
                    "audit_id": f"AUDIT_{len(audit_records) + 1:04d}",
                    "record_id": str(rec_id),
                    "attribute_name": col,
                    "missing_category": cat,
                    "imputation_applied": False,
                    "analyst_impact_note": impact,
                })
                
    return pd.DataFrame(audit_records)
