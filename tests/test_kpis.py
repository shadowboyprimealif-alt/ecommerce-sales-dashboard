from __future__ import annotations

import pytest

from src.kpis import calculate_kpis


def test_all_kpis(sample_df) -> None:
    kpis = calculate_kpis(sample_df)

    assert kpis.total_revenue == pytest.approx(130.0)
    assert kpis.total_orders == 4
    assert kpis.total_quantity == pytest.approx(7.0)
    assert kpis.average_order_value == pytest.approx(32.5)
    assert kpis.average_unit_price == pytest.approx(22.5)
    assert kpis.top_product == "Chair"
    assert kpis.top_category == "Electronics"
    assert kpis.top_region == "West"
    assert kpis.revenue_growth_pct == pytest.approx(60.0)