from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ============================================================
# GLOBAL THEME
# ============================================================

sns.set_theme(
    style="whitegrid",
    context="notebook",
    font_scale=0.9,
)

FIGURE_BG = "#FFFFFF"
AXES_BG = "#FFFFFF"

TEXT_COLOR = "#1F2937"
MUTED_COLOR = "#6B7280"
GRID_COLOR = "#E5E7EB"

PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#10B981"
ACCENT_COLOR = "#8B5CF6"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"

PALETTE = [
    "#2563EB",
    "#10B981",
    "#8B5CF6",
    "#F59E0B",
    "#EF4444",
    "#06B6D4",
    "#EC4899",
    "#84CC16",
]


# ============================================================
# REVENUE OVER TIME
# ============================================================

def revenue_over_time_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render a polished revenue-over-time line chart."""

    title = "Revenue Over Time"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No time-series revenue data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            title,
            "No valid revenue data available.",
        )

    chart_data = pd.DataFrame(
        {
            "date": data.index,
            "revenue": data.values,
        }
    )

    fig, ax = plt.subplots(
        figsize=(11, 4.8)
    )

    sns.lineplot(
        data=chart_data,
        x="date",
        y="revenue",
        ax=ax,
        color=PRIMARY_COLOR,
        linewidth=2.5,
        marker="o" if len(data) <= 20 else None,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Date",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Revenue",
        color=MUTED_COLOR,
    )

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


# ============================================================
# CATEGORY REVENUE
# ============================================================

def category_bar_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render revenue by category using Seaborn."""

    return _horizontal_bar_chart(
        series=series,
        title="Revenue by Category",
        xlabel="Revenue",
        ylabel="Category",
        palette=PALETTE,
        currency=True,
    )


# ============================================================
# REGION REVENUE
# ============================================================

