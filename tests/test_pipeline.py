from __future__ import annotations

import pandas as pd
import pytest

from src.pipeline import run_pipeline


def test_full_pipeline(sample_df) -> None:
    result = run_pipeline(sample_df)

    assert result.validation.is_valid
    assert result.data is not None
    assert result.kpis is not None
    assert result.kpis.total_revenue == pytest.approx(130.0)


def test_pipeline_with_missing_columns() -> None:
    df = pd.DataFrame({"foo": [1]})
    result = run_pipeline(df)

    assert not result.validation.is_valid
    assert result.error is not None