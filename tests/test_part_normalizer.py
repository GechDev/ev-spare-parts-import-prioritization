"""
Unit tests for part number normalization and currency conversion logic.
Verifies compliance with FAPI `ns` string cleaning and zero-imputation rules.
"""

import pytest
from src.data_cleaning import normalize_part_number, convert_to_usd


def test_normalize_part_number_standard():
    assert normalize_part_number("BYD-1029384-A") == "BYD1029384A"
    assert normalize_part_number(" 04465-42200 ") == "0446542200"
    assert normalize_part_number("1EA.698.151.A") == "1EA698151A"


def test_normalize_part_number_missing_and_nulls():
    assert normalize_part_number(None) == "UNAVAILABLE"
    assert normalize_part_number("") == "UNAVAILABLE"
    assert normalize_part_number("   ") == "UNAVAILABLE"
    assert normalize_part_number("NAN") == "UNAVAILABLE"
    assert normalize_part_number("NULL") == "UNAVAILABLE"
    assert normalize_part_number("N/A") == "UNAVAILABLE"


def test_convert_to_usd_valid():
    assert convert_to_usd(100.0, "USD") == 100.0
    assert convert_to_usd(100.0, "CNY") == 13.80
    assert convert_to_usd(100.0, "AED") == 27.20
    assert convert_to_usd(100.0, "EUR") == 108.50


def test_convert_to_usd_missing_or_invalid():
    assert convert_to_usd(None, "USD") is None
    assert convert_to_usd(100.0, None) is None
    assert convert_to_usd("invalid", "USD") is None


def test_convert_to_usd_unsupported_currency():
    with pytest.raises(ValueError):
        convert_to_usd(100.0, "UNKNOWN_CURRENCY")
