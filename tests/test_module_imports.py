from __future__ import annotations

import importlib

import pytest

MODULES = [
    "src",
    "src.config",
    "src.exceptions",
    "src.models",
    "src.utils",
    "src.schema",
    "src.data_loader",
    "src.validator",
    "src.cleaner",
    "src.kpis",
    "src.analytics",
    "src.insights",
    "src.pipeline",
    "dashboard",
    "dashboard.sidebar",
    "dashboard.kpi_cards",
    "dashboard.charts",
    "dashboard.data_quality",
    "dashboard.insights_panel",
    "dashboard.summary_table",
    "dashboard.page",
]


@pytest.mark.parametrize("module_name", MODULES)
def test_module_imports(module_name: str) -> None:
    importlib.import_module(module_name)