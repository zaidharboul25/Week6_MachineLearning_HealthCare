"""
Robustness, Edge Cases, and Fault Tolerance Validation Tests (Category E).
Verifies system resilience against unexpected, malformed, out-of-range,
and missing data inputs without unhandled crashes.
"""

import pytest
import pandas as pd
import numpy as np
import joblib

from healthconnect.config import ARTIFACTS_DIR
from healthconnect.data.validator import validate_dataframe_schema
from healthconnect.utils.exceptions import HealthConnectSchemaError, HealthConnectDataError


class TestRobustnessAndEdgeCases:
    """Evaluate pipeline resilience on hostile or degraded inputs."""

    def test_pipeline_handles_missing_numerical_values_gracefully(self, sample_billing_payload):
        """Verify pipeline does not crash when numerical features contain NaNs (handled by imputer)."""
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        sample = sample_billing_payload.copy()
        sample["BMI"] = np.nan
        sample["DoctorExperience"] = np.nan
        sample["PatientToDoctorRatio"] = np.nan

        input_df = pd.DataFrame([sample])
        pred = pipe.predict(input_df)
        assert len(pred) == 1
        assert not np.isnan(pred[0])
        assert pred[0] > 0

    def test_pipeline_handles_unseen_categorical_levels_gracefully(self, sample_billing_payload):
        """Verify pipeline does not crash on brand-new unseen categories (handled by OneHotEncoder ignore)."""
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        sample = sample_billing_payload.copy()
        sample["Diagnosis"] = "CompletelyUnknownTropicalFever"
        sample["ProvinceName"] = "ForeignProvince"
        sample["Occupation"] = "Astronaut"

        input_df = pd.DataFrame([sample])
        pred = pipe.predict(input_df)
        assert len(pred) == 1
        assert pred[0] > 0

    def test_pipeline_handles_extreme_numerical_values_gracefully(self, sample_billing_payload):
        """Verify pipeline produces finite prediction even with extreme values."""
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        sample = sample_billing_payload.copy()
        sample["Age"] = 120
        sample["FacilityApptVolume"] = 50000

        input_df = pd.DataFrame([sample])
        pred = pipe.predict(input_df)
        assert len(pred) == 1
        assert np.isfinite(pred[0])

    def test_empty_dataframe_raises_expected_exception(self):
        """Verify passing empty DataFrame to validator raises HealthConnectDataError."""
        empty_df = pd.DataFrame()
        with pytest.raises(HealthConnectDataError) as exc_info:
            validate_dataframe_schema(empty_df, "claims")
        assert "contains 0 rows" in str(exc_info.value)

    def test_schema_mismatch_raises_expected_exception(self):
        """Verify passing wrong schema raises HealthConnectSchemaError."""
        bad_df = pd.DataFrame([{"wrong_col_1": 12, "wrong_col_2": "test"}])
        with pytest.raises(HealthConnectSchemaError) as exc_info:
            validate_dataframe_schema(bad_df, "claims")
        assert "Missing required columns" in str(exc_info.value)

    def test_claims_classifier_handles_unseen_provider(self):
        """Verify claims classifier runs smoothly on non-existent insurance provider."""
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        sample = pd.DataFrame([{
            "ClaimAmount": 50000.0,
            "BillingAmount": 60000.0,
            "ClaimToBillingRatio": 0.833,
            "ClaimDiff": 10000.0,
            "IsFullClaim": 0,
            "Provider": "NonExistentGlobalHealthInsurer"
        }])
        pred = pipe.predict(sample)
        proba = pipe.predict_proba(sample)
        assert len(pred) == 1
        assert pred[0] in [0, 1]
        assert proba.shape == (1, 2)

