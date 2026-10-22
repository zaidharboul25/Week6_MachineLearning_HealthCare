"""
Integration tests for FastAPI ML Inference Service.
Tests /health, /predict/claims, and /predict/billing endpoints.
"""

import pytest
from starlette.testclient import TestClient
from deployment.app import app, load_models

client = TestClient(app)

@pytest.fixture(autouse=True)
def init_api_models():
    """Ensure models are loaded in FastAPI state."""
    load_models()

def test_health_endpoint():
    """Test /health probe returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Healthy"
    assert "claims" in data["models_loaded"]
    assert "billing" in data["models_loaded"]

def test_predict_claims_endpoint():
    """Test insurance claim approval prediction endpoint."""
    payload = {
        "Provider": "RSSB",
        "ClaimAmount": 80000.0,
        "BillingAmount": 95000.0
    }
    response = client.post("/predict/claims", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_label"] in ["Approved", "Pending"]
    assert 0.0 <= data["probability_approved"] <= 1.0
    assert "recommendation" in data

def test_predict_billing_endpoint():
    """Test encounter billing amount prediction endpoint."""
    payload = {
        "Age": 52,
        "BMI": 28.2,
        "DoctorExperience": 14,
        "FacilityApptVolume": 310,
        "PatientToDoctorRatio": 15.2,
        "BedToDoctorRatio": 7.1,
        "DepartmentWorkload": 65,
        "Month": 6,
        "VisitType": "Consultation",
        "Diagnosis": "Diabetes",
        "Severity": "Moderate",
        "Gender": "Male",
        "MaritalStatus": "Married",
        "Occupation": "Civil Servant",
        "Education": "University",
        "InsuranceID": "INS001",
        "ChronicCondition": "Diabetes",
        "DepartmentName": "Internal Medicine",
        "ProvinceName": "Kigali City"
    }
    response = client.post("/predict/billing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_billing_amount_rwf"] > 0
    assert data["confidence_interval_lower_rwf"] <= data["predicted_billing_amount_rwf"]
    assert data["confidence_interval_upper_rwf"] >= data["predicted_billing_amount_rwf"]

def test_predict_claims_invalid_input():
    """Verify input validation rejects negative claim amount with 422."""
    payload = {
        "Provider": "RSSB",
        "ClaimAmount": -5000.0,
        "BillingAmount": 10000.0
    }
    response = client.post("/predict/claims", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_predict_missing_model_behavior():
    """Verify missing model returns 503 without revealing server internals."""
    from deployment.app import models
    models.clear()
    payload = {
        "Provider": "RSSB",
        "ClaimAmount": 5000.0,
        "BillingAmount": 10000.0
    }
    response = client.post("/predict/claims", json=payload)
    assert response.status_code == 503
    assert response.json()["detail"] == "Claims model unavailable"
    # Reload for subsequent tests
    load_models()