def region_bar_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render revenue by region using Seaborn."""

    return _horizontal_bar_chart(
        series=series,
        title="Revenue by Region",
        xlabel="Revenue",
        ylabel="Region",
        palette=[SECONDARY_COLOR],
        currency=True,
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

def top_products_bar_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render top 10 products by revenue."""

    if series is None or series.empty:
        return _empty_figure(
            "Top Products",
            "No product revenue data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            "Top Products",
            "No valid product revenue data available.",
        )

    data = (
        data.sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    chart_data = pd.DataFrame(
        {
            "product": [
                str(value)
                for value in data.index
            ],
            "revenue": data.values,
        }
    )

    fig, ax = plt.subplots(
        figsize=(10, 5.5)
    )

    sns.barplot(
        data=chart_data,
        x="revenue",
        y="product",
        ax=ax,
        hue="product",
        palette="Blues_r",
        legend=False,
    )

    _style_axes(ax)

    ax.set_title(
        "Top 10 Products by Revenue",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Revenue",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Product",
        color=MUTED_COLOR,
    )

    _add_horizontal_labels(
        ax,
        currency=True,
    )

    fig.tight_layout()

    return fig


# ============================================================
# QUANTITY BY CATEGORY
# ============================================================

def quantity_by_category_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render quantity sold by category."""

    return _horizontal_bar_chart(
        series=series,
        title="Quantity by Category",
        xlabel="Quantity",
        ylabel="Category",
        palette="Purples_r",
        currency=False,
    )


# ============================================================
# ORDERS BY REGION
# ============================================================

def orders_by_region_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render order count by region."""

    return _horizontal_bar_chart(
        series=series,
        title="Orders by Region",
        xlabel="Orders",
        ylabel="Region",
        palette="Greens",
        currency=False,
    )


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

def average_order_value_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render average order value over time."""

    title = "Average Order Value"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No average order value data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            title,
            "No valid average order value data available.",
        )

    chart_data = pd.DataFrame(
        {
            "date": data.index,
            "aov": data.values,
        }
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.lineplot(
        data=chart_data,
        x="date",
        y="aov",
        ax=ax,
        color=WARNING_COLOR,
        linewidth=2.5,
        marker="o" if len(data) <= 20 else None,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Date",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Average Order Value",
        color=MUTED_COLOR,
    )

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


# ============================================================
# MONTHLY GROWTH
# ============================================================

def monthly_growth_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render monthly revenue growth percentage."""

    title = "Monthly Revenue Growth"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No monthly growth data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            title,
            "No valid growth data available.",
        )

    chart_data = pd.DataFrame(
        {
            "period": [
                str(value)
                for value in data.index
            ],
            "growth": data.values,
        }
    )

    chart_data["direction"] = chart_data[
        "growth"
    ].apply(
        lambda value: (
            "Positive"
            if value >= 0
            else "Negative"
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    sns.barplot(
        data=chart_data,
        x="period",
        y="growth",
        hue="direction",
        palette={
            "Positive": SECONDARY_COLOR,
            "Negative": DANGER_COLOR,
        },
        ax=ax,
        legend=False,
    )

    ax.axhline(
        0,
        linewidth=1,
        color=GRID_COLOR,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Period",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Growth (%)",
        color=MUTED_COLOR,
    )

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


# ============================================================
# CATEGORY SHARE / DONUT
# ============================================================

def category_share_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render revenue share by category."""

    title = "Revenue Share by Category"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No category revenue data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            title,
            "No valid category data available.",
        )

    data = (
        data.sort_values(ascending=False)
        .head(8)
    )

    fig, ax = plt.subplots(
        figsize=(7.5, 5.5)
    )

    wedges, _, autotexts = ax.pie(
        data.values,
        autopct="%1.1f%%",
        startangle=90,
        colors=PALETTE[: len(data)],
        wedgeprops={
            "width": 0.42,
            "edgecolor": FIGURE_BG,
        },
    )

    for text in autotexts:
        text.set_fontsize(9)
        text.set_fontweight("bold")
        text.set_color("white")

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.legend(
        wedges,
        [
            str(label)
            for label in data.index
        ],
        title="Category",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False,
    )

    fig.tight_layout()

    return fig


# ============================================================
# SALES HEATMAP
# ============================================================

def sales_heatmap(
    data: pd.DataFrame | None,
    value_column: str = "sales",
) -> plt.Figure:
    """
    Render sales heatmap by weekday and month.

    Required columns:
        order_date
        sales
    """

    title = "Sales Activity Heatmap"

    if data is None or data.empty:
        return _empty_figure(
            title,
            "No sales data available.",
        )

    required_columns = {
        "order_date",
        value_column,
    }

    missing = required_columns.difference(
        data.columns
    )

    if missing:
        return _empty_figure(
            title,
            "Missing required data columns.",
        )

    df = data.copy()

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
    )

    df[value_column] = pd.to_numeric(
        df[value_column],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "order_date",
            value_column,
        ]
    )

    if df.empty:
        return _empty_figure(
            title,
            "No valid sales records available.",
        )

    df["month"] = df[
        "order_date"
    ].dt.month

    df["weekday"] = df[
        "order_date"
    ].dt.day_name()

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    pivot = pd.pivot_table(
        df,
        values=value_column,
        index="weekday",
        columns="month",
        aggfunc="sum",
        fill_value=0,
    )

    pivot = pivot.reindex(
        weekday_order
    ).fillna(0)

    fig, ax = plt.subplots(
        figsize=(11, 5.5)
    )

    sns.heatmap(
        pivot,
        cmap="Blues",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        linecolor=FIGURE_BG,
        ax=ax,
        cbar_kws={
            "label": "Revenue"
        },
    )

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Month",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Day",
        color=MUTED_COLOR,
    )

    fig.tight_layout()

    return fig


# ============================================================
# SALES DISTRIBUTION
# ============================================================

def sales_distribution_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render sales distribution histogram."""

    title = "Sales Distribution"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No sales data available.",
        )

    data = pd.to_numeric(
        series,
        errors="coerce",
    ).dropna()

    if data.empty:
        return _empty_figure(
            title,
            "No valid sales data available.",
        )

    fig, ax = plt.subplots(
        figsize=(9, 4.5)
    )

    sns.histplot(
        data=data,
        bins=30,
        kde=True,
        color=PRIMARY_COLOR,
        ax=ax,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Sales",
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        "Frequency",
        color=MUTED_COLOR,
    )

    fig.tight_layout()

    return fig


# ============================================================
# SALES BOXPLOT
# ============================================================

def sales_boxplot_chart(
    series: pd.Series | None,
) -> plt.Figure:
    """Render sales distribution using a boxplot."""

    title = "Sales Distribution & Outliers"

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No sales data available.",
        )

    data = pd.to_numeric(
        series,
        errors="coerce",
    ).dropna()

    if data.empty:
        return _empty_figure(
            title,
            "No valid sales data available.",
        )

    fig, ax = plt.subplots(
        figsize=(9, 3.5)
    )

    sns.boxplot(
        x=data,
        color=PRIMARY_COLOR,
        ax=ax,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        "Sales",
        color=MUTED_COLOR,
    )

    fig.tight_layout()

    return fig


