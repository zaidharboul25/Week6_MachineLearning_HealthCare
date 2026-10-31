"""
Cross-Track Interface Contract Validation Tests (Data Science -> Machine Learning Engineering).
Validates interface compatibility, feature schema expectations, and data contract compliance
between Data Science model specifications and the serving ML pipeline.
"""

import pytest
import pandas as pd
import numpy as np
import joblib

from healthconnect.config import ARTIFACTS_DIR
from healthconnect.data.validator import MODEL_FEATURE_SCHEMAS, validate_dataframe_schema
from healthconnect.utils.exceptions import HealthConnectSchemaError


class TestCrossTrackInterfaceContracts:
    """Validate interface contracts between DS modeling and MLE pipeline serving."""

    def test_ds_mle_claims_feature_contract(self):
        """
        Verify that the feature vector specified by Data Science for claim approval
        matches the exact inputs processed by the ML Engineering serving pipeline.
        """
        expected_ds_features = [
            "ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim", "Provider"
        ]
        mle_contract = MODEL_FEATURE_SCHEMAS["claims"]["required_columns"]
        assert mle_contract == expected_ds_features

        # Test against loaded pipeline
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        preprocessor = pipe.named_steps["preprocessor"]
        
        # Verify columns matched in ColumnTransformer
        transformer_cols = []
        for name, trans, cols in preprocessor.transformers:
            if name != "remainder":
                transformer_cols.extend(cols)
        assert set(transformer_cols) == set(expected_ds_features)

    def test_ds_mle_contract_detects_missing_ratio_feature(self):
        """
        Simulate a contract violation: Data Science passes raw amounts but omits
        engineered feature `ClaimToBillingRatio`. Pipeline must detect violation cleanly.
        """
        payload_missing_ratio = pd.DataFrame([{
            "ClaimAmount": 50000.0,
            "BillingAmount": 60000.0,
            # Omitting ClaimToBillingRatio, ClaimDiff, IsFullClaim
            "Provider": "RSSB"
        }])

        with pytest.raises(HealthConnectSchemaError) as exc_info:
            validate_dataframe_schema(payload_missing_ratio, "claims")
        
        err_msg = str(exc_info.value)
        assert "Missing required columns" in err_msg
        assert "ClaimToBillingRatio" in err_msg

    def test_ds_mle_probability_threshold_contract(self):
        """
        Verify probability contract: Data Science specifies binary decision boundary at 0.50 threshold.
        Verify serving logic adheres strictly to this contract.
        """
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        sample = pd.DataFrame([{
            "ClaimAmount": 85000.0,
            "BillingAmount": 100000.0,
            "ClaimToBillingRatio": 0.85,
            "ClaimDiff": 15000.0,
            "IsFullClaim": 0,
            "Provider": "RSSB"
        }])

        pred = pipe.predict(sample)[0]
        proba_approved = pipe.predict_proba(sample)[0][1]

        # Verification of threshold contract
        if proba_approved >= 0.50:
            assert pred == 1
        else:
            assert pred == 0

