"""
Data and Schema Validation Module for HealthConnect Rwanda.
Provides deterministic schema, type, and boundary validation for incoming
data batches and single inference payloads across all modeling workflows.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np

from healthconnect.utils.exceptions import HealthConnectSchemaError, HealthConnectDataError

# Expected feature schemas for production models
MODEL_FEATURE_SCHEMAS: Dict[str, Dict[str, List[str]]] = {
    "claims": {
        "required_columns": [
            "ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim", "Provider"
        ],
        "numeric_columns": ["ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim"],
        "categorical_columns": ["Provider"]
    },
    "billing": {
        "required_columns": [
            "Age", "BMI", "DoctorExperience", "FacilityApptVolume",
            "PatientToDoctorRatio", "BedToDoctorRatio", "DepartmentWorkload", "Month",
            "VisitType", "Diagnosis", "Severity", "Gender", "MaritalStatus",
            "Occupation", "Education", "InsuranceID", "ChronicCondition",
            "DepartmentName", "ProvinceName"
        ],
        "numeric_columns": [
            "Age", "BMI", "DoctorExperience", "FacilityApptVolume",
            "PatientToDoctorRatio", "BedToDoctorRatio", "DepartmentWorkload", "Month"
        ],
        "categorical_columns": [
            "VisitType", "Diagnosis", "Severity", "Gender", "MaritalStatus",
            "Occupation", "Education", "InsuranceID", "ChronicCondition",
            "DepartmentName", "ProvinceName"
        ]
    },
    "triage": {
        "required_columns": [
            "Age", "BMI", "DoctorExperience", "FacilityApptVolume", "PatientToDoctorRatio",
            "Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID",
            "ChronicCondition", "Severity", "DepartmentName", "ProvinceName"
        ],
        "numeric_columns": ["Age", "BMI", "DoctorExperience", "FacilityApptVolume", "PatientToDoctorRatio"],
        "categorical_columns": [
            "Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID",
            "ChronicCondition", "Severity", "DepartmentName", "ProvinceName"
        ]
    },
    "satisfaction": {
        "required_columns": [
            "Age", "BMI", "Amount", "DoctorExperience", "PatientToDoctorRatio", "DepartmentWorkload",
            "VisitType", "Severity", "Diagnosis", "Gender", "InsuranceID", "DepartmentName"
        ],
        "numeric_columns": ["Age", "BMI", "Amount", "DoctorExperience", "PatientToDoctorRatio", "DepartmentWorkload"],
        "categorical_columns": ["VisitType", "Severity", "Diagnosis", "Gender", "InsuranceID", "DepartmentName"]
    }
}

# Domain constraints and realistic ranges
VALUE_BOUNDS: Dict[str, Tuple[float, float]] = {
    "Age": (0, 120),
    "BMI": (10.0, 70.0),
    "DoctorExperience": (0, 60),
    "FacilityApptVolume": (0, 100000),
    "PatientToDoctorRatio": (0.0, 500.0),
    "BedToDoctorRatio": (0.0, 100.0),
    "DepartmentWorkload": (0, 50000),
    "Month": (1, 12),
    "ClaimAmount": (0.0, 50000000.0),
    "BillingAmount": (0.0, 50000000.0),
    "Amount": (0.0, 50000000.0),
}


def validate_dataframe_schema(
    df: pd.DataFrame,
    model_name: str,
    strict_numeric: bool = True
) -> Tuple[bool, List[str]]:
    """
    Validate that an input DataFrame contains all required columns and meets type invariants.
    Returns:
        (is_valid, list_of_errors)
    Raises:
        HealthConnectDataError: If DataFrame is None or empty.
        HealthConnectSchemaError: If required columns are missing.
    """
    if df is None:
        raise HealthConnectDataError("Input DataFrame cannot be None.")
    if len(df) == 0:
        raise HealthConnectDataError("Input DataFrame contains 0 rows.")

    if model_name not in MODEL_FEATURE_SCHEMAS:
        raise ValueError(f"Unknown model name '{model_name}'. Known models: {list(MODEL_FEATURE_SCHEMAS.keys())}")

    schema = MODEL_FEATURE_SCHEMAS[model_name]
    required = set(schema["required_columns"])
    actual = set(df.columns)
    missing = required - actual

    errors: List[str] = []

    if missing:
        msg = f"Missing required columns for model '{model_name}': {sorted(list(missing))}"
        errors.append(msg)
        raise HealthConnectSchemaError(msg)

    if strict_numeric:
        for num_col in schema["numeric_columns"]:
            if num_col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[num_col]):
                    # Attempt safe conversion check
                    converted = pd.to_numeric(df[num_col], errors="coerce")
                    if converted.isna().any() and not df[num_col].isna().all():
                        errors.append(f"Column '{num_col}' contains non-numeric values that cannot be cast.")

    return (len(errors) == 0, errors)


def check_value_bounds(df: pd.DataFrame) -> List[str]:
    """
    Check if numeric columns contain values outside clinical or operational plausibility bounds.
    Returns a list of warning messages (does not raise, for soft-boundary auditing).
    """
    warnings: List[str] = []
    for col, (lower, upper) in VALUE_BOUNDS.items():
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            below = (df[col] < lower).sum()
            above = (df[col] > upper).sum()
            if below > 0:
                warnings.append(f"Column '{col}' has {below} values below boundary {lower}.")
            if above > 0:
                warnings.append(f"Column '{col}' has {above} values above boundary {upper}.")
    return warnings

