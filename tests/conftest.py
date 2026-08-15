from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["A1", "A2", "A3", "A4"],
            "order_date": ["2024-01-01", "2024-01-15", "2024-02-01", "2024-02-15"],
            "product": ["Mouse", "Keyboard", "Mouse", "Chair"],
            "category": ["Electronics", "Electronics", "Electronics", "Furniture"],
            "region": ["North", "South", "North", "West"],
            "quantity": [1, 2, 3, 1],
            "unit_price": [10.0, 20.0, 10.0, 50.0],
            "sales": [10.0, 40.0, 30.0, 50.0],
            "customer_id": ["C1", "C2", "C3", "C4"],
        }
    )