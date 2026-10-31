"""
Custom exception hierarchy for HealthConnect Rwanda ML Pipeline.
Provides distinct, actionable error types for data validation, preprocessing,
and model inference layers.
"""

class HealthConnectError(Exception):
    """Base exception for all HealthConnect domain errors."""
    pass

class HealthConnectDataError(HealthConnectError):
    """Raised when data source cannot be loaded, is empty, or corrupted."""
    pass

class HealthConnectSchemaError(HealthConnectError):
    """Raised when incoming dataset does not match expected schema or column requirements."""
    pass

class HealthConnectPreprocessingError(HealthConnectError):
    """Raised when a feature transformation fails unexpectedly."""
    pass

class HealthConnectModelError(HealthConnectError):
    """Raised when model loading, compatibility, or prediction fails."""
    pass

