from __future__ import annotations

from src.analytics import calculate_analytics
from src.insights import generate_insights
from src.kpis import calculate_kpis


def test_insights_are_generated_from_data(sample_df) -> None:
    kpis = calculate_kpis(sample_df)
    analytics = calculate_analytics(sample_df)
    insights = generate_insights(sample_df, kpis, analytics)

    messages = " ".join(insight.message for insight in insights)

    assert "Chair" in messages
    assert "Electronics" in messages
    assert "West" in messages