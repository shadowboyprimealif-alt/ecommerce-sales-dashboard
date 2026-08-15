from __future__ import annotations

import pandas as pd

from .analytics import calculate_analytics
from .cleaner import clean_dataframe
from .insights import generate_insights
from .kpis import calculate_kpis
from .models import Insight, PipelineResult, ValidationResult
from .schema import normalize_columns
from .validator import calculate_data_quality, validate_dataframe


def run_pipeline(data: pd.DataFrame, filename: str = "") -> PipelineResult:
    """Run the complete normalize-validate-clean-KPI-analytics-insights pipeline."""
    if data is None:
        validation = ValidationResult(False, ["No data was provided."], [])
        return PipelineResult(
            data=None,
            validation=validation,
            cleaning=None,
            kpis=None,
            analytics={},
            insights=[Insight("Warning", "No data was provided.", "error")],
            data_quality=None,
            error="No data was provided.",
        )

    normalized = normalize_columns(data)
    validation = validate_dataframe(normalized)
    data_quality = calculate_data_quality(normalized)

    if not validation.is_valid:
        insights = [Insight("Warning", error, "error") for error in validation.errors]
        return PipelineResult(
            data=normalized,
            validation=validation,
            cleaning=None,
            kpis=None,
            analytics={},
            insights=insights,
            data_quality=data_quality,
            error="; ".join(validation.errors),
        )

    cleaned, cleaning = clean_dataframe(normalized)

    kpis = calculate_kpis(cleaned)
    analytics = calculate_analytics(cleaned)
    insights = generate_insights(cleaned, kpis, analytics)

    return PipelineResult(
        data=cleaned,
        validation=validation,
        cleaning=cleaning,
        kpis=kpis,
        analytics=analytics,
        insights=insights,
        data_quality=data_quality,
        error=None,
    )