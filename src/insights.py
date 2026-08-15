from __future__ import annotations

import pandas as pd

from .models import Insight, KPIResult
from .utils import format_currency


def generate_insights(
    df: pd.DataFrame,
    kpis: KPIResult,
    analytics: dict[str, pd.Series | pd.DataFrame],
) -> list[Insight]:
    """Generate dynamic business insights from actual data."""
    insights: list[Insight] = []

    if df is None or df.empty:
        insights.append(
            Insight(
                category="Warning",
                message="No rows are available for analysis after cleaning and filtering.",
                severity="warning",
            )
        )
        return insights

    insights.append(
        Insight(
            category="Revenue",
            message=f"Total revenue is {format_currency(kpis.total_revenue)}.",
        )
    )

    if kpis.total_orders == 0:
        insights.append(
            Insight(
                category="Warning",
                message="No unique orders were found in the current dataset.",
                severity="warning",
            )
        )

    if kpis.top_product:
        insights.append(
            Insight(
                category="Product",
                message=f"{kpis.top_product} is the best-performing product by revenue.",
            )
        )

    if kpis.top_category:
        insights.append(
            Insight(
                category="Category",
                message=f"Revenue is strongest in {kpis.top_category}.",
            )
        )

    if kpis.top_region:
        insights.append(
            Insight(
                category="Region",
                message=f"{kpis.top_region} generated the highest revenue.",
            )
        )

    if kpis.revenue_growth_pct is not None:
        direction = "increased" if kpis.revenue_growth_pct >= 0 else "decreased"
        insights.append(
            Insight(
                category="Trend",
                message=(
                    f"Revenue {direction} by {abs(kpis.revenue_growth_pct):.1f}% "
                    f"from {kpis.period_label}."
                ),
            )
        )

    monthly = analytics.get("monthly_revenue")
    if isinstance(monthly, pd.Series) and not monthly.empty:
        peak_month = monthly.idxmax()
        insights.append(
            Insight(
                category="Trend",
                message=f"The strongest monthly revenue period is {peak_month}.",
            )
        )

    bottom_products = analytics.get("bottom_products")
    if isinstance(bottom_products, pd.Series) and not bottom_products.empty and kpis.total_revenue > 0:
        insights.append(
            Insight(
                category="Product",
                message=f"{bottom_products.index[0]} has relatively low revenue compared with other products.",
            )
        )

    if kpis.total_revenue <= 0:
        insights.append(
            Insight(
                category="Warning",
                message="No positive revenue was found in the current data.",
                severity="warning",
            )
        )

    return insights