from __future__ import annotations

import streamlit as st

from src.models import CleaningReport, DataQualityReport


def render_data_quality(report: DataQualityReport | None, cleaning: CleaningReport | None = None) -> None:
    """Render data-quality metrics and cleaning statistics."""
    if report is None:
        st.info("No data-quality report available.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{report.rows:,}")
    col2.metric("Columns", f"{report.columns:,}")
    col3.metric("Missing Values", f"{report.missing_values:,}")
    col4.metric("Duplicate Rows", f"{report.duplicate_rows:,}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Invalid Dates", f"{report.invalid_dates:,}")
    col6.metric("Invalid Numeric Values", f"{report.invalid_numeric_values:,}")
    col7.metric("Data Completeness", f"{report.completeness_pct:.1f}%")
    col8.metric("Cleaning Applied", "Yes" if cleaning is not None else "No")

    if cleaning is not None:
        with st.expander("Cleaning statistics", expanded=False):
            for message in cleaning.messages:
                st.write(message)