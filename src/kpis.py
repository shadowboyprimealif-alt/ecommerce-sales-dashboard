from __future__ import annotations

import pandas as pd

from .models import KPIResult
from .utils import safe_div


def calculate_kpis(df: pd.DataFrame) -> KPIResult:
    """Calculate KPI values from a cleaned sales dataframe."""
    if df is None or df.empty:
        return KPIResult()

    sales = _numeric_series(df, "sales")
    quantity = _numeric_series(df, "quantity")
    unit_price = _numeric_series(df, "unit_price")

    total_revenue = float(sales.fillna(0.0).sum())
    total_orders = int(df["order_id"].nunique()) if "order_id" in df.columns else 0
    total_quantity = float(quantity.fillna(0.0).sum())
    average_order_value = safe_div(total_revenue, total_orders, 0.0)
    average_unit_price = float(unit_price.mean()) if unit_price.notna().any() else 0.0

    top_product = _top_by_revenue(df, "product")
    top_category = _top_by_revenue(df, "category")
    top_region = _top_by_revenue(df, "region")

    revenue_growth_pct, period_label = _revenue_growth(df)

    return KPIResult(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_quantity=total_quantity,
        average_order_value=average_order_value,
        average_unit_price=average_unit_price,
        top_product=top_product,
        top_category=top_category,
        top_region=top_region,
        revenue_growth_pct=revenue_growth_pct,
        period_label=period_label,
    )


def _numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric pandas Series for a column, or an empty float Series."""
    if column not in df.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(df[column], errors="coerce")


def _top_by_revenue(df: pd.DataFrame, column: str) -> str | None:
    """Return the highest-revenue item for a grouping column."""
    if df.empty or column not in df.columns or "sales" not in df.columns:
        return None

    sales = pd.to_numeric(df["sales"], errors="coerce")
    grouped = df.assign(_sales=sales).groupby(column)["_sales"].sum().dropna()
    grouped = grouped[grouped.index.notna()]

    if grouped.empty:
        return None

    return str(grouped.idxmax())


def _revenue_growth(df: pd.DataFrame) -> tuple[float | None, str | None]:
    """Calculate month-over-month revenue growth when enough data exists."""
    if df.empty or "order_date" not in df.columns or "sales" not in df.columns:
        return None, None

    dates = pd.to_datetime(df["order_date"], errors="coerce")
    valid_dates = dates.notna()

    if int(valid_dates.sum()) < 2:
        return None, None

    sales = pd.to_numeric(df["sales"], errors="coerce")
    monthly_revenue = sales[valid_dates].groupby(dates[valid_dates].dt.to_period("M")).sum()
    monthly_revenue = monthly_revenue.dropna().sort_index()

    if len(monthly_revenue) < 2:
        return None, None

    previous = float(monthly_revenue.iloc[-2])
    current = float(monthly_revenue.iloc[-1])
    period_label = f"{monthly_revenue.index[-2]} to {monthly_revenue.index[-1]}"

    if previous == 0.0:
        return None, period_label

    growth = ((current - previous) / previous) * 100.0
    return float(growth), period_label