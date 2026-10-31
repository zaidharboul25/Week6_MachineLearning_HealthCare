"""
Pytest configuration and synthetic fixtures for HealthConnect Rwanda.
Strictly uses anonymized, synthetic healthcare records — ZERO real patient PII.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from healthconnect.config import ARTIFACTS_DIR
from deployment.app import app, load_models

@pytest.fixture(scope="session", autouse=True)
def setup_api_models():
    """Ensure all serialized artifacts are loaded for API and model testing."""
    load_models()

@pytest.fixture
def synthetic_patients_raw():
    """Synthetic raw patient records fixture."""
    return pd.DataFrame({
        "PatientID": ["PAT001", "PAT002", "PAT003", "PAT004"],
        "Age": [25, 45, 135, -5],  # Contains out-of-bounds to test clipping
        "HeightCm": [175, 160, 180, 150],
        "WeightKg": [75, 62, 85, 45],
        "BMI": [24.5, np.nan, 26.2, np.nan],  # Contains NaNs
        "Gender": ["Male", "Female", "Female", "Male"],
        "MaritalStatus": ["Single", "Married", "Divorced", "Single"],
        "Occupation": ["Teacher", "Farmer", "Civil Servant", "Student"],
        "Education": ["Degree", "Primary", "Secondary", "None"],
        "BloodGroup": ["O+", "A+", "B+", "O-"],
        "ChronicCondition": ["None", np.nan, "Hypertension", "Diabetes"],
        "Status": ["Active", "Active", "Inactive", "Active"]
    })

@pytest.fixture
def synthetic_billing_raw():
    """Synthetic raw billing records fixture."""
    return pd.DataFrame({
        "BillingID": ["BIL001", "BIL002", "BIL003"],
        "AppointmentID": ["APT001", "APT002", "APT003"],
        "Amount": [75000.0, -1000.0, 150000.0],  # Contains negative value to test clipping
        "Status": ["Paid", "Pending", "Paid"]
    })

@pytest.fixture
def sample_claims_payload():
    """Valid claims inference payload."""
    return {
        "Provider": "RSSB",
        "ClaimAmount": 75000.0,
        "BillingAmount": 90000.0
    }

@pytest.fixture
def sample_billing_payload():
    """Valid billing encounter inference payload."""
    return {
        "Age": 42,
        "BMI": 25.4,
        "DoctorExperience": 12,
        "FacilityApptVolume": 280,
        "PatientToDoctorRatio": 14.5,
        "BedToDoctorRatio": 6.8,
        "DepartmentWorkload": 55,
        "Month": 7,
        "VisitType": "Consultation",
        "Diagnosis": "Malaria",
        "Severity": "Moderate",
        "Gender": "Female",
        "MaritalStatus": "Married",
        "Occupation": "Teacher",
        "Education": "Degree",
        "InsuranceID": "INS001",
        "ChronicCondition": "None",
        "DepartmentName": "Internal Medicine",
        "ProvinceName": "Kigali City"
    }

@pytest.fixture
def sample_triage_payload():
    """Valid admission triage inference payload."""
    return {
        "Age": 55,
        "BMI": 27.8,
        "DoctorExperience": 15,
        "FacilityApptVolume": 320,
        "PatientToDoctorRatio": 16.0,
        "Gender": "Male",
        "MaritalStatus": "Married",
        "Occupation": "Civil Servant",
        "Education": "Degree",
        "InsuranceID": "INS001",
        "ChronicCondition": "Hypertension",
        "Severity": "Severe",
        "DepartmentName": "Emergency",
        "ProvinceName": "Kigali City"
    }

@pytest.fixture
def sample_satisfaction_payload():
    """Valid patient satisfaction inference payload."""
    return {
        "Age": 38,
        "BMI": 23.1,
        "Amount": 45000.0,
        "DoctorExperience": 9,
        "PatientToDoctorRatio": 11.2,
        "DepartmentWorkload": 40,
        "VisitType": "Consultation",
        "Severity": "Mild",
        "Diagnosis": "Hypertension",
        "Gender": "Female",
        "InsuranceID": "INS001",
        "DepartmentName": "Cardiology"
    }

