from __future__ import annotations

from src.analytics import calculate_analytics


def test_analytics(sample_df) -> None:
    analytics = calculate_analytics(sample_df)

    monthly = analytics["monthly_revenue"]
    assert monthly.sum() == 130.0

    revenue_by_product = analytics["revenue_by_product"]
    assert revenue_by_product["Chair"] == 50.0

    revenue_by_category = analytics["revenue_by_category"]
    assert revenue_by_category["Electronics"] == 80.0

    revenue_by_region = analytics["revenue_by_region"]
    assert revenue_by_region["West"] == 50.0

    assert len(analytics["top_products"]) <= 10