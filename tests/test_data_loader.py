from __future__ import annotations

import pandas as pd
import pytest

from src.data_loader import load_data
from src.exceptions import DataLoadingError, UnsupportedFileTypeError


def test_csv_loading(tmp_path, sample_df) -> None:
    path = tmp_path / "test.csv"
    sample_df.to_csv(path, index=False)

    df = load_data(path)

    assert len(df) == 4
    assert "order_id" in df.columns


def test_excel_loading(tmp_path, sample_df) -> None:
    path = tmp_path / "test.xlsx"
    sample_df.to_excel(path, index=False)

    df = load_data(path)

    assert len(df) == 4
    assert "order_id" in df.columns


def test_unsupported_extension(tmp_path) -> None:
    path = tmp_path / "test.txt"
    path.write_text("hello")

    with pytest.raises(UnsupportedFileTypeError):
        load_data(path)


def test_invalid_excel_file(tmp_path) -> None:
    path = tmp_path / "bad.xlsx"
    path.write_bytes(b"not an excel file")

    with pytest.raises(DataLoadingError):
        load_data(path)


def test_empty_file(tmp_path) -> None:
    path = tmp_path / "empty.csv"
    path.write_bytes(b"")

    with pytest.raises(DataLoadingError):
        load_data(path)