from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd

from .config import MAX_UPLOAD_BYTES, SUPPORTED_EXTENSIONS
from .exceptions import DataLoadingError, UnsupportedFileTypeError
from .utils import get_file_extension


def load_data(source: bytes | bytearray | Path | str, filename: str | None = None) -> pd.DataFrame:
    """Load CSV or Excel data from bytes or a filesystem path."""
    if isinstance(source, (bytes, bytearray)):
        data = bytes(source)
        name = filename or ""
    else:
        path = Path(source)
        if not path.exists():
            raise DataLoadingError("The file does not exist.")
        data = path.read_bytes()
        name = filename or path.name

    if not data:
        raise DataLoadingError("The uploaded file is empty.")

    if len(data) > MAX_UPLOAD_BYTES:
        raise DataLoadingError("The uploaded file is too large.")

    extension = get_file_extension(name)
    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            "Unsupported file type. Please upload a .csv, .xlsx, or .xls file."
        )

    buffer = BytesIO(data)

    try:
        if extension == ".csv":
            df = _read_csv_buffer(buffer)
        else:
            df = _read_excel_buffer(buffer, extension)
    except UnsupportedFileTypeError:
        raise
    except DataLoadingError:
        raise
    except Exception as exc:
        raise DataLoadingError(
            "Unable to read the file. Please check that it is a valid CSV or Excel file."
        ) from exc

    if df is None:
        raise DataLoadingError("No readable data was found in the file.")

    return df


def _read_csv_buffer(buffer: BytesIO) -> pd.DataFrame:
    """Read a CSV file from an in-memory byte buffer."""
    last_error: Exception | None = None

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            buffer.seek(0)
            df = pd.read_csv(
                buffer,
                encoding=encoding,
                sep=None,
                engine="python",
                on_bad_lines="warn",
            )

            if df.columns.size == 0:
                raise DataLoadingError("The CSV file does not contain any columns.")

            return df
        except UnicodeDecodeError as exc:
            last_error = exc
        except pd.errors.EmptyDataError as exc:
            raise DataLoadingError("The CSV file is empty or has no readable rows.") from exc
        except Exception as exc:
            last_error = exc

    raise DataLoadingError(
        "Unable to decode the CSV file. Please try exporting it as UTF-8 or Latin-1."
    ) from last_error


def _read_excel_buffer(buffer: BytesIO, extension: str) -> pd.DataFrame:
    """Read the first worksheet of an Excel file from an in-memory byte buffer."""
    engine = "openpyxl" if extension == ".xlsx" else "xlrd"

    try:
        df = pd.read_excel(buffer, sheet_name=0, engine=engine)
    except ImportError as exc:
        raise DataLoadingError(
            "Reading .xls files requires the xlrd package. Please convert the file to .xlsx or install xlrd."
        ) from exc

    if df is None:
        raise DataLoadingError("The Excel file is empty.")

    if df.columns.size == 0:
        raise DataLoadingError("The Excel file does not contain any columns.")

    return df