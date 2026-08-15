from __future__ import annotations

import streamlit as st

from src.models import Insight


def render_insights(insights: list[Insight]) -> None:
    """Render business insights."""
    if not insights:
        st.info("No insights available.")
        return

    for insight in insights:
        if insight.severity == "error":
            st.error(f"{insight.category}: {insight.message}")
        elif insight.severity == "warning":
            st.warning(f"{insight.category}: {insight.message}")
        else:
            st.info(f"{insight.category}: {insight.message}")