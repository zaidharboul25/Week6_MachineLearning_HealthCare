"""
Unit tests for Data Ingestion, Cleaning & Schema Validation (Category A).
Tests data schema integrity, type casting, boundary constraints, and deduplication.
"""

import pytest
import pandas as pd
import numpy as np

from healthconnect.config import DATA_RAW_DIR, DATASET_FILES
from healthconnect.data.cleaner import (
    clean_patients,
    clean_appointments,
    clean_billing,
    clean_diagnoses,
    clean_claims,
    clean_feedback
)
from healthconnect.data.validator import (
    validate_dataframe_schema,
    check_value_bounds,
    MODEL_FEATURE_SCHEMAS
)
from healthconnect.utils.exceptions import HealthConnectSchemaError, HealthConnectDataError


class TestDataCleaningUnit:
    """Test data cleaning and normalization routines on synthetic data."""

    def test_clean_patients_bounds_and_missing(self, synthetic_patients_raw):
        """Test clipping of Age, imputation of ChronicCondition, and BMI calculation."""
        df_cleaned = clean_patients(synthetic_patients_raw)

        # 1. Age clipping to [0, 120]
        assert df_cleaned["Age"].min() >= 0
        assert df_cleaned["Age"].max() <= 120
        assert df_cleaned.loc[df_cleaned["PatientID"] == "PAT003", "Age"].values[0] == 120
        assert df_cleaned.loc[df_cleaned["PatientID"] == "PAT004", "Age"].values[0] == 0

        # 2. ChronicCondition imputation
        assert df_cleaned.loc[df_cleaned["PatientID"] == "PAT002", "ChronicCondition"].values[0] == "None"

        # 3. Missing BMI calculation from Height and Weight
        # PAT002: weight=62, height=160 -> BMI = 62 / (1.6^2) = 24.2
        pat2_bmi = df_cleaned.loc[df_cleaned["PatientID"] == "PAT002", "BMI"].values[0]
        assert not np.isnan(pat2_bmi)
        assert pat2_bmi == 24.2

    def test_clean_billing_non_negative(self, synthetic_billing_raw):
        """Test non-negative billing constraint."""
        df_cleaned = clean_billing(synthetic_billing_raw)
        assert (df_cleaned["Amount"] >= 0).all()
        assert df_cleaned.loc[df_cleaned["BillingID"] == "BIL002", "Amount"].values[0] == 0.0

    def test_clean_appointments_datetime_casting(self):
        """Test appointment date string parsing to proper datetime."""
        df_appts = pd.DataFrame({
            "AppointmentID": ["APT01", "APT02"],
            "Date": ["2026-03-15", "invalid-date"],
            "VisitType": [" Routine ", "Emergency "]
        })
        df_cleaned = clean_appointments(df_appts)
        assert pd.api.types.is_datetime64_any_dtype(df_cleaned["Date"])
        assert pd.isna(df_cleaned["Date"].iloc[1])
        assert df_cleaned["VisitType"].iloc[0] == "Routine"
        assert df_cleaned["VisitType"].iloc[1] == "Emergency"

    def test_clean_claims_non_negative_and_stripped(self):
        """Test insurance claim cleaning and provider string whitespace stripping."""
        df_claims = pd.DataFrame({
            "ClaimID": ["CLM01", "CLM02"],
            "ClaimAmount": ["50000", "-500"],
            "Provider": [" RSSB ", "MMI"],
            "Status": ["Approved", " Pending "]
        })
        df_cleaned = clean_claims(df_claims)
        assert (df_cleaned["ClaimAmount"] >= 0).all()
        assert df_cleaned["ClaimAmount"].iloc[1] == 0.0
        assert df_cleaned["Provider"].iloc[0] == "RSSB"
        assert df_cleaned["Status"].iloc[1] == "Pending"

    def test_clean_feedback_rating_boundaries(self):
        """Test patient feedback rating constraints (1-5)."""
        df_fb = pd.DataFrame({
            "FeedbackID": ["FB01", "FB02", "FB03"],
            "Rating": [5, 1, 3],
            "Comments": ["Good", "Slow service", "Okay"]
        })
        df_cleaned = clean_feedback(df_fb)
        assert df_cleaned["Rating"].min() >= 1
        assert df_cleaned["Rating"].max() <= 5


class TestSchemaValidationUnit:
    """Test schema and boundary validation logic."""

    def test_validate_claims_schema_success(self):
        """Verify schema validator accepts compliant claims DataFrame."""
        df = pd.DataFrame([{
            "ClaimAmount": 80000.0,
            "BillingAmount": 100000.0,
            "ClaimToBillingRatio": 0.8,
            "ClaimDiff": 20000.0,
            "IsFullClaim": 0,
            "Provider": "RSSB"
        }])
        is_valid, errors = validate_dataframe_schema(df, "claims")
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_claims_schema_missing_column(self):
        """Verify schema validator raises HealthConnectSchemaError on missing column."""
        df = pd.DataFrame([{
            "ClaimAmount": 80000.0,
            # Missing BillingAmount
            "ClaimToBillingRatio": 0.8,
            "ClaimDiff": 20000.0,
            "IsFullClaim": 0,
            "Provider": "RSSB"
        }])
        with pytest.raises(HealthConnectSchemaError) as exc_info:
            validate_dataframe_schema(df, "claims")
        assert "Missing required columns" in str(exc_info.value)
        assert "BillingAmount" in str(exc_info.value)

    def test_validate_empty_dataframe_raises(self):
        """Verify empty DataFrame raises HealthConnectDataError."""
        df_empty = pd.DataFrame()
        with pytest.raises(HealthConnectDataError):
            validate_dataframe_schema(df_empty, "claims")

    def test_check_value_bounds_detection(self):
        """Verify boundary auditing flags extreme out-of-range clinical values."""
        df = pd.DataFrame({
            "Age": [25, 150],  # 150 > 120
            "BMI": [22.0, 85.0]  # 85 > 70
        })
        warnings = check_value_bounds(df)
        assert len(warnings) == 2
        assert any("Age" in w for w in warnings)
        assert any("BMI" in w for w in warnings)

