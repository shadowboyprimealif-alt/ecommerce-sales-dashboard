from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class CleaningReport:
    rows_uploaded: int
    empty_rows_removed: int
    duplicate_rows_removed: int
    invalid_rows_removed: int
    missing_sales_calculated: int
    final_rows: int
    messages: list[str] = field(default_factory=list)


@dataclass
class DataQualityReport:
    rows: int
    columns: int
    missing_values: int
    duplicate_rows: int
    invalid_dates: int
    invalid_numeric_values: int
    completeness_pct: float


@dataclass
class KPIResult:
    total_revenue: float = 0.0
    total_orders: int = 0
    total_quantity: float = 0.0
    average_order_value: float = 0.0
    average_unit_price: float = 0.0
    top_product: str | None = None
    top_category: str | None = None
    top_region: str | None = None
    revenue_growth_pct: float | None = None
    period_label: str | None = None


@dataclass
class Insight:
    category: str
    message: str
    severity: str = "info"


@dataclass
class PipelineResult:
    data: pd.DataFrame | None
    validation: ValidationResult
    cleaning: CleaningReport | None
    kpis: KPIResult | None
    analytics: dict[str, Any]
    insights: list[Insight]
    data_quality: DataQualityReport | None
    error: str | None = None