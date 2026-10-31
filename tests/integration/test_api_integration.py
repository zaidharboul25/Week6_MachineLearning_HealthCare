"""
Integration tests for FastAPI ML Inference Service (Category D).
Verifies HTTP endpoints, Pydantic request validation, error responses (422, 503),
and complete multi-model prediction responses.
"""

import pytest
from starlette.testclient import TestClient
from deployment.app import app, load_models, models

client = TestClient(app)

@pytest.fixture(autouse=True)
def ensure_models_loaded():
    """Ensure models are active in memory before each test."""
    load_models()


class TestFastAPIEndpoints:
    """Test suite for FastAPI endpoints."""

    def test_health_check_endpoint(self):
        """Verify /health returns 200, status Healthy, and model list."""
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "Healthy"
        assert "claims" in data["models_loaded"]
        assert "billing" in data["models_loaded"]
        assert "triage" in data["models_loaded"]
        assert "satisfaction" in data["models_loaded"]

    def test_predict_claims_success(self, sample_claims_payload):
        """Verify POST /predict/claims returns 200 and prediction payload."""
        resp = client.post("/predict/claims", json=sample_claims_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["prediction_label"] in ["Approved", "Pending"]
        assert data["prediction_code"] in [0, 1]
        assert 0.0 <= data["probability_approved"] <= 1.0
        assert "recommendation" in data

    def test_predict_billing_success(self, sample_billing_payload):
        """Verify POST /predict/billing returns 200 and confidence intervals."""
        resp = client.post("/predict/billing", json=sample_billing_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["predicted_billing_amount_rwf"] > 0
        assert data["confidence_interval_lower_rwf"] <= data["predicted_billing_amount_rwf"]
        assert data["confidence_interval_upper_rwf"] >= data["predicted_billing_amount_rwf"]
        assert "notes" in data

    def test_predict_triage_success(self, sample_triage_payload):
        """Verify POST /predict/triage returns 200 and triage recommendation."""
        resp = client.post("/predict/triage", json=sample_triage_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["prediction_label"] in ["Emergency", "Routine"]
        assert data["is_emergency"] in [0, 1]
        assert "recommendation" in data

    def test_predict_satisfaction_success(self, sample_satisfaction_payload):
        """Verify POST /predict/satisfaction returns 200 and satisfaction tier."""
        resp = client.post("/predict/satisfaction", json=sample_satisfaction_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["predicted_satisfaction_tier"] in ["Low", "Medium", "High", "0", "1", "2"]
        assert "recommendation" in data

    def test_validation_error_negative_claim(self):
        """Verify Pydantic input validation rejects negative claim amount with 422."""
        invalid_payload = {
            "Provider": "RSSB",
            "ClaimAmount": -50000.0,
            "BillingAmount": 100000.0
        }
        resp = client.post("/predict/claims", json=invalid_payload)
        assert resp.status_code == 422
        data = resp.json()
        assert "detail" in data

    def test_validation_error_missing_required_field(self):
        """Verify Pydantic input validation rejects missing fields with 422."""
        incomplete_payload = {
            "Provider": "RSSB",
            # Missing ClaimAmount and BillingAmount
        }
        resp = client.post("/predict/claims", json=incomplete_payload)
        assert resp.status_code == 422

    def test_service_unavailable_when_model_unloaded(self, sample_claims_payload):
        """Verify graceful 503 response if model is unavailable."""
        saved_claims_model = models.pop("claims", None)
        try:
            resp = client.post("/predict/claims", json=sample_claims_payload)
            assert resp.status_code == 503
            assert resp.json()["detail"] == "Claims model unavailable"
        finally:
            if saved_claims_model is not None:
                models["claims"] = saved_claims_model

