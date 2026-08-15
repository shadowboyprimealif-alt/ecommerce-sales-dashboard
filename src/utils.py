from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd


def normalize_column_name(name: Any) -> str:
    """Normalize a column name into a safe snake_case identifier."""
    if name is None:
        return ""

    text = str(name).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^0-9a-zA-Z_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def get_file_extension(filename: str | Path | None) -> str:
    """Return a lowercase file extension, or an empty string."""
    if not filename:
        return ""
    return Path(filename).suffix.lower()


def safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide two numbers safely, returning default on zero division or bad input."""
    try:
        num = float(numerator or 0.0)
        den = float(denominator)
    except (TypeError, ValueError):
        return default

    if den == 0.0:
        return default

    return num / den


def format_currency(value: Any, symbol: str = "$") -> str:
    """Format a value as currency."""
    try:
        return f"{symbol}{float(value):,.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0.00"


def parse_date_series(series: pd.Series) -> pd.Series:
    """Parse a pandas Series into datetime values, coercing errors to NaT."""
    if series is None:
        return pd.Series(dtype="datetime64[ns]")
    return pd.to_datetime(series, errors="coerce")


def date_range(series: pd.Series) -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
    """Return min and max valid dates from a Series."""
    dates = pd.to_datetime(series, errors="coerce").dropna()
    if dates.empty:
        return None, None
    return dates.min(), dates.max()