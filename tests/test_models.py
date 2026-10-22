"""
Unit tests for model loading, prediction shape, and metric computation.
"""

import pytest
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from healthconnect.config import ARTIFACTS_DIR
from healthconnect.models.classifier import evaluate_classifier
from healthconnect.models.regressor import evaluate_regressor

def test_serialized_model_artifacts_exist():
    """Verify that all core serialized model artifacts exist in artifacts/."""
    expected_artifacts = [
        "claims_classifier.joblib",
        "billing_regressor.joblib",
        "satisfaction_classifier.joblib",
        "admission_triage_classifier.joblib",
        "patient_clusterer.joblib",
        "facility_clusterer.joblib",
        "anomaly_detector.joblib"
    ]
    for art in expected_artifacts:
        art_path = ARTIFACTS_DIR / art
        assert art_path.exists(), f"Artifact {art} does not exist!"

def test_claims_classifier_inference():
    """Verify claims classifier pipeline loads and outputs binary prediction."""
    pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
    sample_input = pd.DataFrame([{
        "ClaimAmount": 85000.0,
        "BillingAmount": 100000.0,
        "ClaimToBillingRatio": 0.85,
        "ClaimDiff": 15000.0,
        "IsFullClaim": 0,
        "Provider": "RSSB"
    }])
    
    pred = pipe.predict(sample_input)
    proba = pipe.predict_proba(sample_input)
    assert len(pred) == 1
    assert pred[0] in [0, 1]
    assert proba.shape == (1, 2)
    assert round(float(proba.sum()), 2) == 1.0

def test_billing_regressor_inference():
    """Verify billing regressor pipeline loads and outputs positive amount."""
    pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
    sample_input = pd.DataFrame([{
        "Age": 45,
        "BMI": 24.5,
        "DoctorExperience": 10,
        "FacilityApptVolume": 200,
        "PatientToDoctorRatio": 12.0,
        "BedToDoctorRatio": 5.0,
        "DepartmentWorkload": 50,
        "Month": 5,
        "VisitType": "Consultation",
        "Diagnosis": "Malaria",
        "Severity": "Moderate",
        "Gender": "Female",
        "MaritalStatus": "Single",
        "Occupation": "Teacher",
        "Education": "Degree",
        "InsuranceID": "INS001",
        "ChronicCondition": "None",
        "DepartmentName": "Internal Medicine",
        "ProvinceName": "Kigali City"
    }])
    
    pred = pipe.predict(sample_input)
    assert len(pred) == 1
    assert pred[0] > 0
