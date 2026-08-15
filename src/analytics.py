from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_analytics(df: pd.DataFrame) -> dict[str, pd.Series | pd.DataFrame]:
    """Calculate analytics from a cleaned sales dataframe."""
    revenue_by_product = _group_sum(df, "product", "sales")
    revenue_by_category = _group_sum(df, "category", "sales")
    revenue_by_region = _group_sum(df, "region", "sales")

    return {
        "revenue_over_time": revenue_over_time(df),
        "daily_revenue": revenue_over_time(df),
        "monthly_revenue": monthly_revenue(df),
        "revenue_by_product": revenue_by_product,
        "revenue_by_category": revenue_by_category,
        "revenue_by_region": revenue_by_region,
        "quantity_by_product": _group_sum(df, "product", "quantity"),
        "quantity_by_category": _group_sum(df, "category", "quantity"),
        "aov_trend": aov_trend(df),
        "top_products": revenue_by_product.head(10),
        "bottom_products": revenue_by_product.sort_values().head(5),
        "category_performance": performance_table(df, "category"),
        "regional_performance": performance_table(df, "region"),
        "product_summary": product_summary(df),
    }


def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Filter a cleaned dataframe using sidebar filter values."""
    if df is None or df.empty or not filters:
        return df

    filtered = df.copy()

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")

    if "order_date" in filtered.columns:
        if start_date is not None:
            filtered = filtered[filtered["order_date"] >= pd.Timestamp(start_date)]
        if end_date is not None:
            filtered = filtered[filtered["order_date"] <= pd.Timestamp(end_date)]

    filter_map = {
        "category": "categories",
        "region": "regions",
        "product": "products",
    }

    for column, key in filter_map.items():
        values = filters.get(key)
        if values and column in filtered.columns:
            filtered = filtered[filtered[column].isin(values)]

    return filtered


def revenue_over_time(df: pd.DataFrame) -> pd.Series:
    """Return daily revenue indexed by date."""
    if df.empty or "order_date" not in df.columns or "sales" not in df.columns:
        return _empty_series("revenue")

    work = df.copy()
    work["order_date"] = pd.to_datetime(work["order_date"], errors="coerce")
    work["sales"] = pd.to_numeric(work["sales"], errors="coerce")
    work = work.dropna(subset=["order_date", "sales"])

    if work.empty:
        return _empty_series("revenue")

    return work.groupby("order_date")["sales"].sum().sort_index()


def monthly_revenue(df: pd.DataFrame) -> pd.Series:
    """Return monthly revenue indexed by month string."""
    if df.empty or "order_date" not in df.columns or "sales" not in df.columns:
        return _empty_series("monthly_revenue")

    work = df.copy()
    work["order_date"] = pd.to_datetime(work["order_date"], errors="coerce")
    work["sales"] = pd.to_numeric(work["sales"], errors="coerce")
    work = work.dropna(subset=["order_date", "sales"])

    if work.empty:
        return _empty_series("monthly_revenue")

    work["month"] = work["order_date"].dt.to_period("M")
    monthly = work.groupby("month")["sales"].sum().sort_index()
    monthly.index = monthly.index.astype(str)
    return monthly


def aov_trend(df: pd.DataFrame) -> pd.Series:
    """Return average order value by month."""
    if (
        df.empty
        or "order_date" not in df.columns
        or "sales" not in df.columns
        or "order_id" not in df.columns
    ):
        return _empty_series("aov")

    work = df.copy()
    work["order_date"] = pd.to_datetime(work["order_date"], errors="coerce")
    work["sales"] = pd.to_numeric(work["sales"], errors="coerce")
    work = work.dropna(subset=["order_date", "sales"])

    if work.empty:
        return _empty_series("aov")

    work["month"] = work["order_date"].dt.to_period("M")
    revenue = work.groupby("month")["sales"].sum()
    orders = work.groupby("month")["order_id"].nunique()
    aov = revenue / orders.replace(0, np.nan)
    aov = aov.dropna()
    aov.index = aov.index.astype(str)
    return aov


def performance_table(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Return a performance table for a category or region column."""
    columns = [group_col.capitalize(), "Revenue", "Quantity", "Orders", "Average Price"]

    if df.empty or group_col not in df.columns or "sales" not in df.columns:
        return pd.DataFrame(columns=columns)

    work = df.copy()
    work["sales"] = _to_numeric(work, "sales")
    work["quantity"] = _to_numeric(work, "quantity")
    work["unit_price"] = _to_numeric(work, "unit_price")

    if "order_id" in work.columns:
        grouped = work.groupby(group_col, dropna=False).agg(
            Revenue=("sales", "sum"),
            Quantity=("quantity", "sum"),
            Orders=("order_id", "nunique"),
            Average_Price=("unit_price", "mean"),
        )
    else:
        grouped = work.groupby(group_col, dropna=False).agg(
            Revenue=("sales", "sum"),
            Quantity=("quantity", "sum"),
            Orders=("sales", "count"),
            Average_Price=("unit_price", "mean"),
        )

    grouped = grouped.reset_index().fillna(0.0).sort_values("Revenue", ascending=False)
    grouped = grouped.rename(columns={group_col: group_col.capitalize(), "Average_Price": "Average Price"})
    return grouped


def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a product-level summary table."""
    columns = ["Product", "Category", "Revenue", "Quantity", "Orders", "Average Price"]

    if (
        df.empty
        or "product" not in df.columns
        or "category" not in df.columns
        or "sales" not in df.columns
    ):
        return pd.DataFrame(columns=columns)

    work = df.copy()
    work["sales"] = _to_numeric(work, "sales")
    work["quantity"] = _to_numeric(work, "quantity")
    work["unit_price"] = _to_numeric(work, "unit_price")

    if "order_id" in work.columns:
        grouped = work.groupby(["product", "category"], dropna=False).agg(
            Revenue=("sales", "sum"),
            Quantity=("quantity", "sum"),
            Orders=("order_id", "nunique"),
            Average_Price=("unit_price", "mean"),
        )
    else:
        grouped = work.groupby(["product", "category"], dropna=False).agg(
            Revenue=("sales", "sum"),
            Quantity=("quantity", "sum"),
            Orders=("sales", "count"),
            Average_Price=("unit_price", "mean"),
        )

    grouped = grouped.reset_index().fillna(0.0).sort_values("Revenue", ascending=False)
    grouped = grouped.rename(
        columns={
            "product": "Product",
            "category": "Category",
            "Average_Price": "Average Price",
        }
    )
    return grouped


def _empty_series(name: str) -> pd.Series:
    """Return an empty float Series."""
    return pd.Series(dtype="float64", name=name)


def _to_numeric(df: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric Series for a column, filling missing values with zero."""
    if column not in df.columns:
        return pd.Series(0.0, index=df.index)
    return pd.to_numeric(df[column], errors="coerce").fillna(0.0)


def _group_sum(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
) -> pd.Series:
    """Group by a column and sum another column safely."""
    if df.empty or group_col not in df.columns or value_col not in df.columns:
        return _empty_series(value_col)

    work = df.copy()
    work[value_col] = pd.to_numeric(work[value_col], errors="coerce")
    work = work.dropna(subset=[value_col])

    if work.empty:
        return _empty_series(value_col)

    grouped = work.groupby(group_col, dropna=False)[value_col].sum()
    grouped = grouped[grouped.index.notna()].sort_values(ascending=False)
    grouped.index = grouped.index.astype(str)
    return grouped