# ============================================================
# GENERIC HORIZONTAL BAR
# ============================================================

def _horizontal_bar_chart(
    series: pd.Series | None,
    title: str,
    xlabel: str,
    ylabel: str,
    palette,
    currency: bool = False,
) -> plt.Figure:
    """Reusable Seaborn horizontal bar chart."""

    if series is None or series.empty:
        return _empty_figure(
            title,
            "No data available.",
        )

    data = _prepare_series(series)

    if data.empty:
        return _empty_figure(
            title,
            "No valid numeric data available.",
        )

    data = (
        data.sort_values(ascending=False)
        .head(15)
        .sort_values()
    )

    chart_data = pd.DataFrame(
        {
            "label": [
                str(label)
                for label in data.index
            ],
            "value": data.values,
        }
    )

    fig_height = max(
        4.0,
        len(chart_data) * 0.38,
    )

    fig, ax = plt.subplots(
        figsize=(9.5, fig_height)
    )

    sns.barplot(
        data=chart_data,
        x="value",
        y="label",
        hue="label",
        palette=palette,
        legend=False,
        ax=ax,
    )

    _style_axes(ax)

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.set_xlabel(
        xlabel,
        color=MUTED_COLOR,
    )

    ax.set_ylabel(
        ylabel,
        color=MUTED_COLOR,
    )

    _add_horizontal_labels(
        ax,
        currency=currency,
    )

    fig.tight_layout()

    return fig


# ============================================================
# AXIS STYLE
# ============================================================

def _style_axes(
    ax: plt.Axes,
) -> None:
    """Apply consistent dashboard chart styling."""

    ax.set_facecolor(AXES_BG)

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    ax.spines[
        "left"
    ].set_color(GRID_COLOR)

    ax.spines[
        "bottom"
    ].set_color(GRID_COLOR)

    ax.tick_params(
        colors=MUTED_COLOR,
        labelsize=9,
    )

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        alpha=0.45,
        color=GRID_COLOR,
    )


# ============================================================
# HORIZONTAL BAR LABELS
# ============================================================

def _add_horizontal_labels(
    ax: plt.Axes,
    currency: bool = False,
) -> None:
    """Add values at the end of horizontal bars."""

    for container in ax.containers:
        labels = []

        for bar in container:
            value = bar.get_width()

            if currency:
                text = _format_currency(
                    value
                )
            else:
                text = _format_number(
                    value
                )

            labels.append(text)

        ax.bar_label(
            container,
            labels=labels,
            padding=4,
            fontsize=8,
            color=TEXT_COLOR,
        )


# ============================================================
# DATA PREPARATION
# ============================================================

def _prepare_series(
    series: pd.Series,
) -> pd.Series:
    """Safely prepare a pandas Series."""

    result = series.copy()

    result = pd.to_numeric(
        result,
        errors="coerce",
    )

    result = result.dropna()

    if isinstance(
        result.index,
        pd.DatetimeIndex,
    ):
        result = result.sort_index()

    return result


# ============================================================
# NUMBER FORMATTING
# ============================================================

def _format_currency(
    value: float,
) -> str:
    """Format currency values."""

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"৳{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"৳{value / 1_000:.1f}K"

    return f"৳{value:,.0f}"


def _format_number(
    value: float,
) -> str:
    """Format numeric values."""

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


# ============================================================
# EMPTY STATE
# ============================================================

def _empty_figure(
    title: str,
    message: str,
) -> plt.Figure:
    """Render a clean empty-state chart."""

    fig, ax = plt.subplots(
        figsize=(8, 3.5)
    )

    fig.patch.set_facecolor(
        FIGURE_BG
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=15,
    )

    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        fontsize=10,
        color=MUTED_COLOR,
        transform=ax.transAxes,
    )

    ax.axis("off")

    fig.tight_layout()

    return fig