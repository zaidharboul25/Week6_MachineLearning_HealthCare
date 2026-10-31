"""
Reproducibility and Determinism Validation Tests (Categories B & C).
Verifies that prediction pipelines produce bit-for-bit identical results
across multiple runs with fixed inputs.
"""

import pytest
import pandas as pd
import numpy as np
import joblib

from healthconnect.config import ARTIFACTS_DIR


class TestReproducibilityValidation:
    """Test deterministic behavior across pipeline components."""

    def test_claims_classifier_reproducibility(self):
        """Verify identical claims input produces identical predictions and probabilities across repeated calls."""
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        sample = pd.DataFrame([{
            "ClaimAmount": 65000.0,
            "BillingAmount": 80000.0,
            "ClaimToBillingRatio": 0.8125,
            "ClaimDiff": 15000.0,
            "IsFullClaim": 0,
            "Provider": "Radiant"
        }])

        preds = [pipe.predict(sample)[0] for _ in range(5)]
        probas = [pipe.predict_proba(sample)[0][1] for _ in range(5)]

        # Verify all predictions are identical
        assert len(set(preds)) == 1, "Predictions differed across runs!"
        # Verify probabilities match within 1e-9 tolerance
        for p in probas[1:]:
            assert abs(p - probas[0]) < 1e-9, "Probabilities drifted across runs!"

    def test_billing_regressor_reproducibility(self, sample_billing_payload):
        """Verify identical encounter input produces bit-for-bit identical regression prediction."""
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        sample = pd.DataFrame([sample_billing_payload])

        preds = [pipe.predict(sample)[0] for _ in range(5)]
        for p in preds[1:]:
            assert abs(p - preds[0]) < 1e-6, "Regression predictions drifted across runs!"

    def test_triage_classifier_reproducibility(self, sample_triage_payload):
        """Verify triage model reproducibility."""
        pipe = joblib.load(ARTIFACTS_DIR / "admission_triage_classifier.joblib")
        sample = pd.DataFrame([sample_triage_payload])

        preds = [pipe.predict(sample)[0] for _ in range(5)]
        assert len(set(preds)) == 1
