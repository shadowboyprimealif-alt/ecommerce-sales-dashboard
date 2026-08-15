from __future__ import annotations

import pandas as pd
import streamlit as st

from src.analytics import product_summary


def render_summary_table(df: pd.DataFrame | None) -> None:
    """Render the product/category summary table."""
    if df is None or df.empty:
        st.info("No summary data available.")
        return

    summary = product_summary(df)

    if summary.empty:
        st.info("No summary data available.")
        return

    st.dataframe(summary, use_container_width=True, hide_index=True)