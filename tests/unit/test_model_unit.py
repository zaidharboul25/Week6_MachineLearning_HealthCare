"""
Unit tests for Machine Learning Models, Serialization, and Contracts (Category C).
Tests artifact integrity, prediction contracts, probability calibration,
and metric calculation logic across all 7 HealthConnect models.
"""

import pytest
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from healthconnect.config import ARTIFACTS_DIR
from healthconnect.models.classifier import evaluate_classifier
from healthconnect.models.regressor import evaluate_regressor


class TestModelLoadingAndArtifacts:
    """Verify serialized artifacts exist and load correctly."""

    @pytest.mark.parametrize("artifact_name", [
        "claims_classifier.joblib",
        "billing_regressor.joblib",
        "satisfaction_classifier.joblib",
        "admission_triage_classifier.joblib",
        "patient_clusterer.joblib",
        "facility_clusterer.joblib",
        "anomaly_detector.joblib"
    ])
    def test_artifact_exists_and_loads(self, artifact_name):
        path = ARTIFACTS_DIR / artifact_name
        assert path.exists(), f"Artifact {artifact_name} not found on disk."
        model = joblib.load(path)
        assert model is not None, f"Failed to deserialize {artifact_name}."


class TestModelPredictionContracts:
    """Test inference contracts, prediction shapes, and probabilities."""

    def test_claims_classifier_contract(self):
        pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
        sample = pd.DataFrame([{
            "ClaimAmount": 70000.0,
            "BillingAmount": 100000.0,
            "ClaimToBillingRatio": 0.7,
            "ClaimDiff": 30000.0,
            "IsFullClaim": 0,
            "Provider": "RSSB"
        }])
        pred = pipe.predict(sample)
        proba = pipe.predict_proba(sample)

        # Output shape and type
        assert len(pred) == 1
        assert int(pred[0]) in [0, 1]
        assert proba.shape == (1, 2)
        assert 0.0 <= proba[0][0] <= 1.0
        assert 0.0 <= proba[0][1] <= 1.0
        assert round(float(proba[0].sum()), 4) == 1.0

    def test_billing_regressor_contract(self, sample_billing_payload):
        pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
        sample = pd.DataFrame([sample_billing_payload])
        pred = pipe.predict(sample)

        assert len(pred) == 1
        assert isinstance(float(pred[0]), float)
        assert pred[0] > 0.0, "Predicted encounter billing amount must be positive."

    def test_admission_triage_contract(self, sample_triage_payload):
        pipe = joblib.load(ARTIFACTS_DIR / "admission_triage_classifier.joblib")
        sample = pd.DataFrame([sample_triage_payload])
        pred = pipe.predict(sample)

        assert len(pred) == 1
        assert int(pred[0]) in [0, 1]

    def test_patient_satisfaction_contract(self, sample_satisfaction_payload):
        pipe = joblib.load(ARTIFACTS_DIR / "satisfaction_classifier.joblib")
        sample = pd.DataFrame([sample_satisfaction_payload])
        pred = pipe.predict(sample)

        assert len(pred) == 1
        # Target classes: 0 (Low), 1 (Medium), 2 (High) or corresponding string tiers
        assert pred[0] in [0, 1, 2, "Low", "Medium", "High"]

    def test_patient_clustering_contract(self):
        artifact = joblib.load(ARTIFACTS_DIR / "patient_clusterer.joblib")
        kmeans = artifact["kmeans"]
        scaler = artifact["scaler"]
        feature_cols = artifact["feature_cols"]
        assert len(feature_cols) == 6
        # 6 features: Age, BMI, HasChronicCondition, HistoricalApptCount, TotalBilledAmount, SevereDiagnosisCount
        sample = pd.DataFrame([{
            "Age": 45.0,
            "BMI": 26.5,
            "HasChronicCondition": 1,
            "HistoricalApptCount": 3,
            "TotalBilledAmount": 150000.0,
            "SevereDiagnosisCount": 0
        }])[feature_cols]
        scaled_sample = scaler.transform(sample)
        cluster_id = kmeans.predict(scaled_sample)
        assert len(cluster_id) == 1
        assert cluster_id[0] in [0, 1, 2]

    def test_anomaly_detector_contract(self):
        detector = joblib.load(ARTIFACTS_DIR / "anomaly_detector.joblib")
        sample = pd.DataFrame([{
            "ClaimAmount": 100000.0,
            "BillingAmount": 100000.0,
            "ClaimToBillingRatio": 1.0
        }])
        flag = detector.predict(sample)
        # Isolation Forest outputs 1 for inlier, -1 for anomaly
        assert flag[0] in [1, -1]


class TestMetricsEvaluationFunctions:
    """Verify metrics calculation logic."""

    def test_evaluate_classifier_metrics(self):
        from sklearn.dummy import DummyClassifier
        X = pd.DataFrame({"feat": [1, 2, 3, 4]})
        y = pd.Series([0, 1, 0, 1])
        model = DummyClassifier(strategy="most_frequent")
        model.fit(X, y)

        metrics = evaluate_classifier(model, X, y, is_multiclass=False)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert "confusion_matrix" in metrics
        assert 0.0 <= metrics["accuracy"] <= 1.0

    def test_evaluate_regressor_metrics(self):
        from sklearn.dummy import DummyRegressor
        X = pd.DataFrame({"feat": [1, 2, 3, 4]})
        y = pd.Series([100.0, 200.0, 150.0, 250.0])
        model = DummyRegressor(strategy="mean")
        model.fit(X, y)

        metrics = evaluate_regressor(model, X, y)
        assert "rmse" in metrics
        assert "mae" in metrics
        assert "r2" in metrics
        assert metrics["rmse"] >= 0.0
        assert metrics["mae"] >= 0.0
