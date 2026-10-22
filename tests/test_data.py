"""
Unit tests for data integrity and data loading.
Uses small synthetic fixtures and validates schema invariants.
"""

import pytest
import pandas as pd
import numpy as np

from healthconnect.config import DATA_RAW_DIR, DATA_PROCESSED_DIR, DATASET_FILES
from healthconnect.data.cleaner import clean_patients, clean_appointments, clean_billing

def test_raw_datasets_exist():
    """Verify that all 27 expected raw datasets exist in data/raw/."""
    for key, filename in DATASET_FILES.items():
        filepath = DATA_RAW_DIR / filename
        assert filepath.exists(), f"Missing required raw dataset: {filename}"

def test_clean_patients_synthetic():
    """Verify patient cleaning logic on synthetic data."""
    synthetic_df = pd.DataFrame({
        "PatientID": ["PAT001", "PAT002"],
        "Age": [45, 130],  # 130 should be clipped
        "HeightCm": [170, 160],
        "WeightKg": [70, 50],
        "BMI": [np.nan, 19.5],
        "ChronicCondition": [np.nan, "Diabetes"],
        "Gender": ["Male", "Female"],
        "MaritalStatus": ["Single", "Married"],
        "Occupation": ["Engineer", "Farmer"],
        "Education": ["Degree", "Primary"],
        "BloodGroup": ["O+", "A+"],
        "Status": ["Active", "Active"]
    })
    
    cleaned = clean_patients(synthetic_df)
    assert cleaned["ChronicCondition"].iloc[0] == "None"
    assert cleaned["ChronicCondition"].iloc[1] == "Diabetes"
    assert cleaned["Age"].iloc[1] <= 120
    assert not np.isnan(cleaned["BMI"].iloc[0])
    assert cleaned["BMI"].iloc[0] == round(70 / (1.7 ** 2), 1)

def test_clean_billing_synthetic():
    """Verify non-negative billing constraint."""
    df = pd.DataFrame({
        "BillingID": ["BIL01", "BIL02"],
        "Amount": [-500, 150000],
        "Status": ["Pending", "Paid"]
    })
    cleaned = clean_billing(df)
    assert (cleaned["Amount"] >= 0).all()
    assert cleaned["Amount"].iloc[0] == 0
