from __future__ import annotations

import streamlit as st

from src.models import KPIResult
from src.utils import format_currency


def render_kpi_cards(kpis: KPIResult) -> None:
    """Render the four primary KPI cards."""
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", format_currency(kpis.total_revenue))
    col2.metric("Total Orders", f"{int(kpis.total_orders):,}")
    col3.metric("Total Quantity", f"{int(kpis.total_quantity):,}")
    col4.metric("Average Order Value", format_currency(kpis.average_order_value))