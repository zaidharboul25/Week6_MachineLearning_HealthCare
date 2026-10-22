"""
Unit tests for feature engineering logic and target leakage prevention.
"""

import pytest
import pandas as pd
import numpy as np

from healthconnect.features.engineer import (
    derive_age_group,
    derive_bmi_category,
    build_claims_analytical_dataset
)

def test_derive_age_group():
    """Verify age grouping boundaries."""
    ages = pd.Series([12, 17, 18, 35, 36, 50, 51, 65, 75])
    groups = derive_age_group(ages)
    assert groups.iloc[0] == "<18"
    assert groups.iloc[1] == "<18"
    assert groups.iloc[2] == "18-35"
    assert groups.iloc[4] == "36-50"
    assert groups.iloc[6] == "51-65"
    assert groups.iloc[8] == ">65"

def test_derive_bmi_category():
    """Verify WHO BMI category classifications."""
    bmis = pd.Series([17.5, 22.0, 27.5, 33.0])
    cats = derive_bmi_category(bmis)
    assert cats.iloc[0] == "Underweight"
    assert cats.iloc[1] == "Normal"
    assert cats.iloc[2] == "Overweight"
    assert cats.iloc[3] == "Obese"

def test_claims_financial_features():
    """Verify claims financial ratio computations."""
    df_claims = pd.DataFrame({
        "ClaimID": ["CLM01", "CLM02"],
        "BillingID": ["BIL01", "BIL02"],
        "Provider": ["RSSB", "MMI"],
        "ClaimAmount": [50000.0, 120000.0],
        "Status": ["Approved", "Pending"]
    })
    df_billing = pd.DataFrame({
        "BillingID": ["BIL01", "BIL02"],
        "Amount": [100000.0, 100000.0]
    })
    
    res = build_claims_analytical_dataset(df_claims, df_billing)
    assert res["ClaimToBillingRatio"].iloc[0] == 0.5
    assert res["ClaimToBillingRatio"].iloc[1] == 1.2
    assert res["ClaimDiff"].iloc[0] == 50000.0
    assert res["ClaimDiff"].iloc[1] == -20000.0
    assert res["TargetStatus"].iloc[0] == 1
    assert res["TargetStatus"].iloc[1] == 0
