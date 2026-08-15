from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard import (
    charts,
    data_quality,
    insights_panel,
    kpi_cards,
    sidebar,
    summary_table,
)

from src import config
from src.analytics import calculate_analytics, filter_dataframe
from src.data_loader import load_data
from src.exceptions import SalesDashboardError
from src.insights import generate_insights
from src.kpis import calculate_kpis
from src.models import Insight, PipelineResult, ValidationResult
from src.pipeline import run_pipeline


# ============================================================
# MAIN PAGE
# ============================================================

def render_page() -> None:
    """Render the complete Sales Analytics Dashboard."""

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    st.title(config.APP_NAME)

    st.caption(
        "Upload a CSV or Excel file, or use the sample dataset "
        "to analyze sales performance."
    )

    # --------------------------------------------------------
    # Upload / Sample Controls
    # --------------------------------------------------------

    controls = sidebar.render_upload_controls()

    result: PipelineResult | None = None

    if controls["file_bytes"] is not None:
        result = process_upload(
            controls["file_bytes"],
            controls["filename"],
        )

    elif controls["use_sample"]:
        result = process_sample()

        if (
            result.data is not None
            and not result.data.empty
        ):
            _persist_processed_sample(
                result.data
            )

    else:
        st.info(
            "Upload a CSV/Excel file or load "
            "the sample dataset to begin."
        )
        return

    # --------------------------------------------------------
    # Dataset Information
    # --------------------------------------------------------

    if result.data is not None:
        sidebar.render_dataset_info(
            result.data
        )

    # --------------------------------------------------------
    # Validation Errors
    # --------------------------------------------------------

    if not result.validation.is_valid:

        for error in result.validation.errors:
            st.error(error)

        if result.validation.warnings:

            with st.expander(
                "Warnings",
                expanded=False,
            ):
                for warning in (
                    result.validation.warnings
                ):
                    st.warning(warning)

        return

    # --------------------------------------------------------
    # Validation Warnings
    # --------------------------------------------------------

    if result.validation.warnings:

        with st.expander(
            "Data Warnings",
            expanded=False,
        ):
            for warning in (
                result.validation.warnings
            ):
                st.warning(warning)

    # --------------------------------------------------------
    # Empty Dataset Check
    # --------------------------------------------------------

    if (
        result.data is None
        or result.data.empty
    ):
        st.warning(
            "The dataset is empty after "
            "loading and cleaning."
        )

        if result.data_quality is not None:
            data_quality.render_data_quality(
                result.data_quality,
                result.cleaning,
            )

        return

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    filters = sidebar.render_filters(
        result.data
    )

    filtered_df = filter_dataframe(
        result.data,
        filters,
    )

    # --------------------------------------------------------
    # Empty Filter Result
    # --------------------------------------------------------

    if filtered_df.empty:
        st.warning(
            "No records match the selected filters."
        )
        return

    # --------------------------------------------------------
    # Calculate Business Metrics
    # --------------------------------------------------------

    kpis = calculate_kpis(
        filtered_df
    )

    analytics = calculate_analytics(
        filtered_df
    )

    insights = generate_insights(
        filtered_df,
        kpis,
        analytics,
    )

    # ========================================================
    # KPI SECTION
    # ========================================================

    st.markdown("## Key Performance Indicators")

    kpi_cards.render_kpi_cards(
        kpis
    )

    st.divider()

    # ========================================================
    # REVENUE TREND
    # ========================================================

    st.markdown("## Revenue Performance")

    revenue_chart = (
        charts.revenue_over_time_chart(
            analytics.get(
                "revenue_over_time"
            )
        )
    )

    st.pyplot(
        revenue_chart,
        use_container_width=True,
    )

    # ========================================================
    # CATEGORY + REGION
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Revenue by Category"
        )

        fig = charts.category_bar_chart(
            analytics.get(
                "revenue_by_category"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    with col2:

        st.markdown(
            "### Revenue by Region"
        )

        fig = charts.region_bar_chart(
            analytics.get(
                "revenue_by_region"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    # ========================================================
    # TOP PRODUCTS + QUANTITY
    # ========================================================

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            "### Top Products"
        )

        fig = charts.top_products_bar_chart(
            analytics.get(
                "top_products"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    with col4:

        st.markdown(
            "### Quantity by Category"
        )

        fig = charts.quantity_by_category_chart(
            analytics.get(
                "quantity_by_category"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    # ========================================================
    # AOV + MONTHLY GROWTH
    # ========================================================

    col5, col6 = st.columns(2)

    with col5:

        st.markdown(
            "### Average Order Value"
        )

        fig = charts.average_order_value_chart(
            analytics.get(
                "average_order_value"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    with col6:

        st.markdown(
            "### Monthly Growth"
        )

        fig = charts.monthly_growth_chart(
            analytics.get(
                "monthly_growth"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    # ========================================================
    # CATEGORY SHARE + ORDERS BY REGION
    # ========================================================

    col7, col8 = st.columns(2)

    with col7:

        st.markdown(
            "### Revenue Share"
        )

        fig = charts.category_share_chart(
            analytics.get(
                "revenue_by_category"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    with col8:

        st.markdown(
            "### Orders by Region"
        )

        fig = charts.orders_by_region_chart(
            analytics.get(
                "orders_by_region"
            )
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    # ========================================================
    # SALES HEATMAP
    # ========================================================

    st.markdown(
        "## Sales Activity"
    )

    heatmap = charts.sales_heatmap(
        filtered_df,
        value_column="sales",
    )

    st.pyplot(
        heatmap,
        use_container_width=True,
    )

    # ========================================================
    # SALES DISTRIBUTION
    # ========================================================

    col9, col10 = st.columns(2)

    with col9:

        st.markdown(
            "### Sales Distribution"
        )

        distribution = (
            charts.sales_distribution_chart(
                filtered_df["sales"]
                if "sales" in filtered_df.columns
                else None
            )
        )

        st.pyplot(
            distribution,
            use_container_width=True,
        )

    with col10:

        st.markdown(
            "### Sales Outliers"
        )

        boxplot = charts.sales_boxplot_chart(
            filtered_df["sales"]
            if "sales" in filtered_df.columns
            else None
        )

        st.pyplot(
            boxplot,
            use_container_width=True,
        )

    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.divider()

    st.markdown(
        "## Data Quality"
    )

    data_quality.render_data_quality(
        result.data_quality,
        result.cleaning,
    )

    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================

    st.markdown(
        "## Business Insights"
    )

    insights_panel.render_insights(
        insights
    )

    # ========================================================
    # SUMMARY TABLE
    # ========================================================

    st.markdown(
        "## Summary Table"
    )

    summary_table.render_summary_table(
        filtered_df
    )

    # ========================================================
    # RAW / CLEANED DATA
    # ========================================================

    with st.expander(
        "View Detailed Cleaned Data",
        expanded=False,
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# PROCESS UPLOAD
# ============================================================

@st.cache_data(
    show_spinner=False
)
def process_upload(
    file_bytes: bytes,
    filename: str,
) -> PipelineResult:
    """Process uploaded file through the pipeline."""

    try:

        df = load_data(
            file_bytes,
            filename,
        )

        return run_pipeline(
            df,
            filename,
        )

    except SalesDashboardError as exc:

        return _error_pipeline(
            str(exc)
        )

    except Exception:

        return _error_pipeline(
            "An unexpected error occurred while "
            "processing the file. Please check "
            "the file and try again."
        )


# ============================================================
# PROCESS SAMPLE
# ============================================================

@st.cache_data(
    show_spinner=False
)
def process_sample() -> PipelineResult:
    """Process the bundled sample dataset."""

    try:

        if not config.RAW_SAMPLE_PATH.exists():

            return _error_pipeline(
                "Sample data is missing. "
                "Please restore "
                "data/raw/sample_sales.csv."
            )

        df = load_data(
            config.RAW_SAMPLE_PATH,
            config.RAW_SAMPLE_PATH.name,
        )

        return run_pipeline(
            df,
            config.RAW_SAMPLE_PATH.name,
        )

    except SalesDashboardError as exc:

        return _error_pipeline(
            str(exc)
        )

    except Exception:

        return _error_pipeline(
            "Unable to load sample data."
        )


# ============================================================
# ERROR PIPELINE
# ============================================================

def _error_pipeline(
    message: str,
) -> PipelineResult:
    """Build a safe PipelineResult for user-facing errors."""

    validation = ValidationResult(
        is_valid=False,
        errors=[message],
        warnings=[],
    )

    insight = Insight(
        category="Warning",
        message=message,
        severity="error",
    )

    return PipelineResult(
        data=None,
        validation=validation,
        cleaning=None,
        kpis=None,
        analytics={},
        insights=[insight],
        data_quality=None,
        error=message,
    )


# ============================================================
# SAVE PROCESSED SAMPLE
# ============================================================

def _persist_processed_sample(
    cleaned: pd.DataFrame,
) -> None:
    """Persist processed sample data if it does not exist."""

    try:

        config.PROCESSED_SAMPLE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not config.PROCESSED_SAMPLE_PATH.exists():

            cleaned.to_csv(
                config.PROCESSED_SAMPLE_PATH,
                index=False,
            )

    except Exception:
        # Persistence failure should not break dashboard.
        return