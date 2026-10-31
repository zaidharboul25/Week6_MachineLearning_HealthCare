"""
Integration tests for HealthConnect Machine Learning Pipeline (Category D).
Verifies the complete data -> cleaning -> feature engineering -> model prediction chain.
"""

import pytest
import pandas as pd
import numpy as np
import joblib

from healthconnect.config import ARTIFACTS_DIR
from healthconnect.data.cleaner import clean_claims, clean_billing
from healthconnect.features.engineer import build_claims_analytical_dataset
from healthconnect.data.validator import validate_dataframe_schema


class TestPipelineComponentChaining:
    """Verify contracts and data flow across sequential pipeline stages."""

    def test_claims_end_to_end_flow(self):
        """Test Raw Claims & Billing -> Cleaning -> Feature Eng -> Schema Validation -> Model Predict."""
        # 1. Raw synthetic records
        raw_claims = pd.DataFrame({
            "ClaimID": ["CLM_TEST_01", "CLM_TEST_02"],
            "BillingID": ["BIL_TEST_01", "BIL_TEST_02"],
            "Provider": ["  RSSB ", "Radiant  "],
            "ClaimAmount": ["85000", "120000"],
            "Status": ["Approved", "Pending"]
        })
        raw_billing = pd.DataFrame({
            "BillingID": ["BIL_TEST_01", "BIL_TEST_02"],
            "Amount": [100000.0, 110000.0]
        })

        # 2. Stage: Cleaning
        cleaned_claims = clean_claims(raw_claims)
        cleaned_billing = clean_billing(raw_billing)
        assert cleaned_claims["Provider"].iloc[0] == "RSSB"
        assert cleaned_claims["Provider"].iloc[1] == "Radiant"

        # 3. Stage: Feature Engineering
        analytical_claims = build_claims_analytical_dataset(cleaned_claims, cleaned_billing)
        assert "ClaimToBillingRatio" in analytical_claims.columns
        assert "ClaimDiff" in analytical_claims.columns
        assert "IsFullClaim" in analytical_claims.columns

        # 4. Stage: Schema Validation
        features = ["ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim", "Provider"]
        model_input = analytical_claims[features]
        is_valid, errors = validate_dataframe_schema(model_input, "claims")
        assert is_valid is True
        assert len(errors) == 0

        # 5. Stage: Inference Pipeline Execution
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        preds = pipe.predict(model_input)
        probas = pipe.predict_proba(model_input)

        assert len(preds) == 2
        assert preds[0] in [0, 1]
        assert preds[1] in [0, 1]
        assert probas.shape == (2, 2)
        assert (probas >= 0.0).all() and (probas <= 1.0).all()

    def test_billing_end_to_end_flow(self, sample_billing_payload):
        """Test Encounter Billing Payload -> Validation -> Pipeline Prediction -> Confidence Bounds."""
        input_df = pd.DataFrame([sample_billing_payload])

        # Validate Schema
        is_valid, errors = validate_dataframe_schema(input_df, "billing")
        assert is_valid is True

        # Pipeline inference
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        pred_amount = float(pipe.predict(input_df)[0])
        assert pred_amount > 0

        # Post-processing interval calculation
        rmse = 82993.0
        ci_lower = max(0.0, pred_amount - 1.96 * rmse)
        ci_upper = pred_amount + 1.96 * rmse
        assert ci_lower <= pred_amount <= ci_upper

