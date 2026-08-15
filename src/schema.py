from __future__ import annotations

import pandas as pd

from .config import COLUMN_ALIASES, REQUIRED_COLUMNS
from .utils import normalize_column_name


def map_column_alias(normalized_name: str) -> str:
    """Map a normalized column name to the canonical schema name."""
    return COLUMN_ALIASES.get(normalized_name, normalized_name)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe column names and avoid duplicate column collisions."""
    normalized = df.copy()
    new_columns: list[str] = []
    seen: dict[str, int] = {}

    for column in normalized.columns:
        base = map_column_alias(normalize_column_name(column))

        if base in seen:
            seen[base] += 1
            base = f"{base}_{seen[base]}"
        else:
            seen[base] = 1

        new_columns.append(base)

    normalized.columns = new_columns
    return normalized


def get_missing_required_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns missing from the dataframe."""
    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def derive_sales_if_possible(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Create a sales column from quantity * unit_price when possible."""
    result = df.copy()

    if "sales" in result.columns:
        return result, 0

    if "quantity" in result.columns and "unit_price" in result.columns:
        quantity = pd.to_numeric(result["quantity"], errors="coerce")
        unit_price = pd.to_numeric(result["unit_price"], errors="coerce")
        sales = quantity * unit_price
        calculated = int(sales.notna().sum())
        result["sales"] = sales
        return result, calculated

    return result, 0