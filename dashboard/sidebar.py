from __future__ import annotations

import pandas as pd
import streamlit as st

from src import config


def render_upload_controls() -> dict:
    """Render logo, uploader, and sample-data controls in the sidebar."""
    _render_logo()

    st.sidebar.header("Data Source")

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
    )

    load_sample = st.sidebar.button("Load sample dataset")

    if load_sample:
        st.session_state["use_sample"] = True

    if uploaded_file is not None:
        st.session_state["use_sample"] = False
        return {
            "file_bytes": uploaded_file.getvalue(),
            "filename": uploaded_file.name,
            "use_sample": False,
        }

    return {
        "file_bytes": None,
        "filename": None,
        "use_sample": bool(st.session_state.get("use_sample", False)),
    }


def render_dataset_info(df: pd.DataFrame | None) -> None:
    """Render dataset metadata in the sidebar."""
    if df is None:
        return

    st.sidebar.subheader("Dataset")
    st.sidebar.write(f"Rows: {len(df):,}")
    st.sidebar.write(f"Columns: {df.shape[1]:,}")

    if "order_date" in df.columns:
        dates = pd.to_datetime(df["order_date"], errors="coerce").dropna()
        if not dates.empty:
            st.sidebar.write(f"Date range: {dates.min().date()} to {dates.max().date()}")


def render_filters(df: pd.DataFrame | None) -> dict:
    """Render filters and return the selected filter values."""
    st.sidebar.subheader("Filters")

    filters: dict = {}

    if df is None or df.empty:
        st.sidebar.info("No filter options available.")
        return filters

    if "order_date" in df.columns:
        dates = pd.to_datetime(df["order_date"], errors="coerce").dropna()

        if not dates.empty:
            min_date = dates.min().date()
            max_date = dates.max().date()
            value = (min_date, max_date) if min_date != max_date else (min_date, min_date)

            selected_range = st.sidebar.slider(
                "Date range",
                min_value=min_date,
                max_value=max_date,
                value=value,
            )

            filters["start_date"] = pd.Timestamp(selected_range[0])
            filters["end_date"] = pd.Timestamp(selected_range[1])

    filter_columns = (
        ("category", "categories"),
        ("region", "regions"),
        ("product", "products"),
    )

    for column, key in filter_columns:
        if column in df.columns:
            options = sorted({str(value) for value in df[column].dropna().unique().tolist()})

            if options:
                selected = st.sidebar.multiselect(
                    column.capitalize(),
                    options=options,
                    default=options,
                )
                filters[key] = selected

    return filters


def _render_logo() -> None:
    """Render the application logo if present."""
    if config.LOGO_PATH.exists():
        st.sidebar.image(str(config.LOGO_PATH), width=180)
    else:
        st.sidebar.markdown("### 📊 Sales Analytics")