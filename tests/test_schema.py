from __future__ import annotations

import pandas as pd

from src.schema import get_missing_required_columns, normalize_columns


def test_column_normalization() -> None:
    df = pd.DataFrame(
        {
            "Order ID": [1],
            "OrderDate": ["2024-01-01"],
            "Product": ["x"],
            "Category": ["y"],
            "Region": ["z"],
            "Qty": [1],
            "Unit Price": [10.0],
        }
    )

    normalized = normalize_columns(df)

    assert "order_id" in normalized.columns
    assert "order_date" in normalized.columns
    assert "product" in normalized.columns
    assert "category" in normalized.columns
    assert "region" in normalized.columns
    assert "quantity" in normalized.columns
    assert "unit_price" in normalized.columns


def test_missing_required_columns() -> None:
    df = pd.DataFrame({"foo": [1]})
    missing = get_missing_required_columns(df)

    assert "order_id" in missing
    assert "order_date" in missing