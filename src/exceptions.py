from __future__ import annotations


class SalesDashboardError(Exception):
    """Base exception for the Sales Analytics Dashboard."""


class DataLoadingError(SalesDashboardError):
    """Raised when a file cannot be loaded or parsed."""


class UnsupportedFileTypeError(DataLoadingError):
    """Raised when the uploaded file type is not supported."""


class DataValidationError(SalesDashboardError):
    """Raised when data validation fails."""


class MissingColumnsError(DataValidationError):
    """Raised when required columns are missing."""


class DataProcessingError(SalesDashboardError):
    """Raised when data processing fails."""