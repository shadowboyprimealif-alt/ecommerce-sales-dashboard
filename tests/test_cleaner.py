from __future__ import annotations

import pandas as pd
import pytest

from src.cleaner import clean_dataframe


def test_duplicate_removal(sample_df) -> None:
    df = pd.concat([sample_df, sample_df], ignore_index=True)
    cleaned, report = clean_dataframe(df)

    assert report.duplicate_rows_removed >= len(sample_df)
    assert len(cleaned) == len(sample_df)


def test_numeric_conversion(sample_df) -> None:
    df = sample_df.copy()
    df["quantity"] = df["quantity"].astype(str)

    cleaned, _ = clean_dataframe(df)

    assert pd.api.types.is_numeric_dtype(cleaned["quantity"])


def test_date_conversion(sample_df) -> None:
    cleaned, _ = clean_dataframe(sample_df)

    assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])


def test_missing_sales_calculation(sample_df) -> None:
    df = sample_df.drop(columns=["sales"])
    cleaned, report = clean_dataframe(df)

    assert "sales" in cleaned.columns
    assert report.missing_sales_calculated > 0
    assert cleaned["sales"].sum() == pytest.approx(sample_df["sales"].sum())