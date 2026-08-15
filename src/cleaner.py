from __future__ import annotations

import numpy as np
import pandas as pd

from .config import NUMERIC_COLUMNS, TEXT_COLUMNS
from .models import CleaningReport


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningReport]:
    """Clean a normalized sales dataframe and return cleaning statistics."""
    rows_uploaded = len(df)
    cleaned = df.copy()

    empty_before = len(cleaned)
    cleaned = cleaned.dropna(how="all")
    empty_rows_removed = empty_before - len(cleaned)

    duplicate_before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    duplicate_rows_removed = duplicate_before - len(cleaned)

    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip().replace("", pd.NA)

    if "order_date" in cleaned.columns:
        cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    missing_sales_calculated = 0
    if "quantity" in cleaned.columns and "unit_price" in cleaned.columns:
        if "sales" not in cleaned.columns:
            cleaned["sales"] = np.nan

        missing_sales_mask = (
            cleaned["sales"].isna()
            & cleaned["quantity"].notna()
            & cleaned["unit_price"].notna()
        )
        missing_sales_calculated = int(missing_sales_mask.sum())

        cleaned.loc[missing_sales_mask, "sales"] = (
            cleaned.loc[missing_sales_mask, "quantity"]
            * cleaned.loc[missing_sales_mask, "unit_price"]
        )

    invalid_before = len(cleaned)
    invalid_mask = pd.Series(False, index=cleaned.index)

    if "order_id" in cleaned.columns:
        order_id_text = cleaned["order_id"].astype("string").str.strip()
        invalid_mask |= cleaned["order_id"].isna() | order_id_text.eq("").fillna(False)

    if "order_date" in cleaned.columns:
        invalid_mask |= cleaned["order_date"].isna()

    if "quantity" in cleaned.columns:
        invalid_mask |= cleaned["quantity"].isna() | (cleaned["quantity"] < 0)

    if "unit_price" in cleaned.columns:
        invalid_mask |= cleaned["unit_price"].isna() | (cleaned["unit_price"] < 0)

    if "sales" in cleaned.columns:
        invalid_mask |= cleaned["sales"].isna() | (cleaned["sales"] < 0)

    cleaned = cleaned[~invalid_mask]
    invalid_rows_removed = invalid_before - len(cleaned)

    final_rows = len(cleaned)

    report = CleaningReport(
        rows_uploaded=rows_uploaded,
        empty_rows_removed=empty_rows_removed,
        duplicate_rows_removed=duplicate_rows_removed,
        invalid_rows_removed=invalid_rows_removed,
        missing_sales_calculated=missing_sales_calculated,
        final_rows=final_rows,
        messages=[
            f"{rows_uploaded} rows uploaded.",
            f"{empty_rows_removed} completely empty rows removed.",
            f"{duplicate_rows_removed} exact duplicate rows removed.",
            f"{invalid_rows_removed} invalid rows removed.",
            f"{missing_sales_calculated} missing sales values calculated.",
            f"{final_rows} final rows.",
        ],
    )

    return cleaned.reset_index(drop=True), report