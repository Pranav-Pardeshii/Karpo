"""
Domain and Infrastructure Exceptions for Smart Crop Advisory System.
"""


class CropAdvisoryError(Exception):
    """Base exception for all domain and operational errors in crop advisory."""

    pass


class ModelNotFoundError(CropAdvisoryError, FileNotFoundError):
    """Raised when a required trained model or preprocessor artifact is missing."""

    pass


class DatasetNotFoundError(CropAdvisoryError, FileNotFoundError):
    """Raised when a required dataset file cannot be located on the filesystem."""

    pass


class ValidationError(CropAdvisoryError, ValueError):
    """Raised when input parameters violate physical agronomic bounds or formats."""

    pass


class CropNotFoundError(CropAdvisoryError, KeyError):
    """Raised when a queried crop cannot be normalized or matched against reference data."""

    pass


class InferenceError(CropAdvisoryError, RuntimeError):
    """Raised when model inference or prediction execution encounters an error."""

    pass
