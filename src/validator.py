from __future__ import annotations

import pandas as pd

from .config import NUMERIC_COLUMNS, REQUIRED_COLUMNS
from .models import DataQualityReport, ValidationResult
from .schema import get_missing_required_columns


def validate_dataframe(df: pd.DataFrame) -> ValidationResult:
    """Validate a normalized sales dataframe and return structured results."""
    errors: list[str] = []
    warnings: list[str] = []

    if df is None:
        return ValidationResult(False, ["No data was provided."], [])

    if df.columns.size == 0:
        return ValidationResult(False, ["The file does not contain any recognizable columns."], [])

    missing_columns = get_missing_required_columns(df)
    if missing_columns:
        errors.append(
            f"Your file is missing the required {', '.join(missing_columns)} column(s). "
            "Please check the dataset format and upload again."
        )
        return ValidationResult(False, errors, warnings)

    if df.empty:
        warnings.append("The dataset contains no rows.")

    empty_rows = int(df.isna().all(axis=1).sum())
    if empty_rows:
        warnings.append(f"{empty_rows} completely empty row(s) were found.")

    duplicate_rows = int(df.duplicated().sum())
    if duplicate_rows:
        warnings.append(f"{duplicate_rows} exact duplicate row(s) were found.")

    if "order_id" in df.columns:
        duplicate_order_ids = int(df["order_id"].dropna().duplicated().sum())
        if duplicate_order_ids:
            warnings.append(f"{duplicate_order_ids} duplicate order_id value(s) were found.")

    required_present = [column for column in REQUIRED_COLUMNS if column in df.columns]
    missing_values = int(df[required_present].isna().sum().sum())
    if missing_values:
        warnings.append(f"{missing_values} missing value(s) were found in required columns.")

    if "order_date" in df.columns:
        parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
        invalid_dates = int((df["order_date"].notna() & parsed_dates.isna()).sum())
        if invalid_dates:
            warnings.append(f"{invalid_dates} invalid or unparseable order_date value(s) were found.")

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            parsed_numbers = pd.to_numeric(df[column], errors="coerce")
            invalid_numbers = int((df[column].notna() & parsed_numbers.isna()).sum())
            if invalid_numbers:
                warnings.append(f"{invalid_numbers} invalid numeric value(s) were found in {column}.")

    if "quantity" in df.columns:
        quantity = pd.to_numeric(df["quantity"], errors="coerce")
        negative_quantity = int((quantity < 0).sum())
        if negative_quantity:
            warnings.append(f"{negative_quantity} negative quantity value(s) were found.")

    if "unit_price" in df.columns:
        unit_price = pd.to_numeric(df["unit_price"], errors="coerce")
        negative_price = int((unit_price < 0).sum())
        if negative_price:
            warnings.append(f"{negative_price} negative unit_price value(s) were found.")

    if "sales" in df.columns:
        sales = pd.to_numeric(df["sales"], errors="coerce")
        negative_sales = int((sales < 0).sum())
        if negative_sales:
            warnings.append(f"{negative_sales} negative sales value(s) were found.")

    if all(column in df.columns for column in ("quantity", "unit_price", "sales")):
        quantity = pd.to_numeric(df["quantity"], errors="coerce")
        unit_price = pd.to_numeric(df["unit_price"], errors="coerce")
        sales = pd.to_numeric(df["sales"], errors="coerce")

        valid_rows = quantity.notna() & unit_price.notna() & sales.notna()
        mismatched_sales = int((valid_rows & ((sales - quantity * unit_price).abs() > 0.01)).sum())

        if mismatched_sales:
            warnings.append(
                f"{mismatched_sales} sales value(s) do not equal quantity * unit_price."
            )

    return ValidationResult(len(errors) == 0, errors, warnings)


def calculate_data_quality(df: pd.DataFrame) -> DataQualityReport:
    """Calculate data-quality metrics for a normalized dataframe."""
    rows = int(df.shape[0])
    columns = int(df.shape[1])
    total_cells = rows * columns

    missing_values = int(df.isna().sum().sum()) if total_cells else 0
    duplicate_rows = int(df.duplicated().sum()) if rows else 0

    invalid_dates = 0
    if "order_date" in df.columns and rows:
        parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
        invalid_dates = int((df["order_date"].notna() & parsed_dates.isna()).sum())

    invalid_numeric_values = 0
    for column in NUMERIC_COLUMNS:
        if column in df.columns and rows:
            parsed_numbers = pd.to_numeric(df[column], errors="coerce")
            invalid_numeric_values += int((df[column].notna() & parsed_numbers.isna()).sum())

    completeness_pct = (
        100.0
        if total_cells == 0
        else max(0.0, min(100.0, (1.0 - missing_values / total_cells) * 100.0))
    )

    return DataQualityReport(
        rows=rows,
        columns=columns,
        missing_values=missing_values,
        duplicate_rows=duplicate_rows,
        invalid_dates=invalid_dates,
        invalid_numeric_values=invalid_numeric_values,
        completeness_pct=completeness_pct,
    )