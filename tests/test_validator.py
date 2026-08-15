from __future__ import annotations

import pandas as pd

from src.validator import validate_dataframe


def test_missing_required_columns(sample_df) -> None:
    df = sample_df.drop(columns=["order_id"])
    result = validate_dataframe(df)

    assert not result.is_valid
    assert any("order_id" in error for error in result.errors)


def test_duplicate_rows(sample_df) -> None:
    df = pd.concat([sample_df, sample_df.iloc[[0]]], ignore_index=True)
    result = validate_dataframe(df)

    assert result.is_valid
    assert any("duplicate" in warning.lower() for warning in result.warnings)


def test_missing_values(sample_df) -> None:
    df = sample_df.copy()
    df.loc[0, "quantity"] = None
    result = validate_dataframe(df)

    assert result.is_valid
    assert any("missing" in warning.lower() for warning in result.warnings)


def test_invalid_numeric_values(sample_df) -> None:
    df = sample_df.copy()
    df.loc[0, "quantity"] = "abc"
    result = validate_dataframe(df)

    assert result.is_valid
    assert any("numeric" in warning.lower() for warning in result.warnings)


def test_invalid_dates(sample_df) -> None:
    df = sample_df.copy()
    df.loc[0, "order_date"] = "not-a-date"
    result = validate_dataframe(df)

    assert result.is_valid
    assert any("date" in warning.lower() for warning in result.warnings)


def test_invalid_sales_mismatch(sample_df) -> None:
    df = sample_df.copy()
    df.loc[0, "sales"] = 999.0
    result = validate_dataframe(df)

    assert result.is_valid
    assert any("sales" in warning.lower() for warning in result.warnings)